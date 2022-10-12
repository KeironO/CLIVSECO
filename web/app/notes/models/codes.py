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
from marshmallow import fields

from ..enums import EnumCodedSection, EnumCodeType

class NoteCode(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(7), nullable=False)
    note_id = db.Column(db.Integer, ForeignKey("note.id"), nullable=False)
    type = db.Column(db.Enum(EnumCodeType), nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    confirmations = db.relationship("NoteConfirmation", primaryjoin="NoteCode.id == NoteConfirmation.note_code_id")
    note = db.relationship("Note", primaryjoin="Note.id == NoteCode.note_id")


class AutoCode(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_code_id = db.Column(db.Integer, ForeignKey(NoteCode.id), nullable=False)
    note_code = db.relationship(
        "NoteCode",
        uselist=False,
        primaryjoin="AutoCode.note_code_id == NoteCode.id",
    )
    
    # start - Starting position of text where the code was taken
    # end - End position of text where the code was taken
    # section - The section in which the code was taken
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    section = db.Column(db.Enum(EnumCodedSection))
    # position - Where the code is placed
    # source_id - Taken from SOURCEID from [_Sandbox_General].[dbo].[TbAutoCodedDALs]
    # source - Taken from SOURCE from [_Sandbox_General].[dbo].[TbAutoCodedDALs]
    position = db.Column(db.Integer)
    source_id = db.Column(db.String(1024))
    source = db.Column(db.String(2048), nullable=False)
    # comorbidity - Where the code has been taken forward via a comorb
    # pmh - Whether the diagnosis has been noted as a 'past medical history'
    # sec - Whether the code is a secondary modifier or not
    # acr - Developed from a deycphered acronym
    # dia - Whether the code is a diagnosis
    # fmh - Whether the code is a family history of
    # daa - Whether the code is a dagger and asterix modified code
    comorbidity = db.Column(db.Boolean, default=False, nullable=False)
    pmh = db.Column(db.Boolean, default=False, nullable=False)
    sec = db.Column(db.Boolean, default=False, nullable=False)
    acr = db.Column(db.Boolean, default=False, nullable=False)
    dia = db.Column(db.Boolean, default=False, nullable=False)
    fmh = db.Column(db.Boolean, default=False, nullable=False)
    daa = db.Column(db.Boolean, default=False, nullable=False)


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
