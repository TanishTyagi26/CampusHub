from flask import Blueprint, render_template, request, redirect, current_app
import sqlite3
import os
from flask import send_from_directory
from flask import session

student = Blueprint("student", __name__)

@student.route("/student")
def student_home():
    return render_template("login.html", role="Student")


@student.route("/student/dashboard")
def dashboard():

    if "student_id" not in session:
        return redirect("/login/student")

    connection = sqlite3.connect("database/campushub.db")
    cursor = connection.cursor()

    # Total Notes
    cursor.execute("SELECT COUNT(*) FROM notes")
    notes_count = cursor.fetchone()[0]

    # Total Announcements
    cursor.execute("SELECT COUNT(*) FROM announcements")
    announcements_count = cursor.fetchone()[0]

    # Recent Notes
    cursor.execute("""
        SELECT title, subject
        FROM notes
        ORDER BY id DESC
        LIMIT 5
    """)
    recent_notes = cursor.fetchall()

    # Latest Announcements
    cursor.execute("""
        SELECT title
        FROM announcements
        ORDER BY id DESC
        LIMIT 5
    """)
    recent_announcements = cursor.fetchall()

    connection.close()

    return render_template(
        "dashboard.html",
        student_name=session["student_name"],
        notes_count=notes_count,
        announcements_count=announcements_count,
        recent_notes=recent_notes,
        recent_announcements=recent_announcements
    )

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

@student.route("/student/profile")
def profile():

    if "student_id" not in session:
        return redirect("/login/student")

    connection = sqlite3.connect("database/campushub.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (session["student_id"],)
    )

    student_data = cursor.fetchone()

    connection.close()

    return render_template(
        "profile.html",
        student=student_data
    )

@student.route("/student/announcements")
def announcements():

    if "student_id" not in session:
        return redirect("/login/student")

    connection = sqlite3.connect("database/campushub.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM announcements
    ORDER BY id DESC
    """)

    announcements = cursor.fetchall()

    connection.close()

    return render_template(
        "announcements.html",
        announcements=announcements
    )