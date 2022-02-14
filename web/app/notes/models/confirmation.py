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


class NoteConfirmation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_code_id = db.Column(db.Integer, ForeignKey("note_code.id"), nullable=False)
    is_correct = db.Column(db.Boolean, default=True)
    comments = db.Column(db.String(2048), nullable=True)
    replace_with = db.Column(db.String(7), nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("user_account.id"), nullable=False)
