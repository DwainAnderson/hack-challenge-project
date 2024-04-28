import os
from werkzeug.security import check_password_hash
from sessions import password_login, session_messages
import json
from database.db import DatabaseDriver
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration
app.config.from_mapping(
    DATABASE="database/site.sqlite",
    INIT_SQL="database/init.sql"
)

# Initialize database
driver = DatabaseDriver(app.config['DATABASE'], app.config['INIT_SQL'])

# Connect to the database
def get_db():
    if 'db' not in g:
        g.db = driver.conn
    return g.db

# Close database connection
@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def success_response(body, code=200):
    """
    Success response function
    """
    return json.dumps(body), code

def failure_response(message, code=404):
    """
    Failure response function
    """
    error_message = {'error': message}
    return json.dumps(error_message), code


#Routes

##User Login/Logut Section -> Function Calls to sessions.py and db
@app.route('/login', methods=['POST'])
def login():
    # Receive login data from request
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if username and password are provided
    if not username or not password:
        return failure_response('Username or password not provided', 400)

    # Call password_login function from sessions.py to verify credentials
    user = password_login(username, password)

    # Check if login was successful
    if user:
        return success_response({'message': 'Login successful', 'user': user}, 200)
    else:
        return failure_response('Invalid username or password', 401)
    
    
def create_user(): 
    pass 

def delete_user(): 
    pass

def update_user():
    pass


if __name__ == '__main__':
    app.run()
