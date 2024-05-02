# main.py

from auth import auth
from flask import Flask, redirect, url_for
from website import create_app


# Create the Flask application instance using create_app function from website module
app = create_app()

# Register the 'auth' blueprint and define the route to handle the authentication callback
app.register_blueprint(auth)

# Route to handle the authentication callback from Microsoft
@app.route('/getAToken')
def handle_microsoft_callback():
    # Process the authentication token from Microsoft
    # This could involve validating the token, extracting user information, etc.
    return redirect(url_for('auth.login'))

# Entry point for the application
if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
