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


from ...api import api, db
from ...api.responses import (
    no_values_response,
    validation_error_response,
    success_with_content_response,
    transaction_error_response,
)


from ...database import Note

from ..views import NoteSchema


@api.route("/notes/random", methods=["GET"])
def get_random_dal_id():
    note = Note.query.filter(Note.checked == False).order_by(func.random()).first()
    return success_with_content_response({"dal_id": note.dal_id})

@api.route("/notes/get/<dal_id>", methods=["GET"])
def get_note(dal_id: str):
    note = Note.query.filter(Note.dal_id == dal_id).first()
    if note != None:
        return success_with_content_response(NoteSchema().dump(note))
    else:
        return {"success": False, "content" : {}}

@api.route("/notes/new", methods=["POST"])
def new_note():
    values = request.get_json()

    if not values:
        return no_values_response()

    try:
        note_result = NoteSchema(exclude=("id", "auto_codes", "clinical_coder_codes")).load(values)
    except ValidationError as err:
        return validation_error_response(err)

    new_note = Note(**note_result)

    try:
        db.session.add(new_note)
        db.session.commit()
        db.session.flush()
        return success_with_content_response(NoteSchema().dump(new_note))
    except Exception as err:
        return transaction_error_response(err)