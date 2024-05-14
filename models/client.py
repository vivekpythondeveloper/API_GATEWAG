from db import db
from sqlalchemy import Table, MetaData, inspect, Index
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import defer
class Client(db.Model):
    __tablename__ = 'clients'
    client_id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(255), nullable=False)
    domain = db.Column(db.String(255), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    schema_assign = db.Column(db.String(255), unique=True, nullable=False)
    trial_start_date = db.Column(db.DateTime, nullable=True)
    trial_end_date = db.Column(db.DateTime, nullable=True)
    subscription_start_date = db.Column(db.DateTime, nullable=True)
    subscription_end_date = db.Column(db.DateTime, nullable=True)
    admin_email = db.Column(db.String(255), nullable=False)  # Added admin_email column

    # Indexes
    __table_args__ = (
        Index('ix_client_name', 'client_name'),
        Index('ix_domain', 'domain'),
        Index('ix_schema_assign', 'schema_assign'),
        Index('ix_admin_email', 'admin_email'),
    )

    def __repr__(self):
        return f"Client(client_name='{self.client_name}', domain='{self.domain}')"
    
    @classmethod
    def insert(cls, client_name, domain, schema_assign, admin_email,
                trial_start_date=None, trial_end_date=None,
                subscription_start_date=None, subscription_end_date=None):
        client = cls(client_name=client_name, domain=domain, schema_assign=schema_assign,
                        admin_email=admin_email,
                        trial_start_date=trial_start_date, trial_end_date=trial_end_date,
                        subscription_start_date=subscription_start_date, subscription_end_date=subscription_end_date)
        db.session.add(client)
        try:
            db.session.commit()
            return client
        except IntegrityError:
            db.session.rollback()
            return None

    @classmethod
    def dynamic_query(cls, filters):
        query = cls.query.options(defer('*'))
        for key, value in filters.items():
            if hasattr(cls, key):
                column = getattr(cls, key)
                query = query.filter(column == value)
        return query.all()
    
def create_client_table(schema_name='public'):
    # Create the table in the database
    inspector = inspect(db.engine)
    if not inspector.has_table('clients', schema=schema_name):
        Client.__table__.create(bind=db.engine)
    return Client
