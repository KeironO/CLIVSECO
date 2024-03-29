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

from ...database import AdditionalCode



from ...extensions import ma
from ..enums import EnumCodedSection, EnumCodeType
from marshmallow_enum import EnumField

class AdditionalCodeSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = AdditionalCode

    id = masql.auto_field()
    note_id = masql.auto_field()
    section = EnumField(EnumCodedSection)
    type = EnumField(EnumCodeType)
    start = masql.auto_field()
    end = masql.auto_field()
    code = masql.auto_field()
    comorbidity = masql.auto_field()
    user_id = masql.auto_field()
    created_on = masql.auto_field()