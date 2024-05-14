from models.users import user_model
class UsersHandler:
    def __init__(self) -> None:
        pass
    
    def add_user(self, data, schema):
        username = data['username']
        email = data['email']
        password = data['password']
        org_name = data.get('org_name')
        org_id = data.get('org_id')
        User = user_model(schema)
        # Attempt to insert the new client
        new_user = User.insert(username=username, email=email, 
                                      password=password, org_name=org_name, org_id=org_id)
        return new_user
    
    def user_login(self, email, org_id, password, schema):
        filters = {"email": email, "org_id": org_id}
        User = user_model(schema)
        user_data = User.dynamic_query(filters=filters)
        user_data = user_data[0]
        password_valid = user_data.check_password(password=password)
        if not password_valid:
            return False
        return user_data
