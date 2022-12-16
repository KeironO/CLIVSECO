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

from ...database import AuditResults

class AuditResultsSchema(masql.SQLAlchemyAutoSchema):
    class Meta:
        model = AuditResults

    id = masql.auto_field()

    note_id = masql.auto_field()

    caseno = masql.auto_field()
    linkid = masql.auto_field()

    diagnoses = masql.auto_field()
    procedures= masql.auto_field()

    coders_note=masql.auto_field()
    author=masql.auto_field()
    created_on = masql.auto_field()