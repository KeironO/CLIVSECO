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

SECRET_KEY = "BKGW9AT3x3E8mTtZ"
WTF_CSRF_SECRET_KEY = "BKGW9AT3x3E8mTtZ"
DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///clivseco.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
LDAP_HOST = 'GIG01SRVDOM0003.cymru.nhs.uk'
LDAP_BIND_DIRECT_PREFIX = 'CYMRU\\'
LDAP_BIND_DIRECT_CREDENTIALS = True
LDAP_BIND_DIRECT_GET_USER_INFO = False
# Declares what ldap attribute corresponds to the username passed to any login method when performing a bind. 
SECRET_KEY = 'secret'