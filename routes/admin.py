from flask import Blueprint, render_template

admin = Blueprint("admin", __name__)

@admin.route("/admin")
def admin_home():
    return render_template("admin_login.html")