from db import db
from sqlalchemy import Table, MetaData, inspect, DateTime, func, Index
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    org_name = db.Column(db.String(100))
    org_id = db.Column(db.Integer)
    # Add more generic fields as needed
    create_date = db.Column(DateTime, default=func.now())
    update_date = db.Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"User(username='{self.username}', email='{self.email}')"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def insert(cls, username, email, password, org_name=None, org_id=None):
        new_user = cls(
            username=username,
            email=email,
            org_name=org_name,
            org_id=org_id
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        try:
            db.session.commit()
            return new_user
        except IntegrityError:
            db.session.rollback()
            return None
    
    @classmethod
    def dynamic_query(cls, filters):
        query = cls.query
        for key, value in filters.items():
            if hasattr(cls, key):
                column = getattr(cls, key)
                query = query.filter(column == value)
        return query.all()

def user_model(schema_name):
    

    # Set the schema for the table
    User.__table__.schema = schema_name

    
    inspector = inspect(db.engine)
    if not inspector.has_table('users', schema=schema_name):
        # Add indexes
        Index('ix_username', User.username)
        Index('ix_email', User.email)
        Index('ix_org_name', User.org_name)
        Index('ix_org_id', User.org_id)
        User.__table__.create(bind=db.engine)
        
    return User