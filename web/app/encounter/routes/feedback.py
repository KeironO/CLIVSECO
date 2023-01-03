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

from flask import render_template, url_for, flash, request, redirect, request
from flask_login import login_required, current_user

from .. import encounter

from ..forms import FeedbackForm, DeleteFeedbackForm

import requests


@encounter.route("/code/feedback/<id>", methods=["GET", "POST"])
@login_required
def code_feedback(id: int):
    form = FeedbackForm()

    code = requests.get(url_for("api.get_autocode", id=id, _external=True), verify=False)
    
    if code.status_code == 200:

        if form.validate_on_submit():
            
            response = requests.post(
                url_for("api.add_autocode_feedback", _external=True),
                json={
                    "note_code_id": code.json()["content"]["note_code"]["id"],
                    "comments": form.comments.data,
                    "replace_with": request.form['replace_with_input'],
                    "is_correct": form.is_correct.data,
                    "additional_codes": request.form['additional_codes_input'],
                    "user_id": (current_user.username),
                }, verify=False
            )

            if response.status_code == 200:
                flash("Thank you for providing feedback 😊")
                return redirect(request.referrer)
            else:
                return response.content

        return render_template("encounter/feedback/view.html", form=form, id=id)
    else:
        return code.status_code

@encounter.route("/code/feedback/<id>/endpoint")
@login_required
def code_feedback_endpoint(id: int):
    return requests.get(url_for("api.get_autocode", id=id, _external=True), verify=False).json()




@encounter.route("/feedback")
@login_required
def code_feedback_index():
    return render_template("encounter/feedback/index.html")


@encounter.route("/code/feedback/<id>/delete", methods=["GET", "POST"])
@login_required
def code_feedback_delete(id):
    form = DeleteFeedbackForm()
    if form.validate_on_submit():
        response = requests.post(url_for("api.delete_autocode_feedback", id=id, _external=True), json={'user_id': str(current_user.username)}, verify=False)
        if response.status_code == 200:
            flash("Deleted Feedback %s " % (response.content))
            return redirect(url_for("notes.code_feedback_index"))
        else:
            flash(response.content)
    return render_template("encounter/feedback/delete.html", form=form, id=id)

@encounter.route("/feedback/endpoint")
@login_required
def code_feedback_index_endpoint():
    return requests.get(url_for("api.get_autocode_feedback_all", _external=True), verify=False).json()

