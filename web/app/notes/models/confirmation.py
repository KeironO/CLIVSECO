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
from ..enums import EnumCodeType, EnumCodedSection

from .codes import NoteCode
from .note import Note

class AuditResults(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_id = db.Column(db.Integer, ForeignKey('note.id'), nullable=False)
    caseno = db.Column(db.String(64))
    linkid = db.Column(db.String(64))
    diagnoses = db.Column(db.String(2048))
    procedures = db.Column(db.String(2048))
    coders_note = db.Column(db.String(4096))
    author = db.Column(db.String(64))
    created_on = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    note = db.relationship(Note)


class NoteConfirmation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_code_id = db.Column(db.Integer, ForeignKey("note_code.id"), nullable=False)
    is_correct = db.Column(db.Boolean, default=True)
    comments = db.Column(db.String(2048), nullable=True)
    replace_with = db.Column(db.String(256), nullable=True)
    additional_codes = db.Column(db.String(256), nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    user_id = db.Column(db.String(64))
    marked_as_deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String(64), nullable=True)
    deleted_on = db.Column(db.DateTime, server_default=db.func.now(), default=db.func.now(), nullable=False)
    note_code = db.relationship(NoteCode)


class AdditionalCode(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_id = db.Column(db.Integer, ForeignKey("note.id"), nullable=False)
    section = db.Column(db.Enum(EnumCodedSection), nullable=False)
    type = db.Column(db.Enum(EnumCodeType), nullable=False)
    code = db.Column(db.String(256))
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    comorbidity = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.String(64))
    created_on = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
