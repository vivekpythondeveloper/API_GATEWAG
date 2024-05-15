from db import db
from sqlalchemy import Table, MetaData, inspect, DateTime, func, Index, JSON,cast, String

class Endpoint(db.Model):
    __tablename__ = 'endpoints'
    endpoint_id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), default=None)  # Assuming 'name' corresponds to 'name' in the JSON
    protocols = db.Column(db.JSON, default=[
                                            "http",
                                            "https"
                                            ])  # Store as JSON array
    snis = db.Column(db.JSON, default=None)  # Store as JSON array
    path_handling = db.Column(db.String(10), default="v0")  # Assuming 'path_handling' is a string
    tags = db.Column(db.JSON, default=None)  # Store as JSON array
    paths = db.Column(db.JSON)  # Store as JSON array
    created_at = db.Column(DateTime, default=func.now())  # Assuming 'created_at' is an integer timestamp
    strip_path = db.Column(db.Boolean, default=True)  # Assuming 'strip_path' is a boolean
    sources = db.Column(db.JSON, default=None)  # Store as JSON array
    regex_priority = db.Column(db.Integer, default=0)  # Assuming 'regex_priority' is an integer
    hosts = db.Column(db.JSON, default=None)  # Store as JSON array
    destinations = db.Column(db.JSON, default=None)  # Store as JSON array
    methods = db.Column(db.JSON, default=None)  # Store as JSON array
    headers = db.Column(db.JSON, default=None)  # Store as JSON array
    updated_at = db.Column(DateTime, default=func.now())  # Assuming 'updated_at' is an integer timestamp
    https_redirect_status_code = db.Column(db.Integer, default=426)  # Assuming 'https_redirect_status_code' is an integer
    preserve_host = db.Column(db.Boolean, default=False)  # Assuming 'preserve_host' is a boolean
    request_buffering = db.Column(db.Boolean, default=True)  # Assuming 'request_buffering' is a boolean
    response_buffering = db.Column(db.Boolean, default=True)  # Assuming 'response_buffering' is a boolean
    # Add more generic fields as needed

    

    def __repr__(self):
        return f"Endpoint(url='{self.url}', http_method='{self.http_method}')"
    
    @classmethod
    def insert(cls, data):
        instance = cls(**data)
        db.session.add(instance)
        db.session.commit()
        return instance.as_dict()
    
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    

    @classmethod
    def dynamic_query(cls, filters):
        query = cls.query
        print(f"This is filter: {filters}")
        for key, value in filters.items():
            if hasattr(cls, key):
                column = getattr(cls, key)
                if isinstance(column.property.columns[0].type, JSON):
                    # If column is JSON, handle filtering differently
                    if isinstance(value, dict):
                        # If value is a dictionary, iterate over its items for filtering
                        for json_key, json_value in value.items():
                            query = query.filter(func.json_extract_path_text(column, json_key) == json_value)
                    elif isinstance(value, str):
                        # If value is a string, check if it exists in the JSON array using ANY operator
                        query = query.filter(cast(column, String).contains(value))
                    else:
                        # Handle other types as needed
                        pass
                else:
                    # For non-JSON columns, apply regular filtering
                    query = query.filter(column == value)
        return query.all()


    
def endpoint_model(schema_name):
    
    # Set the schema for the table
    Endpoint.__table__.schema = schema_name
    inspector = inspect(db.engine)
    if not inspector.has_table('endpoints', schema=schema_name):
        # Add indexes
        Index('ix_service_id', Endpoint.service_id)
        Endpoint.__table__.create(bind=db.engine)

    return Endpoint

