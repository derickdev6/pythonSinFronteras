import re
from flask import Flask, request
import sqlite3
app = Flask(__name__)

def get_user_profile(user_id):
    # Connects to DB
    sqliteConnection = sqlite3.connect('usersDB.sqlite3')
    cursor = sqliteConnection.cursor()
    # Print statement and execution
    print("-----------------------------Getting user " + user_id)
    request = f"SELECT * FROM Users WHERE user_id = \"{user_id}\""
    user = ""
    try:
        cursor.execute(request)
    except Exception as e:
        print("Error executing get_user_profile " + str(e))
    records = cursor.fetchall()
    if len(records) != 0:
        print("User found: " + str(records[0]))
        records = records[0]
        user = {
            "user_id": records[0],
            "first_name": records[1],
            "last_name": records[2],
            "email": records[3],
            "gender": records[4],
            "avatar": records[5],
        }
    else:
        print("No user found")
    cursor.close()
    if sqliteConnection:
        sqliteConnection.close()
        print("-----------------------------DB Disconnected")
    # Returning results (can be empty array)
        return user

@app.route('/')
def index():
    return "Hello world"

@app.route('/user/<user_id>', methods=['GET'])
def hi(user_id):
    userdata = get_user_profile(user_id)
    return str(userdata)

@app.route('/register', methods=['POST'])
def register():
    new_user = {
        "user_id": request.form['user_id'],
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "gender": request.form['gender'],
        "avatar": request.form['avatar'],
    }
    print(new_user)
    print(request.form)
    return "Working"