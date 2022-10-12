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

from ..api import api, db
from ..api.responses import (
    validation_error_response,
    no_values_response,
    transaction_error_response,
    success_with_content_response,
)

from ..database import (
    ICD10Lookup,
    OPCS4Lookup,
)

from .views import (
    ICD10CodeSchema,
    OPCS4CodeSchema
)


@api.route("/code/OPCS4/<code>", methods=["GET"])
def get_opcs_code(code: str):
    code = OPCS4Lookup.query.filter(OPCS4Lookup.code == code).first()
    return success_with_content_response(OPCS4CodeSchema().dump(code))


@api.route("/code/ICD10/<code>", methods=["GET"])
def get_icd_code(code: str):
    code = ICD10Lookup.query.filter(ICD10Lookup.code == code).first()
    return success_with_content_response(ICD10CodeSchema().dump(code))



@api.route("/code/opcs4/add/", methods=["POST"])
def add_opcs_code():
    values = request.get_json()

    if not values:
        return no_values_response()
    try:
        new_code_result = OPCS4CodeSchema(exclude=("id", )).load(values)
    except ValidationError as err:
        return validation_error_response(err)

    new_code = OPCS4Lookup(**new_code_result)

    try:
        db.session.add(new_code)
        db.session.commit()
        db.session.flush()
        return OPCS4CodeSchema().dump(new_code)
    except Exception as err:
        return transaction_error_response(err)
