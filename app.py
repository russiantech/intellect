from os import getenv
from flask import jsonify
from web import create_app
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# app = create_app('development')  # Set to 'production' if needed
app = create_app('production')  # Set to 'production' if needed

@app.route("/routes")
def site_map():
    links = []
    # for rule in app.url_map.iter_rules():
    for rule in app.url_map._rules:
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        links.append({'url': rule.rule, 'view': rule.endpoint})
    return jsonify(links), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(getenv("PORT", 5001)))
    # app.run(debug=True, port=5001) 
    