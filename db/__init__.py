from flask_sqlalchemy import SQLAlchemy

sql_uri = 'postgresql://postgres:root@localhost:5433/api_gateway'

db = SQLAlchemy()
