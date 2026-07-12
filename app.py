from flask import Flask

from routes.main import main
from routes.auth import auth
from routes.student import student
from routes.faculty import faculty
from routes.admin import admin

app = Flask(__name__)

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(student)
app.register_blueprint(faculty)
app.register_blueprint(admin)

if __name__ == "__main__":
    app.run(debug=True)