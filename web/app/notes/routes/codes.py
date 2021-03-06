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


from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user

from .. import notes

from ..forms import AdditionalCodeForm

from sqlalchemy import func

from ..forms import FindForm

import requests


@notes.route("/code/")
@login_required
def get_random_code():
    response = requests.get(url_for("api.get_random_dal_id", _external=True))

    if response.status_code == 200:
        note = response.json()
        return redirect(url_for("notes.code", dal_id=note["content"]["dal_id"]))
    else:
        return response.content


@notes.route("/code/<dal_id>", methods=["GET", "POST"])
@login_required
def code(dal_id: str):
    response = requests.get(url_for("api.get_note", dal_id=dal_id, _external=True))

    if response.status_code == 200:
        note = response.json()
        form = AdditionalCodeForm()
        if form.validate_on_submit():
            
            submission_response = requests.post(url_for("api.add_additional_code", _external=True),
                json={
                'note_id': note["content"]["id"],
                'section': form.section.data,
                'type': form.type.data,
                'start': int(form.start.data),
                'end': int(form.end.data),
                'code': request.form['additional_codes_input'],
                'comorbidity': form.comorbidity.data,
                'user_id': current_user.id
            })
            
            if submission_response.status_code == 200:
                flash("???? Thank you for your feedback.")
            else:
                flash(response.content)
        return render_template("notes/view.html", note=note["content"], form=form)
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
        response = requests.get(
            url_for("api.get_note", dal_id=form.dal.data, _external=True)
        )

        if response.status_code == 200 and response.json()["success"]:
            return redirect(url_for("notes.code", dal_id=form.dal.data))
        else:
            flash("%s not found, are you sure it's a valid DAL ID?" % (form.dal.data))

    return render_template("notes/find.html", form=form)
