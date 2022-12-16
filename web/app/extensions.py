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

from flask_ldap3_login import LDAP3LoginManager
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import pickle
import os

from .database import db, LDAPUser

login_manager = LoginManager()
ldap_manager = LDAP3LoginManager()

login_manager = LoginManager()
migrate = Migrate()
ma = Marshmallow()

def load_users():
    users = {}
    if os.path.isfile("users.pkl"):
        with open("users.pkl", "rb") as infile:
            return pickle.load(infile)
    else:
        with open("users.pkl", "wb") as outfile:
            pickle.dump({}, outfile)
        load_users()

users = load_users()

def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    ldap_manager.init_app(app)

    @login_manager.user_loader
    def load_user(username):
        print(username)
        if username in users:
            return users[username]
        return None

    @ldap_manager.save_user
    def save_user(dn, username, data, memberships):
        users = load_users()
        print(users)
        user = LDAPUser(dn, username, data)
        users[username] = user
        with open("users.pkl", "wb") as outfile:
            pickle.dump(users, outfile)
        return user