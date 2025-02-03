from flask import jsonify
from web.models import db
from web.apis.users import user_bp
from web.apis.auth import basic_auth, token_auth


@user_bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})

@user_bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', 204


import jwt
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class HashAuth:
    def __init__(self):
        self.secret_key = getenv('SECRET_KEY')

    def hash_it(self, id):
        payload = {"id": id}
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def unhash_it(self, hashed):
        try:
            payload = jwt.decode(hashed, self.secret_key, algorithms=["HS256"])
            return payload.get("id")
        except jwt.ExpiredSignatureError:
            # Handle token expiration if needed
            return None
        except jwt.DecodeError:
            # Handle invalid token if needed
            return None

# Usage example
hash_auth = HashAuth()

user_auth = HashAuth()
user_id = "12345"
hashed_user_id = user_auth.hash_it(user_id)

# Transmit hashed_user_id over WebSocket

# When received on the openai_client-side, unhash it
unhashed_user_id = user_auth.unhash_it(hashed_user_id)

# print(f"Original User ID: {unhashed_user_id}")
# print(f"Hashed User ID: {hashed_user_id}")
