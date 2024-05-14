from db import db
from sqlalchemy import Table, MetaData, inspect, DateTime, func, Index

class Service(db.Model):
    __tablename__ = 'services'
    service_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    protocol = db.Column(db.String(10), nullable=False)
    host = db.Column(db.String(255), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(255), nullable=False)
    enabled = db.Column(db.Boolean, default=True)
    tags = db.Column(db.Text, default=None)
    ca_certificates = db.Column(db.Text, default=None)
    write_timeout = db.Column(db.Integer, default=60000)
    connect_timeout = db.Column(db.Integer, default=60000)
    read_timeout = db.Column(db.Integer, default=60000)
    retries = db.Column(db.Integer, default=2)
    tls_verify = db.Column(db.Boolean, default=None)
    created_at = db.Column(DateTime, default=func.now())
    updated_at = db.Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"Service(name='{self.name}', host='{self.host}', port={self.port}, path='{self.path}')"
    
    @classmethod
    def insert(cls, name, protocol, host, port, path, **kwargs):
        new_service = cls(name=name, protocol=protocol, host=host, port=port, path=path, **kwargs)
        db.session.add(new_service)
        try:
            db.session.commit()
            return new_service
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def dynamic_query(cls, filters):
        query = cls.query
        for key, value in filters.items():
            if hasattr(cls, key):
                column = getattr(cls, key)
                query = query.filter(column == value)
        return query.all()
    
def service_model(schema_name):
    Service.__table__.schema = schema_name
    inspector = inspect(db.engine)
    if not inspector.has_table('services', schema=schema_name):
        # Add indexes
        Index('ix_name', Service.name)
        Service.__table__.create(bind=db.engine)

    return Service
