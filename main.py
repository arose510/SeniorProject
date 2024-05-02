# main.py

from flask import Flask, redirect, url_for
from auth import auth, get_token

app = Flask(__name__)
app.register_blueprint(auth)

# Route to handle the authentication callback from Microsoft
@app.route('/getAToken')
def handle_microsoft_callback():
    # Process the authentication token from Microsoft
    # This could involve validating the token, extracting user information, etc.
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)
