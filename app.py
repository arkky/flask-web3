import traceback
from datetime import datetime as dt

from flask import Flask, request
from sqlalchemy.orm import Session
from sqlalchemy import select
import jwt

from utils import validate_email, validate_password, create_token, encode_jwt_token, decode_jwt_token
from database import engine
from models import User, Auth

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
    json_data = request.json
    if json_data:
        email = json_data.get("email")
        password = json_data.get("password")
        if email and password:
            e_status = validate_email(email)
            p_status = validate_password(password)
            if e_status and p_status:
                with Session(engine) as session:
                    try:
                        # find user
                        stmt = select(User).where((User.email == email) & (User.password == password))
                        result = session.scalars(stmt).all()
                        if result:
                            user = result[0]

                            # check if token already in db
                            stmt = select(Auth).where(user.id == Auth.user_id)
                            result = session.scalars(stmt).all()
                            jwt_token = encode_jwt_token(user.id)
                            if result:
                                auth = result[0]
                                auth.jwt_token = jwt_token
                            else:
                                auth = Auth(user_id=user.id, jwt_token=jwt_token)
                                session.add(auth)
                        else:
                            return "Invalid email/password"
                    except:
                        traceback.print_exc()
                        session.rollback()
                        raise
                    else:
                        session.commit()
                return {"auth_token": jwt_token}
            else:
                return "Incorrect email or password"
        else:
            return "We don't get your email or password"            
    return "Send to us a JSON POST request with your creds"

@app.get("/user")
def user():
    jwt_token = request.headers.get("Bearer")
    if jwt_token:
        # try to decode token
        try:
            payload = decode_jwt_token(jwt_token)
        except jwt.exceptions.InvalidSignatureError as e:
            return "Invalid token"
        except:
            return "Invalid token. Strong error"

        # check if exp is expired
        exp = payload.get("exp")
        if exp:
            dt_exp = dt.utcfromtimestamp(exp)
            if dt_exp < dt.utcnow():
                return "Your token has expired. Update it"
        else:
            return "Invalid token"

        # return user info
        with Session(engine) as session:
            stmt = select(Auth).where(Auth.jwt_token == jwt_token)
            result = session.scalars(stmt).all()
            if result:
                auth = result[0]
                stmt = select(User).where(User.id == auth.user_id)
                result = session.scalars(stmt).all()
                if result:
                    user = result[0]
                    return {"name": user.name, "surname": user.surname, "email": user.email, "eth_address": user.eth_address}
                else:
                    return "Can't find this user by token"
            else:
                return "Invalid token"
    return "Need Bearer header"