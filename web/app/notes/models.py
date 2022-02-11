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
from ..database import db
from enum import Enum


class CodeFrom(Enum):
    CLI = "Clinical Finding"
    PRE = "Presenting Complaint"
    TRE = "Treatment Narrative"
    DIA = "Diagnoses"
    ALL = "Allergy"


class CodeType(Enum):
    PROC = "Procedure"
    DIAG = "Diagnosis"


class CodedBy(Enum):
    CODER = "Clinical Coder"
    AUTO = "AutoCoder"


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
        "NoteCode", uselist=True, primaryjoin="Note.id==NoteCode.note_id", viewonly=True
    )


class NoteCode(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(7), nullable=False)
    note_id = db.Column(db.Integer, ForeignKey("note.id"), nullable=False)
    type = db.Column(db.Enum(CodeType), nullable=False)
    by = db.Column(db.Enum(CodedBy), nullable=False)
    cfrom = db.Column(db.Enum(CodeFrom))
    # Only populated from auto-coder :-D
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)


class NoteConfirmation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_code_id = db.Column(db.Integer, ForeignKey("note_code.id"), nullable=False)
    is_correct = db.Column(db.Boolean, default=True)
    comments = db.Column(db.String(2048), nullable=True)
    replace_with = db.Column(db.String(7), nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("user_account.id"), nullable=False)


class ICD10Lookup(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(7))
    description = db.Column(db.String(256))
    billable = db.Column(db.Boolean)


class OPCS4ChapterLookup(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chapter = db.Column(db.String(8), unique=True)
    heading = db.Column(db.String(256))


class OPCS4SubChapterLookup(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subchapter = db.Column(db.String(8), unique=True)
    heading = db.Column(db.String(256))
    chapter_id = db.Column(
        db.Integer, ForeignKey(OPCS4ChapterLookup.id), nullable=False
    )

    chapter = db.relationship(
        "OPCS4ChapterLookup",
        uselist=False,
        primaryjoin="OPCS4ChapterLookup.id==OPCS4SubChapterLookup.chapter_id",
        viewonly=True,
    )


class OPCS4CodeLookup(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(8))
    description = db.Column(db.String(256))
    subchapter_id = db.Column(
        db.Integer, ForeignKey(OPCS4SubChapterLookup.id), nullable=False
    )

    subchapter = db.relationship(
        "OPCS4SubChapterLookup",
        uselist=False,
        primaryjoin="OPCS4SubChapterLookup.id==OPCS4CodeLookup.subchapter_id",
        viewonly=True,
    )
