from ...database import db, Base
from sqlalchemy import ForeignKey

class AutoCoderResults(Base):
    encounterid = db.Column(db.String(36), ForeignKey("ENCOUNTER.id"), nullable=False)
    codeableconceptid = db.Column(db.String(36), ForeignKey("CODEABLECONCEPT.id"), nullable=False)
    versioningid = db.Column(db.String(36), ForeignKey("VERSIONING.id"), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    issecondary = db.Column(db.Boolean, default=False)
    iscomorb = db.Column(db.Boolean, default=False)
    ispastmedicalhistory = db.Column(db.Boolean, default=False)
    isfamiliyhistory = db.Column(db.Boolean, default=False)
    isdaggerandasterik = db.Column(db.Boolean, default=False)
    isfromdiagnosis = db.Column(db.Boolean, default=False)
    sourcedocument = db.Column(db.String(128), nullable=False)
    sourcedocumentid = db.Column(db.String(128), nullable=False)
    sourcesection = db.Column(db.String(128), nullable=False)
    sentence = db.Column(db.Integer())
    start = db.Column(db.Integer())
    end = db.Column(db.Integer())