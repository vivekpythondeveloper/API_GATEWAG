from flask import Flask
from db import db, sql_uri
from routes.endpoint_routes import endpoint_bp
from routes.client_route import client_bp
from routes.service_route import service_bp
from token_validater import generate_secret_key

def client_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = generate_secret_key()
    app.config['SQLALCHEMY_DATABASE_URI'] = sql_uri
    # Replace 'username', 'password', 'localhost', and 'dbname' with your PostgreSQL credentials
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    # Register the blueprint
    app.register_blueprint(client_bp)
    app.register_blueprint(endpoint_bp)
    app.register_blueprint(service_bp)
    
    return app
def gateway_app():

    app_gateway = Flask(__name__)
    app_gateway.config['SECRET_KEY'] = generate_secret_key()
    app_gateway.config['SQLALCHEMY_DATABASE_URI'] = sql_uri
    # Replace 'username', 'password', 'localhost', and 'dbname' with your PostgreSQL credentials
    app_gateway.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return app_gateway

app = client_app()
app.run(debug=True)

# from waitress import serve
# import subprocess

# if __name__ == '__main__':
#     # Command to run the first instance of Waitress serving the first Flask app on port 5000
#     command_app1 = ['waitress-serve', '--listen=127.0.0.1:5000', '--call', 'app:client_app']

#     # Command to run the second instance of Waitress serving the second Flask app on port 2000
#     command_app2 = ['waitress-serve', '--listen=127.0.0.1:2000', '--call', 'app:gateway_app']


#     # Start both instances of Waitress as separate processes
#     process_app1 = subprocess.Popen(command_app1)
#     process_app2 = subprocess.Popen(command_app2)

#     # Wait for both processes to finish
#     process_app1.wait()
#     process_app2.wait()


