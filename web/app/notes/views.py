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

from ..database import (
    Note,
    NoteCode,
    OPCS4ChapterLookup,
    OPCS4SubChapterLookup,
    OPCS4CodeLookup,
)
from ..database import CodeFrom, CodeType
from ..database import ICD10Lookup
from ..extensions import ma
from marshmallow_enum import EnumField
from marshmallow import fields

import requests

class OPCS4ChapterLookupSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = OPCS4ChapterLookup

    id = masql.auto_field()
    chapter = masql.auto_field()
    heading = masql.auto_field()


class NewOPCS4ChapterLookupSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = OPCS4ChapterLookup

    chapter = masql.auto_field()
    heading = masql.auto_field()


class OPCS4SubChapterLookupSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = OPCS4SubChapterLookup

    id = masql.auto_field()
    subchapter = masql.auto_field()
    heading = masql.auto_field()
    chapter = ma.Nested(OPCS4ChapterLookupSchema, many=False)


class NewOPCS4SubChapterLookupSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = OPCS4SubChapterLookup

    subchapter = masql.auto_field()
    heading = masql.auto_field()
    chapter_id = masql.auto_field()


class OPCS4CodeLookupSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = OPCS4CodeLookup

    id = masql.auto_field()
    description = masql.auto_field()
    subchapter = ma.Nested(OPCS4SubChapterLookupSchema, many=False)


class NewOPCS4CodeLookupSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = OPCS4CodeLookup

    code = masql.auto_field()
    description = masql.auto_field()
    subchapter_id = masql.auto_field()


class ICD10CodeSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = ICD10Lookup

    code = masql.auto_field()
    description = masql.auto_field()
    billable = masql.auto_field()


class NoteCodeSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteCode

    id = masql.auto_field()

    cfrom = EnumField(CodeFrom, by_value=True)
    type = EnumField(CodeType, by_value=True)

    code = masql.auto_field()
    note_id = masql.auto_field()
    start = masql.auto_field()
    end = masql.auto_field()

    icd10_details = fields.Method("get_icd10_code")
    opcs4_details = fields.Method("get_opcs4_code")
    
    created_on = masql.auto_field()


    def get_icd10_code(self, obj):
        code = obj.code

        if code.endswith("X"):
            code = code[:-1]
        return requests.get(
            url_for("api.get_icd_code", code=code, _external=True)
        ).json()

    def get_opcs4_code(self, obj):
        code = obj.code

        return requests.get(
            url_for("api.get_opcs4_code", code=code, _external=True)
        ).json()

class NewNoteCodeSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteCode

    by = EnumField(CodedBy)
    cfrom = EnumField(CodeFrom, required=False)
    type = EnumField(CodeType)

    code = masql.auto_field()
    note_id = masql.auto_field()
    start = masql.auto_field(required=False)
    end = masql.auto_field(required=False)


class NoteSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = Note

    codes = ma.Nested(NoteCodeSchema, many=True)


class NewNoteSchema(masql.SQLAlchemySchema):
    class Meta:
        model = Note

    dal_id = masql.auto_field()
    clinical_finding = masql.auto_field()
    presenting_complaint = masql.auto_field()
    treatment_narrative = masql.auto_field()
    discharge_diagnosis_1 = masql.auto_field()
    discharge_diagnosis_2 = masql.auto_field()
    allergy = masql.auto_field()
    checked = masql.auto_field()
