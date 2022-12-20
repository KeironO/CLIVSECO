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

from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from flask_ldap3_login.forms import LDAPLoginForm

from sqlalchemy import func

from flask import render_template, flash, redirect, url_for

from .forms import LoginForm


@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("encounter.home"))

    form = LDAPLoginForm()

    form.username.label = 'Nadex Username'

    if form.validate_on_submit():
        login_user(form.user)
        return redirect(url_for("encounter.home"))

    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully been logged out.")
    return redirect(url_for("auth.login"))
