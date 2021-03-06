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
    OPCS4ChapterLookup,
    OPCS4SubChapterLookup,
    OPCS4CodeLookup,
)

from .views import (
    ICD10CodeSchema,
    NewOPCS4ChapterLookupSchema,
    OPCS4ChapterLookupSchema,
    NewOPCS4SubChapterLookupSchema,
    OPCS4SubChapterLookupSchema,
    NewOPCS4CodeLookupSchema,
    OPCS4CodeLookupSchema,
)


@api.route("/code/OPCS4/<code>", methods=["GET"])
def get_opcs_code(code: str):
    if len(code) == 3:
        code = OPCS4SubChapterLookup.query.filter(OPCS4SubChapterLookup.subchapter == code).first()
        return success_with_content_response(OPCS4SubChapterLookupSchema().dump(code))
    elif len(code) > 3:
        code = OPCS4CodeLookup.query.filter(OPCS4CodeLookup.code == code).first()
        return success_with_content_response(OPCS4CodeLookupSchema().dump(code))


@api.route("/code/ICD10/<code>", methods=["GET"])
def get_icd_code(code: str):
    code = ICD10Lookup.query.filter(ICD10Lookup.code == code).first()
    return success_with_content_response(ICD10CodeSchema().dump(code))


@api.route("/opcs4/add/subchapter", methods=["POST"])
def opcs_subchapter():
    values = request.get_json()

    if not values:
        return no_values_response()

    try:
        new_subchapter_result = NewOPCS4SubChapterLookupSchema().load(values)
    except ValidationError as err:
        return validation_error_response(err)

    new_subchapter = OPCS4SubChapterLookup(**new_subchapter_result)

    try:
        db.session.add(new_subchapter)
        db.session.commit()
        db.session.flush()
        return success_with_content_response(
            OPCS4SubChapterLookupSchema().dump(new_subchapter)
        )
    except Exception as err:
        return transaction_error_response(err)


@api.route("/opcs4/add/chapter", methods=["POST"])
def add_opcs_chapter():
    values = request.get_json()

    if not values:
        return no_values_response()

    try:
        new_chapter_result = NewOPCS4ChapterLookupSchema().load(values)
    except ValidationError as err:
        return validation_error_response(err)

    new_chapter = OPCS4ChapterLookup(**new_chapter_result)

    try:
        db.session.add(new_chapter)
        db.session.commit()
        db.session.flush()
        return OPCS4ChapterLookupSchema().dump(new_chapter)
    except Exception as err:
        return transaction_error_response(err)


@api.route("/opcs4/add/code", methods=["POST"])
def add_opcs_code():
    values = request.get_json()

    if not values:
        return no_values_response()

    try:
        new_code_result = NewOPCS4CodeLookupSchema().load(values)
    except ValidationError as err:
        return validation_error_response(err)

    new_code = OPCS4CodeLookup(**new_code_result)

    try:
        db.session.add(new_code)
        db.session.commit()
        db.session.flush()
        return OPCS4CodeLookupSchema().dump(new_code)
    except Exception as err:
        return transaction_error_response(err)
