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


from flask import render_template, url_for, flash, redirect, request, abort, g
from flask_login import login_required, current_user

from .. import encounter

from ..forms import AdditionalCodeForm

from sqlalchemy import func, text

from ..forms import FindForm, AuditorForm

import requests

from ...database import db
from ..models import Encounter

@encounter.route("/code/random/<spec>")
def get_random_code(spec):

    response = requests.get(url_for("api.random_note", spec=spec, _external=True), verify=False)

    if response.status_code == 200:
        note = response.json()
        return redirect(
            url_for(
                "notes.code",
                caseno=note["content"]["caseno"],
                linkid=note["content"]["linkid"]
                )
            )
    else:
        return response.content


@encounter.route("/audit/<id>", methods=["GET", "POST"])
@login_required
def code(id: id):

    REQUEST_SQL = f"""SELECT 
    ENCOUNTER.ID [ID],
    ENCOUNTER.paslinkid [PASLINKID],
    ENCOUNTER.casenumber [CASENUMBER],
    SDX.NHS_Number [NHSNUMBER],
    SDX.BirthDate [BIRTHDATE],
    TBIPA.EPISODENO [EPISODENUMBER],
    TBIPA.SPECIALTY_NAME [SPECIALTY_NAME],
    TBIPA.START_DATE [ADMISSIONDATE],
    TBIPA.DisDate_DT [DISCHARGEDATE],
    TBIPA.LOS [LOS],
    TBIPA.SEX [SEX],
    DATEDIFF(YYYY, CAST(SDX.BirthDate AS DATE), CAST(TBIPA.START_DATE AS DATE)) [AGEONADMISSION]
    FROM [CLIVSECO].[dbo].[ENCOUNTER] AS ENCOUNTER
    INNER JOIN [MTED].[dbo].[EDAL] AS SDX
        ON SDX.Hospital_Number = ENCOUNTER.casenumber AND ENCOUNTER.paslinkid = SDX.WPAS_LINKID
    INNER JOIN [Reporting_CTM].[dbo].[TbIPActivity] AS TBIPA
        ON TBIPA.CASENO = ENCOUNTER.casenumber and ENCOUNTER.paslinkid = TBIPA.LINKID
    WHERE
        ENCOUNTER.ID = '{id}'
    AND
        TBIPA.LastEpInd = 1
    """

    form = AdditionalCodeForm()

    base_encounter_info = list(db.session.execute(REQUEST_SQL).fetchall())[0]

    if base_encounter_info == None:
        return abort(404)

    REQUEST_EDALBASE_SQL = f"""SELECT 
	CLIV_ENCOUNTER.id [ENCOUNTERID],
	CLIV_ENCOUNTER.paslinkid [PASLINKID],
	CLIV_ENCOUNTER.casenumber [CASENUMBER],
	OMTED_EDAL.DAL_Unique_ID [EDALID],
	NMTED_EDALBASE.DocumentDateTime [EDALDOCUMENTDATETIME],
	NMTED_EDALBASE.MedicinesUpdatedBy [EDALMEDICINSUPDATEDBY],
	NMTED_EDALBASE.MedicinesVerifiedForDischarge [EDALVERITIFEDFORDISCHARGE],
	NMTED_EDALBASE.PresentingComplaints [EDALPRESENTINGCOMPLAINTS],
	NMTED_EDALBASE.InvestigationsAndResults [EDALINVESTIGATIONSANDRESULTS],
	NMTED_EDALBASE.ClinicalFindings [EDALCLINICALFINDINGS]
	FROM [CLIVSECO].[dbo].[Encounter] AS CLIV_ENCOUNTER
		INNER JOIN [MTED].[dbo].[EDAL] AS OMTED_EDAL
			ON
				CLIV_ENCOUNTER.casenumber = OMTED_EDAL.Hospital_Number
			AND
				CLIV_ENCOUNTER.paslinkid = OMTED_EDAL.WPAS_LINKID
		INNER JOIN [MTED].[dbo].[EDALBase] AS NMTED_EDALBASE
			ON NMTED_EDALBASE.ID = OMTED_EDAL.DAL_Unique_ID
	WHERE
		CLIV_ENCOUNTER.id = '{id}'
    """
    
    base_edal_infos = list(db.session.execute(REQUEST_EDALBASE_SQL).fetchall())

    
    DIAGNOSIS_REQUEST_SQL = f"""SELECT
	NMTED_EDALDIAGNOSES.EDALBASEID [EDALDIAGNOSISEDALBASEID],
	NMTED_EDALDIAGNOSES.ID [EDALDIGANOSISID],
	NMTED_EDALDIAGNOSES.NARRATIVE [EDALDIAGNOSISNARRATIVE],
	NMTED_EDALDIAGNOSES.STATUS [EDALDIAGNOSISSTATUS],
	NMTED_EDALDIAGNOSES.ISNEW [EDALDIAGNOSISISNEW],
	NMTED_EDALDIAGNOSES.RESOLVED [EDALDIANGOSISRESOLVED],
	NMTED_EDALDIAGNOSES.RECORDEDAT [EDALDIAGNOSISRECORDEDAT]
	FROM [CLIVSECO].[dbo].[Encounter] AS CLIV_ENCOUNTER
		INNER JOIN [MTED].[dbo].[EDAL] AS OMTED_EDAL
			ON
				CLIV_ENCOUNTER.casenumber = OMTED_EDAL.Hospital_Number
			AND
				CLIV_ENCOUNTER.paslinkid = OMTED_EDAL.WPAS_LINKID
		INNER JOIN [MTED].[dbo].[EDALDiagnoses] AS NMTED_EDALDIAGNOSES
			ON NMTED_EDALDIAGNOSES.EDALBASEID = OMTED_EDAL.DAL_Unique_ID
	WHERE
		CLIV_ENCOUNTER.id = '{id}'

    """

    dal_diagnoses = {}
    diagnoses_response = list(db.session.execute(DIAGNOSIS_REQUEST_SQL).fetchall())

    for row in diagnoses_response:
        if row.EDALDIAGNOSISEDALBASEID not in dal_diagnoses:
            dal_diagnoses[row.EDALDIAGNOSISEDALBASEID] = []
        dal_diagnoses[row.EDALDIAGNOSISEDALBASEID].append(row)

    TOMS_DETAILS_SQL = f"""SELECT
	thCase.CASE_NUMBER [TOMSCASENUMBER
    ],
	or_Arrival_Date [TOMSARRIVALDATE],
	thNote.Completed_Date [TOMSCOMPLETEDATE],
	thNote.Date_Entered [TOMSDATENTERED],
	thNote.Entered_By [TOMSENTEREDBY],
	Indications [TOMSINDICATIONS],
	Incision [TOMSINCISION],
	Findings [TOMSFINDINGS],
	Followup [TOMSFOLLOWUP],
	[Procedure] [TOMSPROCEDURE],
	[Comment] [TOMSCOMMENTS]
	FROM [CLIVSECO].[dbo].[ENCOUNTER] AS Encounter
	INNER JOIN [MTED].[dbo].[EDAL] AS EDAL
		ON EDAL.WPAS_LINKID = Encounter.paslinkid AND EDAL.Hospital_Number = Encounter.casenumber
	INNER JOIN [Reporting_CTM].[dbo].[TbIPActivity] AS TbIPActivity
		ON EDAL.WPAS_LINKID = TbIPACtivity.LINKID AND EDAL.Hospital_Number = TbIPACtivity.CaseNo
	INNER JOIN [TOMS_v3].[dbo].[thCase] as thCase
		ON thCase.UNIT_NUMBER = Encounter.casenumber AND thCase.or_Arrival_Date
			BETWEEN TbIPActivity.TRT_DATE_DT AND TbIpActivity.DISDATE_DT
	INNER JOIN [TOMS_v3].[dbo].[thNote] as thNote
		ON thNote.CASE_NUMBER = thCase.CASE_NUMBER
	WHERE 
		TbIPActivity.LastEpInd = 1
	AND
		Encounter.id = '{id}'
	AND
		thNote.Complete_Flag = 'Y'
    """

    toms_info = list(db.session.execute(TOMS_DETAILS_SQL).fetchall())

    CLINIC_LETTERS_SQL = f"""SELECT DISTINCT TBPCL.* FROM [CLIVSECO].[dbo].[Encounter] AS ENC
    INNER JOIN [Reporting_CTM].[dbo].[TbIPActivity] AS TBIPA
        ON ENC.paslinkid = TBIPA.linkid AND ENC.casenumber = TBIPA.caseno
    INNER JOIN [_Sandbox_General].[dbo].[TbParsedClinicLetters] AS TBPCL
        ON ENC.casenumber = TBPCL.CASENO AND TBPCL.VERSION_DATE
			BETWEEN
				DATEADD(D, -14, TBIPA.TRT_DATE) AND DATEADD(D, 14, TBIPA.DISDATE)
    WHERE
        LastEpInd = 1
	AND
		STATUS = 'AUTH'
	AND
		ENC.id = '431E3402-98ED-40A1-95A8-61A4413BAF00'
    """

    clinic_letters = list(db.session.execute(CLINIC_LETTERS_SQL).fetchall())

    form = AdditionalCodeForm()
    if form.validate_on_submit():
        pass

    return render_template(
        "encounter/view.html",
        note=base_encounter_info,
        edalbase_info = base_edal_infos,
        dal_diagnoses=dal_diagnoses,
        toms_info=toms_info,
        clinic_letters=clinic_letters,
        form=form
    )

