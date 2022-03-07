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
from sqlalchemy import ForeignKey
from ...database import db
from enum import Enum
from marshmallow import fields

class EnumCodedSection(Enum):
    CLI = "Clinical Finding"
    PRE = "Presenting Complaint"
    TRE = "Treatment Narrative"
    DIA = "Discharge Diagnoses"
    ALL = "Allergy"


class EnumCodeType(Enum):
    PROC = "Procedure"
    DIAG = "Diagnosis"


class NoteCode(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(7), nullable=False)
    note_id = db.Column(db.Integer, ForeignKey("note.id"), nullable=False)
    type = db.Column(db.Enum(EnumCodeType), nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    


class AutoCode(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    section = db.Column(db.Enum(EnumCodedSection))
    note_code_id = db.Column(db.Integer, ForeignKey(NoteCode.id), nullable=False)
    comorbidity = db.Column(db.Boolean, default=False, nullable=False)
    note_code = db.relationship(
        "NoteCode", uselist=False, primaryjoin="AutoCode.note_code_id == NoteCode.id"
    )


class ClinicalCoderCode(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coded_by = db.Column(db.String(15))
    note_code_id = db.Column(db.Integer, ForeignKey(NoteCode.id), nullable=False)

    # d01, d02, d03
    code_number = db.Column(db.Integer, nullable=False)

    note_code = db.relationship(
        "NoteCode",
        uselist=False,
        primaryjoin="ClinicalCoderCode.note_code_id == NoteCode.id",
    )
