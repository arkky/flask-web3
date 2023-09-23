from flask import Flask, request
from sqlalchemy.orm import Session
from sqlalchemy import select

import traceback

from utils import validate_email, validate_password, create_token
from database import engine
from models import User


app = Flask(__name__)


@app.post("/sign_up")
def sign_up():
    json_data = request.json
    if json_data:
        email = json_data.get("email")
        password = json_data.get("password")
        if email and password:
            e_status = validate_email(email)
            p_status = validate_password(password)
            if e_status and p_status:
                surname = json_data.get("surname")
                eth_address = json_data.get("eth_address")
                name = json_data.get("name")

                # check user in db
                with Session(engine) as session:
                    stmt = select(User.id).where(User.email == email)
                    result = session.scalars(stmt).all()
                    if result:
                        return "You're already created user with this email"

                # add user to db
                with Session(engine) as session:
                    try:
                        usr = User(
                            name=name,
                            surname=surname,
                            email=email,
                            eth_address=eth_address,
                            password=password
                        )
                        session.add(usr)
                    except:
                        traceback.print_exc()
                        session.rollback()
                        raise
                    else:
                        session.commit()

                # get id of the user
                with Session(engine) as session:
                    stmt = select(User.id).where(User.email == email)
                    user_id = session.scalars(stmt).one()
   
                # update signature to the user
                signature = create_token(user_id)
                with Session(engine) as session:
                    try:
                        stmt = select(User).where(User.id == user_id)
                        usr = session.scalars(stmt).one()
                        usr.signature = signature
                    except:
                        traceback.print_exc()
                        session.rollback()
                        raise
                    else:
                        session.commit()
                
                return {"user_id": user_id, "signature": signature}
            else:
                return "Incorrect email or password"
        else:
            return "We don't get your email or password"
    return "Send to us a JSON POST request with your creds"

@app.post("/sign_in")
def sign_in():
    return f"sign in"

@app.get("/user")
def user():
    return f"user"