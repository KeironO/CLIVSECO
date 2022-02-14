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


def validation_error_response(err):
    try:
        message = err.messages

    except AttributeError:
        if isinstance(err, str):
            message = err
        elif "messages" in err.keys():
            message = err["messages"]
        elif "message" in err.keys():
            message = err["message"]

    return (
        {"success": False, "message": message, "type": "Validation Error"},
        417,
        {"ContentType": "application/json"},
    )


def no_values_response():
    return (
        {"success": False, "message": "No input data provided"},
        400,
        {"ContentType": "application/json"},
    )


def transaction_error_response(err):
    try:
        return (
            {"success": False, "message": str(err.orig.diag.message_primary)},
            417,
            {"ContentType": "application/json"},
        )
    except Exception:
        return (
            {"success": False, "message": str(err), "type": "Transaction Error"},
            417,
            {"ContentType": "application/json"},
        )


def success_with_content_response(content):
    return (
        {"success": True, "content": content},
        200,
        {"ContentType": "application/json"},
    )


def success_without_content_response():
    return {"success": True}, 200, {"ContentType": "application/json"}
