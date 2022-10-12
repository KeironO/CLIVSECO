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


from ...database import Note, ClinicLetter

from ..views import NoteSchema, ClinicLetterSchema


@api.route("/notes/random", methods=["GET"])
def random_note():
    note = Note.query.filter(Note.checked == False).order_by(func.random()).first()
    
    if note != None:
        return success_with_content_response({"caseno": note.m_number, "linkid": note.linkid})
    return {"success": False, "content": "No Notes Found found?"}

@api.route("/notes/mark/<caseno>:<linkid>")
def mark_as_complete(caseno, linkid):
    note = Note.query.filter(Note.m_number == caseno, Note.linkid == linkid).order_by(func.random()).first()

    if note != None:
        note.checked = True
        db.session.add(note)
        db.session.commit()
        db.session.flush()
        return success_with_content_response(NoteSchema(many=True).dump(note))
    else:
        return {"success": False, "content": {"error": "Note not found"}}

@api.route("/notes/find/", methods=["POST"])
def find_note():
    values = request.get_json()

    if not values:
        return no_values_response()

    if 'caseno' not in values:
        return {"success": False, "content": {"error": "We require caseno"}}

    caseno = values["caseno"]

    if "linkid" in values:
        linkid = values["linkid"]
        note = Note.query.filter(Note.linkid==linkid, Note.m_number==caseno).all()
    else:
        note = Note.query.filter(Note.m_number==caseno).all()

    if note != None:
        return success_with_content_response(NoteSchema(many=True).dump(note))
    else:
        return {"success": False, "content": {}}

@api.route("/notes/get/<caseno>:<linkid>", methods=["GET"])
def get_note(caseno: str, linkid: str):
    note = Note.query.filter(Note.m_number==caseno,Note.linkid==linkid).first()
    if note != None:
        return success_with_content_response(NoteSchema().dump(note))
    else:
        return {"success": False, "content": {}}

@api.route("/notes/new_letter", methods=["POST"])
def add_letter():
    values = request.get_json()

    if not values:
        return no_values_response()
    
    try:
        letter_result = ClinicLetterSchema(
            exclude=("id", )
        ).load(values)
    except ValidationError as err:
        return validation_error_response(err)

    new_letter = ClinicLetter(**letter_result)

    try:
        db.session.add(new_letter)
        db.session.commit()
        db.session.flush()
        return success_with_content_response(ClinicLetterSchema().dump(new_letter))
    except Exception as err:
        return transaction_error_response(err)

@api.route("/notes/new", methods=["POST"])
def new_note():
    values = request.get_json()

    if not values:
        return no_values_response()

    try:
        note_result = NoteSchema(
            exclude=("id", "auto_codes", "clinical_coder_codes")
        ).load(values)
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
