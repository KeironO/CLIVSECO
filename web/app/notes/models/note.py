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
from enum import Enum


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    spec_name = db.Column(db.String(128), nullable=True)
    dal_id = db.Column(db.String(128))

    clinical_finding = db.Column(db.String(2048))
    presenting_complaint = db.Column(db.String(2048))
    treatment_narrative = db.Column(db.String(8096))
    discharge_diagnoses = db.Column(db.String(1024))
    allergy = db.Column(db.String(2048))
    checked = db.Column(db.Boolean(), default=False, nullable=False)

    admission_date = db.Column(db.Date, nullable=True)
    discharge_date = db.Column(db.Date, nullable=True)

    dob = db.Column(db.Date, nullable=True)

    missing_codes = db.relationship(
        "AdditionalCode",
        uselist=True,
        primaryjoin="Note.id==AdditionalCode.note_id"
    )

    auto_codes = db.relationship(
        "AutoCode",
        uselist=True,
        secondary="note_code",
        primaryjoin="Note.id==NoteCode.note_id",
        secondaryjoin="NoteCode.id==AutoCode.note_code_id",
        viewonly=True,
    )

    clinical_coder_codes = db.relationship(
        "ClinicalCoderCode",
        uselist=True,
        secondary="note_code",
        primaryjoin="Note.id==NoteCode.note_id",
        secondaryjoin="NoteCode.id==ClinicalCoderCode.note_code_id",
        viewonly=True,
    )

    clinic_letters = db.relationship(
        "ClinicLetter",
        uselist=True,
        primaryjoin="Note.id==ClinicLetter.note_id"
    )


class ClinicLetter(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_id = db.Column(db.Integer, ForeignKey("note.id"), nullable=False)
    letter_key = db.Column(db.String(128))
    letter_contents = db.Column(db.String(256000))
    creation_date = db.Column(db.Date, nullable=False)