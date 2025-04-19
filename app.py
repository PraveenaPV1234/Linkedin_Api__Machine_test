from flask import Flask, jsonify, request, abort
import linkedin_scraper  
import json

app = Flask(__name__)

# Basic Auth Credentials
API_USERNAME = 'admin'
API_PASSWORD = 'secret'

def check_auth(username, password):
    return username == API_USERNAME and password == API_PASSWORD

@app.route('/fetch_profiles_connections', methods=['POST'])
def fetch_profiles_connections():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return abort(401)

    data = linkedin_scraper.main(return_data=True)  
    return jsonify(data)
    
if __name__ == "__main__":
    app.run(debug=True)