@encounter.route("/code/<id>/audit", methods=["GET", "POST"])
@login_required
def audit(id): 
    response = requests.get(
        url_for(
            "api.get_note",
            caseno=id,
            linkid=id,
            _external=True
        ), verify=False)

    if response.status_code == 200:
        note = response.json()

        form = AuditorForm()

        if form.validate_on_submit():

            _json = {
                "note_id": note["content"]["id"],
                "procedures": form.procedures.data,
                "diagnoses": form.diagnosis.data,
                "caseno": caseno,
                "linkid": linkid,
                "coders_note": form.coders_note.data,
                "author": "AUTOCODER*%s" % (str(current_user.username))
            }

            audit_response = requests.post(url_for("api.submit_feedback", _external=True),
                json=_json, verify=False)
            
            if audit_response.status_code == 200:
                flash("The audit codes have been submitted. If you've made a mistake email Keiron.")
                return redirect(url_for('notes.code',caseno=caseno,linkid=linkid))


        return render_template(
            "notes/audit.html",
            note=note["content"],
            caseno=caseno,
            linkid=linkid,
            form=form
        )
    else:
        return response.content


@encounter.route("/get/<caseno>:<linkid>")
@login_required
def code_endpoint(caseno: str, linkid: str):
    response = requests.get(
        url_for(
            "api.get_note",
            caseno=caseno,
            linkid=linkid,
            _external=True
        ), verify=False)
    return response.json()



