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


from ...database import AutoCode, NoteCode, ClinicalCoderCode

from ..views import AutoCodeSchema, ClinicalCoderSchema



@api.route("/notes/get/autocode/<id>", methods=["GET"])
def get_autocode(id):
    autocode = AutoCode.query.filter_by(id=id).first()
    return success_with_content_response(
        AutoCodeSchema().dump(autocode)
    )




@api.route("/notes/add/autocode", methods=["POST"])
def add_autocode():
    values = request.get_json()

    if not values:
        return no_values_response()

    try:
        autocode_result = AutoCodeSchema(exclude=("id",)).load(values)
    except ValidationError as err:
        return validation_error_response(err)

    new_note_code = NoteCode(**autocode_result["note_code"])

    try:
        db.session.add(new_note_code)
        db.session.commit()
        db.session.flush()
    except Exception as err:
        return transaction_error_response(err)

    del autocode_result["note_code"]

    new_auto_code = AutoCode(**autocode_result)
    new_auto_code.note_code_id = new_note_code.id

    try:
        db.session.add(new_auto_code)
        db.session.commit()
        db.session.flush()
        return success_with_content_response(AutoCodeSchema().dump(new_auto_code))
    except Exception as err:
        return transaction_error_response(err)


@api.route("/notes/add/clinicalcode", methods=["POST"])
def add_clinicalcode():
    values = request.get_json()

    if not values:
        return no_values_response()

    try:
        clinical_code_result = ClinicalCoderSchema(exclude=("id",)).load(values)
    except ValidationError as err:
        return validation_error_response(err)

    new_note_code = NoteCode(**clinical_code_result["note_code"])

    try:
        db.session.add(new_note_code)
        db.session.commit()
        db.session.flush()
    except Exception as err:
        return transaction_error_response(err)

    del clinical_code_result["note_code"]

    new_clinical_code = ClinicalCoderCode(**clinical_code_result)
    new_clinical_code.note_code_id = new_note_code.id

    try:
        db.session.add(new_clinical_code)
        db.session.commit()
        db.session.flush()
        return success_with_content_response(
            ClinicalCoderSchema().dump(new_clinical_code)
        )
    except Exception as err:
        return transaction_error_response(err)
