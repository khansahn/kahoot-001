import jwt
from datetime import datetime, timedelta
from flask import jsonify

def encode(data):
    payload = {
        "data" : data,
        "exp" : datetime.utcnow() + timedelta(seconds = 3600),
        "iat" : datetime.utcnow()
    }
    encoded = jwt.encode(payload,"kucing-merah",algorithm="HS256").decode('utf-8')
    return encoded

def decode(data):
    decoded = jwt.decode(data,"kucing-merah",algorithms=["HS256"])
    return decoded