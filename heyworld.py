from flask import Flask, render_template, request, url_for, redirect, abort
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


def get_all_users():
    # Connects to DB
    sqliteConnection = sqlite3.connect('usersDB.sqlite3')
    cursor = sqliteConnection.cursor()
    # Print statement and execution
    print("-----------------------------Getting all users ")
    request = "SELECT * FROM Users ORDER BY first_name"
    users = []
    try:
        cursor.execute(request)
    except Exception as e:
        print("Error executing get_all_users " + str(e))
    records = cursor.fetchall()
    if len(records) != 0:
        print("Users found: " + str(len(records)))
        for user in records:
            # print(str(user))
            new_user = {
                "user_id": user[0],
                "first_name": user[1],
                "last_name": user[2],
                "email": user[3],
                "gender": user[4],
                "avatar": user[5],
            }
            users.append(new_user)

    else:
        print("No user found")
    cursor.close()
    if sqliteConnection:
        sqliteConnection.close()
        print("-----------------------------DB Disconnected")
        # Returning results (can be empty array)
        return users


@app.route('/')
def index():
    # abort(401)
    return redirect(url_for('user', user_id='derickrp6'))
    return "Hello world"


@app.route('/user/<user_id>', methods=['GET'])
def user(user_id):
    userdata = get_user_profile(user_id)
    return userdata


@app.route('/users/', methods=['GET'])
def users():
    usersdata = get_all_users()
    return render_template('users.html',
                           userlist=usersdata,
                           listlen=len(usersdata))


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
    print(url_for('user', user_id=new_user['user_id']))
    print(new_user)
    print(request.form)
    return new_user