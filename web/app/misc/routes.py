from . import misc
from flask import render_template

from ..database import db
from ..misc.models import Versioning, News

@misc.route("/test")
def test():

    v = Versioning()
    v.name = "Bad Luck Brian"
    from datetime import datetime
    v.rundatetime = datetime.now()
    v.changelog = "This is a testing Version purely for testing purposes."

    db.session.add(v)
    db.session.commit()

    return {"Test": True}

@misc.route("/news/<news_id>")
def news_item(news_id: str):
    news = db.session.query(News).filter(News.id==news_id).first_or_404()
    return render_template("/misc/newsitem.html", news=news)

@misc.route("/")
def homepage():
    return render_template("index.html")