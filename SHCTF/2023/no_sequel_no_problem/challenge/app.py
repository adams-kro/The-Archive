from flask import Flask, jsonify, render_template, request, redirect, url_for
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

def get_db():
    client = MongoClient(host='mongodb',
                         #host='127.0.0.1',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")
    db = client["users_db"]
    return db

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        db = get_db()
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # query = {'name': {'$eq': username}, 'type': {'$eq': password}}
        query = {"$where": f"this.username == '{username}' && this.password == '{password}'"}

        user = db.user_tb.find_one(query)
        if user:
            print(user)
            return redirect(url_for('home'))

    return render_template('index.html')

@app.route('/home')
def home():
    return "Welcome, flag is admin's password"

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__=='__main__':
    app.run(host="0.0.0.0", port=1337, debug=True)