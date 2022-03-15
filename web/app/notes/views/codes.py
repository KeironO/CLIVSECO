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


from flask import url_for
import marshmallow_sqlalchemy as masql

from ...database import (
    NoteCode,
    AutoCode,
    Note,
    ClinicalCoderCode,
    NoteConfirmation,
)

from ...auth.views import UserAccountSchema

from ..enums import EnumCodedSection, EnumCodeType

from ...extensions import ma
from marshmallow_enum import EnumField
from marshmallow import fields
import requests


class BasicNoteSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = Note

    id = masql.auto_field()

class BasicNoteConfirmationSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteConfirmation

    user = ma.Nested(UserAccountSchema, many=False)


class NoteCodeSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteCode

    id = masql.auto_field()
    code = masql.auto_field()
    type = EnumField(EnumCodeType)
    note_id = masql.auto_field()

    note = ma.Nested(BasicNoteSchema, many=False)
    
    confirmations = ma.Nested(BasicNoteConfirmationSchema, many=True)

    code_information = fields.Method("retrieve_information")

    def retrieve_information(self, obj):
        code = obj.code
        if obj.type == "PROC":
            return requests.get(
                url_for("api.get_opcs_code", code=code, _external=True)
            ).json()["content"]
        else:
            # Remove Stop Code :-D
            if code.endswith("X"):
                code = code[:-1]
            return requests.get(
                url_for("api.get_icd_code", code=code, _external=True)
            ).json()["content"]




class AutoCodeSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = AutoCode

    id = masql.auto_field()
    start = masql.auto_field()
    end = masql.auto_field()
    section = EnumField(EnumCodedSection)

    confirmations = ma.Nested(BasicNoteConfirmationSchema, many=True)
    note_code = ma.Nested(NoteCodeSchema, many=False)

    _links = ma.Hyperlinks(
        {"feedback": ma.URLFor("notes.code_feedback", id="<id>", _external=True)}
    )


class ClinicalCoderSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = ClinicalCoderCode

    id = masql.auto_field()
    coded_by = masql.auto_field()
    code_number = masql.auto_field()

    note_code = ma.Nested(NoteCodeSchema, many=False)
