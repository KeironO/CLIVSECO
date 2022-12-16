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
from ...database import db, Base
import enum

class Encounter(Base):
    paslinkid = db.Column(db.String(10))
    casenumber = db.Column(db.String(8))

class ComplexReason(enum.Enum):
    A = "The available source documentation does not accurately reflect the episode."
    B = "We have not got access to a digital form of documentation required to produce accurate autocoding."
    O = "Other"

class TooComplex(Base):
    encounterid = db.Column(db.String(36), ForeignKey("ENCOUNTER.id"), nullable=False)
    nadex = db.Column(db.String(16), nullable=False)
    comments = db.Column(db.String(2048))
    reason = db.Column(db.Enum(ComplexReason))
    reason_other = db.Column(db.String(4096), nullable=True)

