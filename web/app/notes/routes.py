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


from flask import render_template, url_for
from flask_login import login_required

from . import notes

from sqlalchemy import func

from .models import Note

import requests


@notes.route("/", methods=["GET"])
@login_required
def home():
    note_count = Note.query.count()
    uncoded_count = Note.query.filter(Note.checked == False).count()
    return render_template(
        "notes/index.html", note_count=note_count, uncoded_count=uncoded_count
    )


@notes.route("/code")
@login_required
def code():
    response = requests.get(url_for("api.get_random_note", _external=True))

    if response.status_code == 200:
        note = response.json()
        return render_template("notes/view.html", note=note["content"])
    else:
        return response.content


@notes.route("/code/endpoint")
@login_required
def code_endpoint():
    response = requests.get(url_for("api.get_random_note", _external=True))
    return response.content
