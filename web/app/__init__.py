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

from __future__ import absolute_import

from .database import db
from .extensions import register_extensions
from flask import Flask, g

from .commands import cmd_setup as cmd_setup_blueprint

from .misc import misc as misc_blueprint
from .auth import auth as auth_blueprint
#from .api import api as api_blueprint
from .encounter import encounter as encounter_blueprint

from .globs import _spec_maps

def register_blueprints(app: Flask):
    app.register_blueprint(cmd_setup_blueprint)
    app.register_blueprint(misc_blueprint, url_prefix='/')
    # app.register_blueprint(api_blueprint, url_prefix="/api")
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(encounter_blueprint, url_prefix="/notes")


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")

    @app.context_processor
    def inject_data():
        return dict(spec_maps=_spec_maps)

    register_extensions(app)
    register_blueprints(app)

    return app


def setup_database(app):
    with app.app_context():
        db.create_all()
