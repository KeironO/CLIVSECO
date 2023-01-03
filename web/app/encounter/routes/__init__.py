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

from sqlalchemy import func, desc
from flask import render_template
from flask_login import login_required
from .. import encounter

from ...utils import prepare_for_chartjs
from ...database import db
from ...api.responses import success_with_content_response
from ...misc.models import News

@encounter.route("/", methods=["GET"])
@login_required
def home():
    news = News.query.order_by(desc(News.created_on)).limit(5).all()
    return render_template(
        "encounter/index.html",
        news=news
    )


@encounter.route("/chartjs", methods=["GET"])
@login_required
def charts_js_api():
    content = {}

    content["encounters"] = {}
    content["autocodes"] = {}

    # Admission Spec

    ADMISSION_SPEC_COUNT_QUERY = f"""
    	SELECT DISTINCT ENC.id, TBIPA.SPECIALTY_NAME FROM [CLIVSECO].[dbo].[ENCOUNTER] AS ENC
		INNER JOIN [REPORTING_CTM].[DBO].[TBIPACTIVITY] AS TBIPA
			ON TBIPA.CASENO  = ENC.casenumber AND TBIPA.LINKID = ENC.paslinkid
		INNER JOIN [CLIVSECO].[dbo].[AUTOCODERRESULTS] AS ACR
			ON ACR.encounterid = ENC.id
		WHERE 
			ACR.VERSIONINGID = '41F3109C-06FB-4C36-80D9-BCF27C94C39E'
		AND
			TBIPA.EPISODENO = 1
    """

    admission_spec_count = db.session.execute(ADMISSION_SPEC_COUNT_QUERY)
    admission_spec_count_results = {}

    for row in admission_spec_count:
        if row.SPECIALTY_NAME not in admission_spec_count_results:
            admission_spec_count_results[row.SPECIALTY_NAME] = 0
        admission_spec_count_results[row.SPECIALTY_NAME] += 1

    content["encounters"]["admitting_spec"] = prepare_for_chartjs([(k,v) for k,v in admission_spec_count_results.items()], "Admitting Specialty")

    # Discharging Spec

    DISCHARGING_SPEC_COUNT_QUERY = f"""
    	SELECT DISTINCT ENC.id, TBIPA.SPECIALTY_NAME FROM [CLIVSECO].[dbo].[ENCOUNTER] AS ENC
		INNER JOIN [REPORTING_CTM].[DBO].[TBIPACTIVITY] AS TBIPA
			ON TBIPA.CASENO  = ENC.casenumber AND TBIPA.LINKID = ENC.paslinkid
		INNER JOIN [CLIVSECO].[dbo].[AUTOCODERRESULTS] AS ACR
			ON ACR.encounterid = ENC.id 
		WHERE 
			ACR.VERSIONINGID = '41F3109C-06FB-4C36-80D9-BCF27C94C39E'
		AND
			TBIPA.LASTEPIND = 1
    """

    discharging_spec_count = db.session.execute(DISCHARGING_SPEC_COUNT_QUERY)
    discharging_spec_count_results = {}

    for row in discharging_spec_count:
        if row.SPECIALTY_NAME not in discharging_spec_count_results:
            discharging_spec_count_results[row.SPECIALTY_NAME] = 0
        discharging_spec_count_results[row.SPECIALTY_NAME] += 1

    content["encounters"]["discharge_spec"] = prepare_for_chartjs([(k,v) for k,v in admission_spec_count_results.items()], "Discharging Specialty")

    SOURCE_DOCUMENT_QUERY = f"""
        SELECT sourcedocument, count(*) [count] FROM [CLIVSECO].[dbo].[AUTOCODERRESULTS] AS ACR
        INNER JOIN [CLIVSECO].[dbo].[CODESOURCE] AS CS ON ACR.codesourceid = CS.id
        WHERE
            ACR.VERSIONINGID = '41F3109C-06FB-4C36-80D9-BCF27C94C39E'
        GROUP BY sourcedocument
        ORDER BY 2 DESC
    """

    source_document_count = db.session.execute(SOURCE_DOCUMENT_QUERY)
    source_document_count_result = []

    for result in source_document_count:
        source_document_count_result.append(
            [result.sourcedocument, result.count]
        )
    content["encounters"]["source_text"] = prepare_for_chartjs(source_document_count_result, "Source Text")
    content["counts"] = {}    
    content["counts"]["encounters"] =  sum([y for (x, y) in discharging_spec_count_results.items()])
    content["counts"]["autocodes"] = sum([y for (x, y) in source_document_count_result])

    
    return success_with_content_response(content)

from .codes import *
from .feedback import *