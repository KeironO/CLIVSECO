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

from .codes import *
from .confirmation import *
from .note import *


from ...api import api, db
from ...api.responses import (
    success_with_content_response,
)
from ...database import AutoCode, NoteCode, ClinicalCoderCode, Note, NoteConfirmation
from sqlalchemy import func

def prepare_for_chartjs(data, label):

    colours = """#007A78
#002D85
#003391
#00389D
#003EA9
#0045B6
#004BC2
#0051CE
#0058DA
#005FE7
#0167F3
#0d6efd
#1477FF
#2680FF
#3989FF
#4C92FF
#5E9CFF
#71A7FF
#84B1FF
#97BCFF
#AAC8FF
#BDD3FF"""


    colours = [x for x in colours.split("\n") if x != '']
    colours = colours[0:len(data)]

    dataset = {
        "labels": [str(x[0]) for x in data],
        "datasets": [{
            "label": label,
            "data": [x[1] for x in data],
            "backgroundColor": colours,
            "borderWidth": 1,
            "borderColor": colours,
        }]
    }
    return dataset


@api.route("/notes/chartjs", methods=["GET"])
def charts_js_api():
    content = {}

    content["notes"] = {}
    content["autocodes"] = {}

    # Admission Spec

    asc = [(t, count) for (t, count) in db.session.query(
        Note.admission_spec, func.count(Note.admission_spec)
    ).group_by(Note.admission_spec)]

    asc_prepared = prepare_for_chartjs(asc, "Admitting Spec")
    
    content["notes"]["admitting_spec"] = asc_prepared

    # Discharge Spec

    dcs = [(t, count) for (t, count) in db.session.query(
        Note.discharge_spec, func.count(Note.discharge_spec)
    ).group_by(Note.discharge_spec)]

    dcs_prepared = prepare_for_chartjs(dcs, "Discharge Spec")
    content["notes"]["discharge_spec"] = dcs_prepared

    # Source Text

    stt = [(t, count) for (t, count) in db.session.query(
        AutoCode.section, func.count(AutoCode.section)
    ).group_by(AutoCode.section)]


    stt_prepared = prepare_for_chartjs(stt, "Auto Code Section")
    content["autocodes"]["source_text"] = stt_prepared


    content["counts"] = {}
    
    content["counts"]["letters"] =  db.session.query(func.count(Note.dal_id)).scalar()
    content["counts"]["autocodes"] = db.session.query(func.count(AutoCode.id)).scalar()

    
    return success_with_content_response(content)