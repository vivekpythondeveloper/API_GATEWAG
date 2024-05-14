from flask import Blueprint, jsonify, current_app, request
from token_validater import token_required
from token_validater.token_manager import TokenManager
from handlers.enpoint_handler import EndpointHandler
from handlers.service_handler import ServiceHandler

endpoint_bp = Blueprint('endpoint', __name__)

endpoint_handler = EndpointHandler()
service_handler = ServiceHandler()
token_manager = TokenManager(app=current_app)


@endpoint_bp.route('/services/<service_name>/endpoints', methods=['GET'])
@token_required(token_manager)
def get_endpoints(service_name):
    print(service_name)
    org = request.org
    filters = {"name": service_name}
    service = service_handler.get_service(schema_name=org.get('schema_assign'), filters=filters)
    if not service:
        return jsonify({'error': 'Failed to get service. Check if the service registered.'}), 400
    return jsonify({'endpoints': endpoint_handler.get_endponts(service_name)})
