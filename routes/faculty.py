from flask import Blueprint, render_template

faculty = Blueprint("faculty", __name__)

@faculty.route("/faculty")
def faculty_home():
    return render_template("faculty_login.html")