@encounter.route("/find/", methods=["GET", "POST"])
@login_required
def find_note():
    form = FindForm()
    found = []

    
    if form.validate_on_submit():
        query_extension = ""
        if '%s' % (form.linkid.data) != '':
            query_extension = "AND ENCOUNTER.paslinkid = '%s'" % (form.linkid.data)

        FIND_QUERY = f"""
            SELECT
                ENCOUNTER.ID,
                TBIPA.CASENO,
                TBIPA.LINKID,
                TBIPA.EPISODENO,
                TBIPA.SPECIALTY_NAME,
                ENCOUNTER.ID,
                CAST(TBIPA.Start_Date_DT AS DATE) [STARTDATE],
                CAST(TBIPA.DisDate_DT AS DATE) [DISDATE]
                FROM [Reporting_CTM].[dbo].[TbIPActivity] AS TBIPA
                    INNER JOIN [CLIVSECO].[dbo].[ENCOUNTER] AS ENCOUNTER
                        ON ENCOUNTER.casenumber = TBIPA.CASENO AND ENCOUNTER.paslinkid = TBIPA.LINKID
                WHERE
                    ENCOUNTER.casenumber = '{form.caseno.data}' {query_extension}
                AND
                    TBIPA.LastEpInd = 1
        """
        found = list(db.session.execute(FIND_QUERY))

    return render_template("encounter/find.html", form=form, found=found)
