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

import marshmallow_sqlalchemy as masql
from ..extensions import ma
from marshmallow_enum import EnumField
from marshmallow import fields

from ..database import (
    OPCS4ChapterLookup,
    OPCS4SubChapterLookup,
    OPCS4CodeLookup,
    ICD10Lookup
)



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


