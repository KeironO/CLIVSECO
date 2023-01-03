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

from ...globs import _spec_maps

@api.route("/notes/progress/<spec>", methods=["GET"])
def get_spec_progress(spec):
    spec_cov = _spec_maps[spec]
    notes = Note.query.filter(Note.checked == False, Note.admission_spec.in_(spec_cov)).all()

    fully_audited = []
    partially_audited = []
    not_audited = []

    for note in notes:
        has_been_audited = [len(x.note_code.confirmations) > 0 for x in note.auto_codes]

        if False not in has_been_audited:
            fully_audited.append("%s:%s" % (note.m_number, note.linkid))
        elif True not in has_been_audited:
            not_audited.append("%s:%s" % (note.m_number, note.linkid))
        else:
            partially_audited.append("%s:%s" % (note.m_number, note.linkid))


    return success_with_content_response({
        "counts": {
            "fully_audited": len(fully_audited),
            "partially_audited": len(partially_audited),
            "not_audited": len(not_audited)
        },
        "results": {
            "fully_audited": fully_audited,
            "partially_audited": partially_audited,
            "not_audited": not_audited
        }
    })


@api.route("/notes/random/<spec>", methods=["GET"])
def random_note(spec):
    spec_cov = _spec_maps[spec]
    notes = Note.query.filter(Note.checked == False, Note.admission_spec.in_(spec_cov)).order_by(func.random()).all()

    note = None
    if notes != [] and notes != None:
        for note in notes:
            already_audited = min([len(x.note_code.confirmations) for x in note.auto_codes])
            if already_audited == 0:
                return success_with_content_response({"caseno": note.m_number, "linkid": note.linkid})
    

        return {"success": False, "content": "No unaudited notes found?"}

    else:
        return {"success": False, "content": "No unaudited notes found?"}

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
