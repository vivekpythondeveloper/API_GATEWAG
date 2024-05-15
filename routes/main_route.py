from flask import Blueprint, jsonify, request, current_app
from token_validater import token_required
from handlers.main_handler import MainHandler
from token_validater.token_manager import TokenManager

main_handler = MainHandler()

main_bp = Blueprint('main', __name__)
token_manager = TokenManager(app=current_app)
    
@main_bp.route('/<path:any_path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@token_required(token_manager)
def handle_main(any_path):
    org = request.org
    filters = {"paths": any_path}
    endpoint = main_handler.check_endpoint(schema_name=org.get("schema_assign"), filters=filters)
   # This route will handle any URL path
    return jsonify({'message': 'You have accessed path: {}'.format(endpoint)}), 200
    