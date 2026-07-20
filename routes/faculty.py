from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    current_app,
    flash
)

import sqlite3
import os

faculty = Blueprint("faculty", __name__)


# ==========================
# Faculty Login
# ==========================
@faculty.route("/faculty", methods=["GET", "POST"])
@faculty.route("/faculty", methods=["GET", "POST"])
def faculty_login():

    if request.method == "POST":

        email = request.form["email"].strip()
        password = request.form["password"].strip()

        connection = sqlite3.connect("database/campushub.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM faculty
            WHERE email=? AND password=?
        """, (email, password))

        user = cursor.fetchone()

        connection.close()

        if user:

            session["faculty_id"] = user[0]
            session["faculty_name"] = user[1]

            flash(
                "Welcome back, Faculty!",
                "success"
            )

            return redirect("/faculty/dashboard")

        flash(
            "Invalid Email or Password.",
            "error"
        )

        return redirect("/faculty")

    return render_template("faculty_login.html")

# ==========================
# Dashboard
# ==========================
@faculty.route("/faculty/dashboard")
def faculty_dashboard():

    if "faculty_id" not in session:
        return redirect("/faculty")

    connection = sqlite3.connect("database/campushub.db")
    cursor = connection.cursor()

    # Total Notes
    cursor.execute("SELECT COUNT(*) FROM notes")
    notes_count = cursor.fetchone()[0]

    # Total Announcements
    cursor.execute("SELECT COUNT(*) FROM announcements")
    announcement_count = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "faculty_dashboard.html",
        faculty_name=session["faculty_name"],
        notes_count=notes_count,
        announcement_count=announcement_count
    )

# ==========================
# Upload Notes
# ==========================
@faculty.route("/faculty/upload", methods=["GET", "POST"])
def faculty_upload():

    if "faculty_id" not in session:
        return redirect("/faculty")

    if request.method == "POST":

        title = request.form["title"].strip()
        subject = request.form["subject"].strip()

        file = request.files["file"]

        if file.filename == "":

            flash(
                "Please choose a file.",
                "error"
            )

            return redirect("/faculty/upload")

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
                filename,
                uploaded_by
            )
            VALUES(?,?,?,?)
        """, (
            title,
            subject,
            filename,
            "Faculty"
        ))

        connection.commit()
        connection.close()

        flash(
            "Notes uploaded successfully.",
            "success"
        )

        return redirect("/faculty/notes")

    return render_template("faculty_upload_notes.html")


# ==========================
# View Notes
# ==========================
@faculty.route("/faculty/notes")
def faculty_notes():

    if "faculty_id" not in session:
        return redirect("/faculty")

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
        "faculty_notes.html",
        notes=notes
    )


# ==========================
# Delete Note
# ==========================
@faculty.route("/faculty/delete_note/<int:id>")
def delete_note(id):

    if "faculty_id" not in session:
        return redirect("/faculty")

    connection = sqlite3.connect("database/campushub.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE id=?",
        (id,)
    )

    connection.commit()
    connection.close()

    flash(
        "Note deleted successfully.",
        "success"
    )

    return redirect("/faculty/notes")

# ==========================
# Announcements
# ==========================
@faculty.route("/faculty/announcements", methods=["GET", "POST"])
def faculty_announcements():

    if "faculty_id" not in session:
        return redirect("/faculty")

    connection = sqlite3.connect("database/campushub.db")
    cursor = connection.cursor()

    if request.method == "POST":

        title = request.form["title"].strip()
        description = request.form["description"].strip()

        cursor.execute("""
            INSERT INTO announcements(
            title,
            description
        )
        VALUES(?,?)
    """, (
        title,
        description
    ))

    connection.commit()

    flash(
        "Announcement posted successfully.",
        "success"
    )

    cursor.execute("""
        SELECT *
        FROM announcements
        ORDER BY id DESC
    """)

    announcements = cursor.fetchall()

    connection.close()

    return render_template(
        "faculty_announcements.html",
        announcements=announcements
    )


# ==========================
# Delete Announcement
# ==========================
@faculty.route("/faculty/delete_announcement/<int:id>")
def delete_announcement(id):

    if "faculty_id" not in session:
        return redirect("/faculty")

    connection = sqlite3.connect("database/campushub.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM announcements WHERE id=?",
        (id,)
    )

    connection.commit()
    connection.close()

    flash(
        "Announcement deleted successfully.",
        "success"
    )

    return redirect("/faculty/announcements")


# ==========================
# Logout
# ==========================
@faculty.route("/faculty/logout")
def faculty_logout():

    session.clear()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect("/")