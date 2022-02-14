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

from flask import request
from marshmallow import ValidationError
from sqlalchemy import func

from ..api import api, db
from ..api.responses import (
    no_values_response,
    validation_error_response,
    success_with_content_response
)

from ..database import (
    Note,
    NoteCode
)

from .views import (
    NoteSchema,
    NewNoteSchema,
    NewNoteCodeSchema,
    NoteCodeSchema,
)



@api.route("/notes/get", methods=["GET"])
def get_random_note():
    note = Note.query.filter(Note.checked == False).order_by(func.random()).first()
    return success_with_content_response(NoteSchema().dump(note))

@api.route("/notes/add", methods=["POST"])
def add_note():
    values = request.get_json()

    if not values:
        return no_values_response()

    try:
        note_result = NewNoteSchema().load(values)
    except ValidationError as err:
        return validation_error_response(err)

    new_note = Note(**note_result)

    try:
        db.session.add(new_note)
        db.session.commit()
        db.session.flush()
        return NoteSchema().dump(new_note)
    except Exception as err:
        return (
            {"success": False, "message": str(err.orig.diag.message_primary)},
            417,
            {"ContentType": "application/json"},
        )


@api.route("notes/code/add/icd/", methods=["POST"])
def add_icd():
    values = request.get_json()

    if not values:
        return (
            {"success": False, "message": "No input data provided"},
            400,
            {"ContentType": "application/json"},
        )

    try:
        new_code_result = NewNoteCodeSchema().load(values)
    except ValidationError as err:
        return validation_error_response(err)

    new_code = NoteCode(**new_code_result)

    try:
        db.session.add(new_code)
        db.session.commit()
        db.session.flush()
        return NoteCodeSchema().dump(new_code)
    except Exception as err:
        return (
            {"success": False, "message": str(err)},
            417,
            {"ContentType": "application/json"},
        )