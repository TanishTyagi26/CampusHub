from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    current_app,
    send_from_directory,
    session,
    flash
)

import sqlite3
import os

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

    cursor.execute("""
    SELECT title, description
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

    if "student_id" not in session:
        return redirect("/login/student")

    if request.method == "POST":

        title = request.form["title"].strip()
        subject = request.form["subject"].strip()
        file = request.files["file"]

        if file.filename == "":

            flash(
                "Please select a file.",
                "error"
            )

            return redirect("/student/upload")

        filename = file.filename

        file.save(
            os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )
        )

        connection = sqlite3.connect("database/campushub.db")
        cursor = connection.cursor()

        cursor.execute("""

            INSERT INTO notes(
                title,
                subject,
                filename
            )

            VALUES(?,?,?)

        """, (

            title,
            subject,
            filename

        ))

        connection.commit()
        connection.close()

        flash(
            "Notes uploaded successfully!",
            "success"
        )

        return redirect("/student/dashboard")

    return render_template("upload_notes.html")


@student.route("/student/notes")
def view_notes():

    if "student_id" not in session:
        return redirect("/login/student")

    connection = sqlite3.connect("database/campushub.db")
    cursor = connection.cursor()

    cursor.execute("""

        SELECT *
        FROM notes
        ORDER BY id DESC

    """)

    notes = cursor.fetchall()

    connection.close()

    return render_template(
        "view_notes.html",
        notes=notes
    )

@student.route("/student/download/<filename>")
def download_note(filename):

    if "student_id" not in session:
        return redirect("/login/student")

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
        """
        SELECT *
        FROM students
        WHERE id=?
        """,
        (session["student_id"],)
    )

    student_data = cursor.fetchone()

    connection.close()

    if not student_data:

        flash(
            "Student profile not found.",
            "error"
        )

        return redirect("/student/dashboard")

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

        SELECT *
        FROM announcements
        ORDER BY id DESC

    """)

    announcements = cursor.fetchall()

    connection.close()

    return render_template(
        "announcements.html",
        announcements=announcements
    )