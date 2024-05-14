import os
from functools import wraps
from flask import request, jsonify


# Generate a secure secret key
def generate_secret_key():
    return os.urandom(24).hex()

def token_required(token_manager):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = None
            try:
                if request.headers:
                    token = request.headers.get('Authorization', '')  # Extract token from Authorization header
            except Exception as e:
                print(f"token not found {str(e)}")
            if not token:
                return jsonify({'message': 'Token is missing'}), 401

            payload = token_manager.verify_token(token)
            if isinstance(payload, dict):
                request.org = payload
                return func(*args, **kwargs)
            else:
                return jsonify({'message': payload}), 401
        return wrapper
    return decorator
