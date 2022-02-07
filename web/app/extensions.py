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


from flask import Flask

from flask_migrate import Migrate
from flask_login import LoginManager
from flask_marshmallow import Marshmallow

from .database import db, UserAccount


login_manager = LoginManager()
migrate = Migrate()
ma = Marshmallow()

def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id: int) -> UserAccount:
        return UserAccount.query.get(user_id)