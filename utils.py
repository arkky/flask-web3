import re
from datetime import datetime as dt
from datetime import timedelta as td

import jwt
from web3 import Web3
from eth_account.messages import encode_defunct
from eth_account.account import Account

PRIVATE_KEY = "0d2dacbdc69bee88720ea2f9d5652ad0941303c6fe4e9e269869e312279970a0"
WALLET_ADDR = "0x0914B7665920386a9F05a53e83d1c999B25Eedb5"


def validate_email(email: str) -> bool:  
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):  
        return True  
    return False

def validate_password(password: str) -> bool:
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    match = re.match(pattern, password)
    return bool(match)

def create_token(user_id: int) -> str:
    hash = Web3.keccak(user_id)
    eth_signed_message = encode_defunct(hexstr=hash.hex())
    private_signed_message = Account.sign_message(eth_signed_message, private_key=PRIVATE_KEY)
    return private_signed_message.signature.hex()

def encode_jwt_token(user_id: int) -> str:
    jwt_token = jwt.encode(
        payload={
            "exp": dt.utcnow() + td(days=30), 
            "iat": dt.utcnow(), 
            "sub": user_id
        }, 
        key=PRIVATE_KEY, 
        algorithm="HS256"
    )
    return jwt_token

def decode_jwt_token(jwt_token: str) -> dict[str, None]:
    payload = jwt.decode(jwt_token, key=PRIVATE_KEY, algorithms=["HS256"])
    return payload