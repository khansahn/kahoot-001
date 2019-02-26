from flask import Flask, request
import jwt
from src.routes import router
app = Flask(__name__)   #buat manggil flask
app.register_blueprint(router)

