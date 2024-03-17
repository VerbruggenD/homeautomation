from flask import Flask, render_template, request, redirect, url_for, session
import os, logging
from source import authentication as auth
from source import function as function

app = Flask(__name__)
app.secret_key = os.urandom(24)

logger = function.setup_logger('app.log', logging.WARNING, logging.DEBUG)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Initialize error message to None

    if request.method == 'POST':
        # Your existing code for handling POST requests
        user = request.form['user']
        password = request.form['password']
        csrf_token = request.form['csrf_token']
        logger.debug(f"CSRF token from post request: {csrf_token}")
        logger.debug(f"CSRF token from session: {session['csrf_token']}")

        # Check CSRF token
        if csrf_token != session.pop('csrf_token', None):
            logger.error(f"CSRF token from session and request is not equal")
            return "CSRF Token Validation Failed"

        # Call the function to handle login
        error = auth.handle_login(user, password)
        if error:
            session['csrf_token'] = os.urandom(24).hex() # renew session token
            logger.debug(f"Generated new CSRF token for user: {user} {session['csrf_token']}")
            logger.debug(f"Failed to log in, error {error}")
            return render_template('login.html', error=error, csrf_token=session['csrf_token'])
        
        # If login is successful, redirect to index
        return redirect(url_for('index'))

    # For GET request (initial page load or error)
    session['csrf_token'] = os.urandom(24).hex()  # Generate a new CSRF token for each request
    logger.debug(f"Generated new CSRF token for new session: {session['csrf_token']}")
    return render_template('login.html', error=error, csrf_token=session['csrf_token'])

@app.route('/index')
def index():
    if 'user' in session:
        user = session['user']
        session['id'] = auth.authentication_data[user]["id"]
        user_data = auth.user_data[session['id']]
        print(user_data)
        return render_template('index.html', username=user, user_data=user_data)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    if session:
        logger.debug(f"session still exists: {session}")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
