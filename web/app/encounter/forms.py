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


from tkinter.tix import Select
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError


def equals_yes(form, field):
    if field.data.upper() != 'YES':
        raise ValidationError('Please type Yes if you want to confirm')

class AuditorForm(FlaskForm):
    coders_note = TextAreaField("Coders Note")
    diagnosis = StringField("Diagnoses")
    procedures = StringField("Procedures")
    submit = SubmitField("Submit")

class FindForm(FlaskForm):
    caseno = StringField("Case Number", validators=[DataRequired()])
    linkid = StringField("WPAS Link ID")
    submit = SubmitField("Search")

class FeedbackForm(FlaskForm):
    is_correct = BooleanField("Annotation Correct")
    requires_additional_code = BooleanField("Requires Additional Code(s)")
    additional_codes = StringField(
        "Additional Code(s)",
        description="This can be either an OPCS4, ICD-10 code or a standard. Please separate codes using commas.",
        render_kw={"data-role": "tagsinput"},
    )
    remove_or_replace = SelectField(
        "Remove or Replace?", choices=((1, "Remove"), (2, "Replace"))
    )
    replace_with = StringField(
        "Replace With",
        description="This can be either an OPCS4 or ICD-10 code. Please separate codes using commas.",
        render_kw={"data-role": "tagsinput"},
    )
    comments = TextAreaField("Additional Comments")
    submit = SubmitField("Submit Feedback")

class DeleteFeedbackForm(FlaskForm):
    confirmation = StringField("Type Yes To Confirm Deletion", validators=[equals_yes])
    submit = SubmitField("Delete Feedback")

class AdditionalCodeForm(FlaskForm):
    section = SelectField("DAL Section", choices=(
        ("PRE", "Presenting Complaint"),
        ("TRE", "Treatment Narrative"),
        ("ALL", "Allergy"),
        ("DIA1", "Discharge Diagnoses")))
    start = StringField("Start")
    end = StringField("End")
    type = SelectField("Code Type", choices=(
        ('DIAG', 'Diagnosis'),
        ('PROC', 'Procedure')
    ))
    comorbidity = BooleanField("Comorbidity")
    additional_codes = StringField(
        "Additional Code(s)",
        description="This can be either an OPCS4, ICD-10 code or a standard. Please separate codes using commas.",
        render_kw={"data-role": "tagsinput"},
    )
    submit = SubmitField("Submit Additional Code")
