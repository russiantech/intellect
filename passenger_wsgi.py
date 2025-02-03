# from web import app as application
from web import create_app

application = create_app("production")

from flask import jsonify

@application.route("/routes")
def site_map():
    links = []
    # for rule in app.url_map.iter_rules():
    for rule in application.url_map._rules:
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        links.append({'url': rule.rule, 'view': rule.endpoint})
    return jsonify(links), 200

if __name__ == '__main__':
    application.run("localhost", 8000, True, True)