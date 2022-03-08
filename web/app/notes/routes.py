# Copyright (C) 2022  Keiron O'Shea <keiron.oshea@wales.nhs.uk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from flask import render_template, url_for, flash, redirect
from flask_login import login_required, current_user

from . import notes

from sqlalchemy import func

from .models import Note
from .forms import FeedbackForm, FindForm

import requests


@notes.route("/", methods=["GET"])
@login_required
def home():
    note_count = Note.query.count()
    uncoded_count = Note.query.filter(Note.checked == False).count()
    return render_template(
        "notes/index.html", note_count=note_count, uncoded_count=uncoded_count
    )


@notes.route("/code/")
@login_required
def code():
    response = requests.get(url_for("api.get_random_note", _external=True))

    if response.status_code == 200:
        note = response.json()
        return render_template("notes/view.html", note=note["content"])
    else:
        return response.content

@notes.route("/code/<dal_id>")
def code_by_id(dal_id: str):
    response = requests.get(url_for("api.get_note", dal_id=dal_id, _external=True))

    if response.status_code == 200:
        note = response.json()
        return render_template("notes/view.html", note=note["content"])
    else:
        return response.content


@notes.route("/get/<dal_id>")
@login_required
def code_endpoint(dal_id: str):
    response = requests.get(url_for("api.get_note", dal_id=dal_id, _external=True))
    return response.json()


@notes.route("/find/", methods=["GET", "POST"])
@login_required
def find_note():
    form = FindForm()

    if form.validate_on_submit():
        response = requests.get(url_for("api.get_note", dal_id=form.dal.data, _external=True))

        if response.status_code == 200 and response.json()["success"]:
            return redirect(url_for("notes.code_by_id", dal_id=form.dal.data))
        else:
            flash("%s not found, are you sure it's a valid DAL ID?" % (form.dal.data))

    return render_template("notes/find.html", form=form)



@notes.route("/code/feedback/<id>", methods=["GET", "POST"])
@login_required
def code_feedback(id: int):
    form = FeedbackForm()

    if form.validate_on_submit():

        
        response = requests.post(
            url_for("api.add_autocode_feedback", _external=True),
            json = {
            "note_code_id": id,
            "comments": form.comments.data,
            "replace_with": form.replace_with.data,
            "is_correct": form.is_correct.data,
            "user_id": current_user.id
            }
        )

        if response.status_code == 200:
            flash("Thank you for providing feedback 😊")
            return redirect(url_for("notes.home"))
        return response.content

    
    return render_template("notes/feedback/feedback.html", form=form, id=id)

@notes.route("/feedback")
@login_required
def code_feedback_index():
    return render_template("notes/feedback/index.html")

@notes.route("/feedback/endpoint")
@login_required
def code_feedback_index_endpoint():
    return requests.get(url_for("api.get_autocode_feedback_all", _external=True)).json()

@notes.route("/code/feedback/<id>/endpoint")
@login_required
def code_feedback_endpoint(id: int):
    return requests.get(url_for("api.get_autocode", id=id, _external=True)).json()