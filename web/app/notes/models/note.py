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

from sqlalchemy import ForeignKey
from ...database import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    dal_id = db.Column(db.String(128))

    clinical_finding = db.Column(db.String(2048))
    presenting_complaint = db.Column(db.String(2048))

    treatment_narrative = db.Column(db.String(8096))

    discharge_diagnosis_1 = db.Column(db.String(1024))
    discharge_diagnosis_2 = db.Column(db.String(1024))

    allergy = db.Column(db.String(2048))

    checked = db.Column(db.Boolean(), default=False, nullable=False)

    codes = db.relationship(
        "NoteCode",
        uselist=True,
        primaryjoin="Note.id==NoteCode.note_id",
        viewonly=True
    )