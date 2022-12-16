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

from ...database import db, Base, Encounter, Versioning, CodeableConcept
from sqlalchemy import ForeignKey

class Audited(Base):
    encounterid = db.Column(db.String(36), ForeignKey("ENCOUNTER.id"), nullable=False)
    versionid = db.Column(db.String(36), ForeignKey("VERSIONING.id"), nullable=False)
    comments = db.Column(db.String(4096))
    nadex = db.Column(db.String(16), nullable=False)

class AuditedCode(Base):
    auditedid = db.Column(db.String(36), ForeignKey("AUDITED.id"), nullable=False)
    versionid = db.Column(db.String(36), ForeignKey("VERSIONING.id"), nullable=False)
    codeableconceptid = db.Column(db.String(36), ForeignKey(CodeableConcept.id), nullable=False)
    position = db.Column(db.Integer, nullable=False)