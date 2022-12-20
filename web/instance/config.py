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

from sqlalchemy.engine import URL
import urllib

# pyodbc stuff for MS SQL
driver='{SQL Server}'
server='7a506srvbisql01'
database='CLIVSECO'
trusted_connection='yes'

# pyodbc connection string
connection_string = f'DRIVER={driver};SERVER={server};'
connection_string += f'DATABASE={database};'
connection_string += f'TRUSTED_CONNECTION={trusted_connection}'

SQLALCHEMY_DATABASE_URI = urllib.parse.unquote(str(URL.create(
    "mssql+pyodbc", query={"odbc_connect": connection_string}
)))
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "EXAMPLE-SECRET-KEY"
WTF_CSRF_SECRET_KEY = "EXAMPLE-SECRET-KEY"
DEBUG = True

LDAP_HOST = 'GIG01SRVDOM0003.cymru.nhs.uk'
LDAP_BIND_DIRECT_PREFIX = 'CYMRU\\'
LDAP_BIND_DIRECT_CREDENTIALS = True
LDAP_BIND_DIRECT_GET_USER_INFO = False

SECRET_KEY = 'EXAMPLE-SECRET-KEY'