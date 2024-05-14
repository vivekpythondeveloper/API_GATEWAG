import jwt
from datetime import datetime, timedelta

class TokenManager:
    def __init__(self, app) -> None:
        self.app = app

    # Generate JWT token
    def generate_token(self, org_name, schema_assign, org_id, email):
        payload = {
            'org_name': org_name,
            'schema_assign': schema_assign,
            'org_id': org_id,
            'email': email,
            'exp': datetime.now() + timedelta(minutes=30)  # Token expiration time
        }
        token = jwt.encode(payload, self.app.config['SECRET_KEY'], algorithm='HS256')
        return token
    
    # Verify JWT token
    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return 'Expired token. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'