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


from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class FindForm(FlaskForm):
    dal = StringField("DAL ID", validators=[DataRequired()])
    submit = SubmitField("Search")

class FeedbackForm(FlaskForm):
    is_correct = BooleanField("Annotation Correct")
    requires_additional_code = BooleanField("Requires Additional Code(s)")
    additional_codes = StringField("Additional Code(s)", description="This can be either an ICD-10 code or a standard. Please separate codes using spaces.")
    remove_or_replace = SelectField("Remove or Replace?", choices=((1, "Remove"), (2, "Replace")))
    replace_with = StringField("Replace With")
    comments = TextAreaField("Additional Comments")
    submit = SubmitField("Submit Feedback")
