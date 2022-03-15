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


from ...database import NoteConfirmation, AdditionalCode

from ..views import NoteConfirmationSchema, AdditionalCodeSchema


@api.route("/notes/feedback/autocode/get", methods=["GET"])
def get_autocode_feedback_all():
    confirmation = NoteConfirmation.query.all()
    return success_with_content_response(
        NoteConfirmationSchema(many=True).dump(confirmation)
    )


@api.route("/notes/feedback/additional_code/", methods=["POST"])
def add_additional_code():
    values = request.get_json()

    if not values:
        return no_values_response()

    try:
        additional_code_result = AdditionalCodeSchema(
            exclude=("id", "created_on")
        ).load(values)
    except ValidationError as err:
        return validation_error_response(err)

    new_additional_code = AdditionalCode(**additional_code_result)

    try:
        db.session.add(new_additional_code)
        db.session.commit()
        db.session.flush()
        return success_with_content_response(
            NoteConfirmationSchema().dump(new_additional_code)
        )
    except Exception as err:
        return transaction_error_response(err)

@api.route("/notes/feedback/autocode/", methods=["POST"])
def add_autocode_feedback():
    values = request.get_json()

    if not values:
        return no_values_response()

    try:
        autocode_feedback_result = NoteConfirmationSchema(
            exclude=("id", "created_on",)
        ).load(values)
    except ValidationError as err:
        return validation_error_response(err)

    new_code_confirmation = NoteConfirmation(**autocode_feedback_result)

    try:
        db.session.add(new_code_confirmation)
        db.session.commit()
        db.session.flush()
        return success_with_content_response(
            NoteConfirmationSchema().dump(new_code_confirmation)
        )
    except Exception as err:
        return transaction_error_response(err)
