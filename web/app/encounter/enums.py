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
    DI1 = "Discharge Diagnosis 1"
    DI2 = "Discharge Diagnosis 2"
    ALL = "Allergy"
    CLL = "Clinic Letter"
    TOMS = "TOMS"
    RADIS = "RADIS"
      
    def __repr__(self):
          return self.value

    def __str__(self):
          return str(self.value)    


class EnumCodeType(Enum):
    PROC = "Procedure"
    DIAG = "Diagnosis"

    def __repr__(self):
      return self.value