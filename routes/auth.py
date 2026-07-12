from flask import Blueprint, render_template

auth = Blueprint("auth", __name__)

@auth.route("/login/<role>")
def login(role):
    return render_template("login.html", role=role.title())