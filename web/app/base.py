from sqlalchemy.ext.declarative import as_declarative, declared_attr
from .database import db
import uuid
from sqlalchemy.orm import validates

def generate_uuid():
    return str(uuid.uuid4()).upper()

@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.upper()
    
    @declared_attr
    def __mapper_args__(cls):
        return {"eager_defaults": True}

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    
    created_on = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now(), nullable=False)

    def update(self, values):
        for attr, values in values.items():
            setattr(self, attr, values)
        self.updated_on = db.func.now()