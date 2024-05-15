from flask import Blueprint, jsonify, request, current_app
from token_validater import token_required
from handlers.service_handler import ServiceHandler
from handlers.enpoint_handler import EndpointHandler
from token_validater import token_required
from token_validater.token_manager import TokenManager

service_bp = Blueprint('service', __name__)
token_manager = TokenManager(app=current_app)
endpoint_handler = EndpointHandler()
service_handler = ServiceHandler()

@service_bp.route('/services/register', methods=['POST'])
@token_required(token_manager)
def register_service():
    service_handler = ServiceHandler()
    data = request.json
    org = request.org
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    required_fields = ['name', 'url']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    new_service = service_handler.add_service(data=data, schema_name=org.get("schema_assign"))
    if new_service:
        return jsonify({'message': 'Service registered successfully', 'service_id': new_service.service_id}), 201
    else:
        return jsonify({'error': 'Failed to register service. Check if the service already exists.'}), 400
    
@service_bp.route('/services/<service_name>/routes', methods=['POST'])
@token_required(token_manager)
def get_routes(service_name):
    print(service_name)
    org = request.org
    data = request.json
    required_fields = ['paths']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    filters = {"name": service_name}
    service = service_handler.get_service(schema_name=org.get('schema_assign'), filters=filters)
    if not service:
        return jsonify({'error': 'Failed to get service. Check if the service registered.'}), 400
    service_ = service[0]
    data['service_id'] = service_.service_id
    return jsonify({'endpoints': endpoint_handler.add_endpoint(data, org.get('schema_assign'))})

