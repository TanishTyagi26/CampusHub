from flask import Blueprint, render_template, request, redirect, session
import sqlite3

auth = Blueprint("auth", __name__)

# Login
@auth.route("/login/<role>", methods=["GET", "POST"])
def login(role):

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("database/campushub.db")
        cursor = connection.cursor()

        cursor.execute("""
        SELECT * FROM students
        WHERE email=? AND password=?
        """, (email, password))

        user = cursor.fetchone()

        connection.close()

        if user:

            session["student_id"] = user[0]
            session["student_name"] = user[1]

            return redirect("/student/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html", role=role.title())


# Registration Page
@auth.route("/register")
def register():
    return render_template("register.html")


# Save Student
@auth.route("/register", methods=["POST"])
def register_student():

    full_name = request.form["full_name"]
    email = request.form["email"]
    password = request.form["password"]
    branch = request.form["branch"]
    year = request.form["year"]

    connection = sqlite3.connect("database/campushub.db")
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO students(full_name,email,password,branch,year)
    VALUES(?,?,?,?,?)
    """,(full_name,email,password,branch,year))

    connection.commit()
    connection.close()

    return redirect("/login/student")


# Logout
@auth.route("/logout")
def logout():

    session.clear()

    return redirect("/")