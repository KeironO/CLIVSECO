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

import icd10

from . import cmd_setup

from ..database import db, ICD10Lookup
from tqdm import tqdm


@cmd_setup.cli.command("create-icd10-lookup")
def create_icd10_lookup():
    bulk_list = []
    print("Loading ICD10 codes into a bulk list..")
    for code, values in tqdm(icd10.codes.items()):
        bulk_list.append(
            ICD10Lookup(code=code, description=values[1], billable=values[0])
        )

    print("Bulk commiting to db")
    db.session.bulk_save_objects(bulk_list)
    db.session.commit()
    print("Done!")
