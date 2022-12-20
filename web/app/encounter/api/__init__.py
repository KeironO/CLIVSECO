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

from .. import encounter

from ...api.responses import (
    success_with_content_response,
)

from sqlalchemy import func


from ...database import Encounter, db


@encounter.route("/chartjs", methods=["GET"])
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

