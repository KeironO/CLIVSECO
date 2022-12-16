from ..database import Base, db
from sqlalchemy import ForeignKey

class ResultsFeedback(Base):
    resultsid = db.Column(db.String(36), ForeignKey("AUTOCODERRESULTS.id"), nullable=False)
    nadex = db.Column(db.String(16), nullable=False)
    comments = db.Column(db.String(4096))
    iscorrect = db.Column(db.Boolean, default=False)
    remove = db.Column(db.Boolean, default=False)
    replace = db.Column(db.Boolean, default=False)

class ResultsFeedbackReplacementCode(Base):
    codeableconceptid = db.Column(db.String(36), ForeignKey("CODEABLECONCEPT.id"), nullable=False)
    # position = db.Column(db.Column(db.Integer))
    resultsfeedbackid = db.Column(db.String(36), ForeignKey("RESULTSFEEDBACK.id"), nullable=False)
    comments = db.Column(db.String(4096))
    nadex = db.Column(db.String(16), nullable=False)

class ResultsFeedbackNewCode(Base):
    codeableconceptid = db.Column(db.String(36), ForeignKey("CODEABLECONCEPT.id"), nullable=False)
    # position = db.Column(db.Column(db.Integer))
    resultsfeedbackid = db.Column(db.String(36), ForeignKey("RESULTSFEEDBACK.id"), nullable=False)
    comments = db.Column(db.String(4096))
    nadex = db.Column(db.String(16), nullable=False)