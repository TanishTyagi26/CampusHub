from flask import Blueprint, render_template, request, redirect, session
import sqlite3

faculty = Blueprint("faculty", __name__)


# Faculty Login
@faculty.route("/faculty", methods=["GET", "POST"])
def faculty_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("database/campushub.db")
        cursor = connection.cursor()

        cursor.execute("""
        SELECT * FROM faculty
        WHERE email=? AND password=?
        """, (email, password))

        user = cursor.fetchone()

        print("Email:", email)
        print("Password:", password)
        print("User:", user)



        connection.close()

        if user:

            session["faculty_id"] = user[0]
            session["faculty_name"] = user[1]

            return redirect("/faculty/dashboard")

        return "Invalid Email or Password"

    return render_template("faculty_login.html")


# Faculty Dashboard
@faculty.route("/faculty/dashboard")
def faculty_dashboard():

    if "faculty_id" not in session:
        return redirect("/faculty")

    return render_template(
        "faculty_dashboard.html",
        faculty_name=session["faculty_name"]
    )


# Faculty Logout
@faculty.route("/faculty/logout")
def faculty_logout():

    session.clear()

    return redirect("/")