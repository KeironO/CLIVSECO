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

from ..database import db, Base
import enum

class SeverityEnum(enum.Enum):
    NORMAL = "Normal"
    SEVERE = "Severe"

class News(Base):
    title = db.Column(db.String(1024), nullable=False)
    news = db.Column(db.String(4096), nullable=False)
    severity = db.Column(db.Enum(SeverityEnum))

class AccessLog(Base):
    nadex = db.Column(db.String(16), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    ip = db.Column(db.String(128))
    requesturl = db.Column(db.String(1024), nullable=False)
    responsestatus = db.Column(db.String(1024), nullable=False)
    requestreferrer = db.Column(db.String(1024), nullable=False)

class Versioning(Base):
    name = db.Column(db.String(128))
    rundatetime = db.Column(db.DateTime())
    changelog = db.Column(db.String(4096))

class SystemEnum(enum.Enum):
    ICD10 = "http://hl7.org/fhir/sid/icd-10"
    ICD11 = "http://hl7.org/fhir/sid/icd-11"
    SNOMEDCT = "http://snomed.info/sct"
    OPCS4 = "https://fhir.nhs.uk/Id/opcs-4"

class CodeableConcept(Base):
    system = db.Column(db.Enum(SystemEnum))
    code = db.Column(db.String(1024))