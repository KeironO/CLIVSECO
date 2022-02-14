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
    ClinicalCoderCode,
    EnumCodedSection,
    EnumCodeType
)

from ...extensions import ma
from marshmallow_enum import EnumField
from marshmallow import fields

class NoteCodeSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteCode

    code = masql.auto_field()
    type = EnumField(EnumCodeType)
    note_id = masql.auto_field()

class AutoCodeSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = AutoCode
    
    id = masql.auto_field()
    start = masql.auto_field()
    end = masql.auto_field()
    section = EnumField(EnumCodedSection)

    note_code = ma.Nested(NoteCodeSchema, many=False)


class ClinicalCoderSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = ClinicalCoderCode
    
    id = masql.auto_field()
    coded_by = masql.auto_field()
    note_code = ma.Nested(NoteCodeSchema, many=False)


