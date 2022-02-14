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
