from flask import Blueprint, render_template, request, redirect, current_app
import sqlite3
import os
from flask import send_from_directory

student = Blueprint("student", __name__)

@student.route("/student")
def student_home():
    return render_template("login.html", role="Student")


@student.route("/student/dashboard")
def dashboard():
    return render_template("dashboard.html")


@student.route("/student/upload", methods=["GET", "POST"])
def upload_notes():

    if request.method == "POST":

        title = request.form["title"]
        subject = request.form["subject"]
        file = request.files["file"]

        filename = file.filename

        file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))

        connection = sqlite3.connect("database/campushub.db")
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO notes(title, subject, filename)
        VALUES(?,?,?)
        """, (title, subject, filename))

        connection.commit()
        connection.close()

        return redirect("/student/dashboard")

    return render_template("upload_notes.html")


@student.route("/student/notes")
def view_notes():

    connection = sqlite3.connect("database/campushub.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM notes")

    notes = cursor.fetchall()

    connection.close()

    return render_template("view_notes.html", notes=notes)

@student.route("/student/download/<filename>")
def download_note(filename):

    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=True
    )