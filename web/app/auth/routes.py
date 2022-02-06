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

from flask_login import login_user, logout_user, login_required
from . import auth

from sqlalchemy import func

from flask import render_template, flash, redirect, url_for

from .forms import LoginForm
from .models import UserAccount

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = UserAccount.query.filter(func.lower(UserAccount.email) == func.lower(form.email.data)).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("notes.home"))
        else:
            flash("Incorrect email or password.")
    return render_template("auth/login.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully been logged out.")
    return redirect(url_for("auth.login"))
