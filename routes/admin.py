from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash
)

import sqlite3

admin = Blueprint("admin", __name__)
admin = Blueprint("admin", __name__)


# ==========================
# Admin Login
# ==========================
@admin.route("/admin", methods=["GET", "POST"])
def admin_home():

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"].strip()

        connection = sqlite3.connect("database/campushub.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM admin
            WHERE username=? AND password=?
        """, (username, password))

        user = cursor.fetchone()

        connection.close()

        if user:

            session["admin_id"] = user[0]
            session["admin_username"] = user[1]

            flash(
                "Welcome Admin!",
                "success"
            )

            return redirect("/admin/dashboard")

        flash(
            "Invalid Username or Password.",
            "error"
        )

        return redirect("/admin")

    return render_template("admin_login.html")

# ==========================
# Dashboard
# ==========================
@admin.route("/admin/dashboard")
def admin_dashboard():

    if "admin_id" not in session:
        return redirect("/admin")

    connection = sqlite3.connect("database/campushub.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM faculty")
    faculty = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM notes")
    notes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM announcements")
    announcements = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "admin_dashboard.html",
        students=students,
        faculty=faculty,
        notes=notes,
        announcements=announcements
    )


# ==========================
# Students
# ==========================
@admin.route("/admin/students")
def admin_students():

    if "admin_id" not in session:
        return redirect("/admin")

    connection = sqlite3.connect("database/campushub.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    connection.close()

    return render_template(
        "admin_students.html",
        students=students
    )


@admin.route("/admin/delete_student/<int:id>")
def delete_student(id):

    if "admin_id" not in session:
        return redirect("/admin")

    connection = sqlite3.connect("database/campushub.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    connection.commit()
    connection.close()

    flash(
        "Student deleted successfully.",
        "success"
    )

    return redirect("/admin/students")

# ==========================
# Faculty
# ==========================
@admin.route("/admin/faculty")
def admin_faculty():

    if "admin_id" not in session:
        return redirect("/admin")

    connection = sqlite3.connect("database/campushub.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM faculty")

    faculty = cursor.fetchall()

    connection.close()

    return render_template(
        "admin_faculty.html",
        faculty=faculty
    )


@admin.route("/admin/delete_faculty/<int:id>")
def delete_faculty(id):

    if "admin_id" not in session:
        return redirect("/admin")

    connection = sqlite3.connect("database/campushub.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM faculty WHERE id=?",
        (id,)
    )

    connection.commit()
    connection.close()

    flash(
        "Faculty member deleted successfully.",
        "success"
    )

    return redirect("/admin/faculty")

# ==========================
# Notes
# ==========================
@admin.route("/admin/notes")
def admin_notes():

    if "admin_id" not in session:
        return redirect("/admin")

    connection = sqlite3.connect("database/campushub.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM notes ORDER BY id DESC")

    notes = cursor.fetchall()

    connection.close()

    return render_template(
        "admin_notes.html",
        notes=notes
    )


@admin.route("/admin/delete_note/<int:id>")
def admin_delete_note(id):

    if "admin_id" not in session:
        return redirect("/admin")

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

    return redirect("/admin/notes")


# ==========================
# Announcements
# ==========================
@admin.route("/admin/announcements")
def admin_announcements():

    if "admin_id" not in session:
        return redirect("/admin")

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
        "admin_announcements.html",
        announcements=announcements
    )

    
@admin.route("/admin/delete_announcement/<int:id>")
def admin_delete_announcement(id):

    if "admin_id" not in session:
        return redirect("/admin")

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

    return redirect("/admin/announcements")

# ==========================
# Logout
# ==========================
@admin.route("/admin/logout")
def admin_logout():

    session.clear()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect("/")