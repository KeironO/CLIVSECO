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

from enum import Enum

class EnumCodedSection(Enum):
    CLI = "Clinical Finding"
    PRE = "Presenting Complaint"
    TRE = "Treatment Narrative"
    DIA = "Discharge Diagnoses"
    ALL = "Allergy"
    CL1 = "Clinic Letter One"
    CL2 = "Clinic Letter Two"
    CL3 = "Clinic Letter Three"
    CL4 = "Clinic Letter Four"
    CL5 = "Clinic Letter Five"


class EnumCodeType(Enum):
    PROC = "Procedure"
    DIAG = "Diagnosis"