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

from ...database import Note, ClinicLetter
from ...extensions import ma


from .codes import AutoCodeSchema, ClinicalCoderSchema
from .additional import AdditionalCodeSchema
from .audit import AuditResultsSchema

class ClinicLetterSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = ClinicLetter

    note_id = masql.auto_field()
    

class NoteSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = Note

    auto_codes = ma.Nested(AutoCodeSchema, many=True)
    clinical_coder_codes = ma.Nested(ClinicalCoderSchema, many=True)
    missing_codes = ma.Nested(AdditionalCodeSchema, many=True)
    clinic_letters = ma.Nested(ClinicLetterSchema, many=True)

    audit = ma.Nested(AuditResultsSchema, many=True)

    _links = ma.Hyperlinks(
        {
            
            "self": ma.URLFor("notes.code", caseno="<m_number>", linkid="<linkid>", _external=True)
        }
    )