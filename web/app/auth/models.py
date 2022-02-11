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

from flask_login import UserMixin
from ..database import db
from werkzeug.security import generate_password_hash, check_password_hash


class UserAccount(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    email = db.Column(db.String(320), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)

    @property
    def password(self) -> str:
        return "hunter2"

    @password.setter
    def password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)
