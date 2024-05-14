from flask import Blueprint, jsonify, request, current_app
from handlers.client_handler import ClientHandler
from handlers.users_handler import UsersHandler
from handlers.service_handler import ServiceHandler
from handlers.enpoint_handler import EndpointHandler
from token_validater.token_manager import TokenManager



client_bp = Blueprint('client', __name__)


@client_bp.route('/clients/register', methods=['POST'])
def register_client():
    client_handler = ClientHandler()
    user_handler = UsersHandler()
    service_handler = ServiceHandler()
    endpoint_handler = EndpointHandler()
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    domain = client_handler.get_domain_from_email(data.get('admin_email'))
    data['domain'] = domain
    required_fields = ['client_name', 'admin_email']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    new_client = client_handler.add_client(data=data)
    if new_client:
        service_handler.create_service(schema_name=new_client.schema_assign)
        endpoint_handler.create_endpoint(schema_name=new_client.schema_assign)
        user_handler.add_user({"username": new_client.admin_email,
                               "email": new_client.admin_email,
                               "password": f"{new_client.schema_assign}@123",
                               "org_name": new_client.client_name,
                               "org_id": new_client.client_id}, schema=new_client.schema_assign)
        return jsonify({'message': 'Client registered successfully', 'client_id': new_client.client_id}), 201
    else:
        return jsonify({'error': 'Failed to register client. Domain already exists.'}), 400
    
@client_bp.route('/clients/login', methods=['POST'])
def client_login():
    token_manager = TokenManager(current_app)
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    required_fields = ['email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    client_handler = ClientHandler()
    domain = client_handler.get_domain_from_email(data.get('email'))
    if not domain:
        return jsonify({'error': 'Email not valid'}), 400
    org = client_handler.get_org_details_by_domain(domain)
    if not org:
        return jsonify({'error': 'Email not registered'}), 400
    org = org[0]
    user_handler = UsersHandler()
    user = user_handler.user_login(email=data.get('email'), org_id=org.client_id, 
                            password=data.get('password'), schema=org.schema_assign)
    if not user:
        return jsonify({'error': 'Validation error'}), 401
    token = token_manager.generate_token(org.client_name, 
                                         schema_assign=org.schema_assign,
                                         org_id=org.client_id, email=user.email)
    response = {'token': token,
                'user_name': user.username,
                'user_id': user.user_id,
                'org': org.client_name}
    return jsonify(response), 200
    