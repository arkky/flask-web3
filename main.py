from flask import Flask, request
from sqlalchemy import create_engine

import traceback

from utils import validate_email, validate_password, create_token
from database import Base
from database import db_session
from models import User


app = Flask(__name__)
engine = create_engine("sqlite:///users.db", echo=True)
Base.metadata.create_all(engine)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

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
                try:
                    user = User(name, surname, email, eth_address, password)
                    db_session.add(user)
                except Exception as e:
                    traceback.print_exc()
                    return "Error on creating user"
                finally:
                    db_session.remove()
                
                token = create_token(user.id)
                try:
                    pass
                    db_session.commit()
                except Exception as e:
                    traceback.print_exc()
                    db_session.rollback()
                    return "Error on creating token"

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