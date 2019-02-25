from flask import Flask, request, json, jsonify
import requests, os

from src.utils.crypt import encrypt, decrypt
from src.routes import router
app = Flask(__name__)   #buat manggil flask
app.register_blueprint(router)



# masuk ke development mode tanpa setting environment, biar aman taro paling bawah ajaaa abis td nyobain di atas ga jalan heu
if __name__ == "__main__":
    app.run(debug=True, port = 5000)