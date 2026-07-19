from flask import Blueprint, render_template

student = Blueprint("student", __name__)

@student.route("/student")
def student_home():
    return render_template("login.html", role="Student")

@student.route("/student/dashboard")
def dashboard():
    return render_template("dashboard.html")