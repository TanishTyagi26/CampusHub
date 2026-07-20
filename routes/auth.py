from flask import Blueprint, render_template, request, redirect, session, flash
import sqlite3

auth = Blueprint("auth", __name__)


# ==========================
# Student Login
# ==========================
@auth.route("/login/<role>", methods=["GET", "POST"])
def login(role):

    if request.method == "POST":

        email = request.form["email"].strip()
        password = request.form["password"].strip()

        connection = sqlite3.connect("database/campushub.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM students
            WHERE email=? AND password=?
        """, (email, password))

        user = cursor.fetchone()

        connection.close()

        if user:

            session["student_id"] = user[0]
            session["student_name"] = user[1]

            flash("Login Successful!", "success")

            return redirect("/student/dashboard")

        flash("Invalid Email or Password!", "error")

        return redirect("/login/student")

    return render_template(
        "login.html",
        role=role.title()
    )


# ==========================
# Registration Page
# ==========================
@auth.route("/register")
def register():

    return render_template("register.html")


# ==========================
# Register Student
# ==========================
@auth.route("/register", methods=["POST"])
def register_student():

    full_name = request.form["full_name"].strip()
    email = request.form["email"].strip()
    password = request.form["password"].strip()
    branch = request.form["branch"]
    year = request.form["year"]

    connection = sqlite3.connect("database/campushub.db")
    cursor = connection.cursor()

    try:

        cursor.execute("""

            INSERT INTO students(
                full_name,
                email,
                password,
                branch,
                year
            )

            VALUES(?,?,?,?,?)

        """, (

            full_name,
            email,
            password,
            branch,
            year

        ))

        connection.commit()

        flash(
            "Registration Successful! Please Login.",
            "success"
        )

    except sqlite3.IntegrityError:

        flash(
            "Email already exists!",
            "error"
        )

    finally:

        connection.close()

    return redirect("/login/student")


# ==========================
# Logout
# ==========================
@auth.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged Out Successfully.",
        "success"
    )

    return redirect("/")