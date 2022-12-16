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


from flask import render_template, url_for, flash, redirect, request, abort, g
from flask_login import login_required, current_user

from .. import encounter

from ..forms import AdditionalCodeForm

from sqlalchemy import func

from ..forms import FindForm, AuditorForm

import requests


@encounter.route("/code/random/<spec>")
def get_random_code(spec):

    response = requests.get(url_for("api.random_note", spec=spec, _external=True), verify=False)

    if response.status_code == 200:
        note = response.json()
        return redirect(
            url_for(
                "notes.code",
                caseno=note["content"]["caseno"],
                linkid=note["content"]["linkid"]
                )
            )
    else:
        return response.content


@encounter.route("/code/<caseno>:<linkid>", methods=["GET", "POST"])
@login_required
def code(caseno: str, linkid: str):
    response = requests.get(
        url_for(
            "api.get_note",
            caseno=caseno,
            linkid=linkid,
            _external=True
        ), verify=False)

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
                'user_id': str(current_user.username)
            }, verify=False)
            
            if submission_response.status_code == 200:
                flash("😀 Thank you for your feedback.")
            else:
                flash(response.content)
        return render_template("notes/view.html", note=note["content"], form=form, caseno=caseno, linkid=linkid)
    else:
        return response.content

@encounter.route("/code/<caseno>:<linkid>/audit", methods=["GET", "POST"])
@login_required
def audit(caseno, linkid): 
    response = requests.get(
        url_for(
            "api.get_note",
            caseno=caseno,
            linkid=linkid,
            _external=True
        ), verify=False)

    if response.status_code == 200:
        note = response.json()

        form = AuditorForm()

        if form.validate_on_submit():

            _json = {
                "note_id": note["content"]["id"],
                "procedures": form.procedures.data,
                "diagnoses": form.diagnosis.data,
                "caseno": caseno,
                "linkid": linkid,
                "coders_note": form.coders_note.data,
                "author": "AUTOCODER*%s" % (str(current_user.username))
            }

            audit_response = requests.post(url_for("api.submit_feedback", _external=True),
                json=_json, verify=False)
            
            if audit_response.status_code == 200:
                flash("The audit codes have been submitted. If you've made a mistake email Keiron.")
                return redirect(url_for('notes.code',caseno=caseno,linkid=linkid))


        return render_template(
            "notes/audit.html",
            note=note["content"],
            caseno=caseno,
            linkid=linkid,
            form=form
        )
    else:
        return response.content


@encounter.route("/get/<caseno>:<linkid>")
@login_required
def code_endpoint(caseno: str, linkid: str):
    response = requests.get(
        url_for(
            "api.get_note",
            caseno=caseno,
            linkid=linkid,
            _external=True
        ), verify=False)
    return response.json()


@encounter.route("/find/", methods=["GET", "POST"])
@login_required
def find_note():
    form = FindForm()
    found = []

    if form.validate_on_submit():
        
        _json = {"caseno": form.caseno.data}

        if form.linkid.data != None and len(form.linkid.data) > 1:
            _json["linkid"] = form.linkid.data

        response = requests.post(
            url_for("api.find_note", _external=True),
            verify=False,
            json=_json
        )


        if response.status_code == 200:
            if response.json()["success"]:
                found = response.json()["content"]

    return render_template("notes/find.html", form=form, found=found)
