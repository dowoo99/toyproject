from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, redirect, url_for
import hashlib
import datetime
import jwt
from pymongo import MongoClient
client = MongoClient(
    'mongodb+srv://test:sparta@cluster0.zwi4g.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta



app = Flask(__name__)


@app.route('/')
def home():
    return render_template('login.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
