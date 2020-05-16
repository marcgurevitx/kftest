import os
import pathlib

from flask import Flask, current_app, render_template

from . import db


def create_app():
    """
    Flask app factory
    """
    app = Flask(__name__)
    app.config.from_pyfile("local_secrets.py")
    app.teardown_appcontext(db.close_connection)
    
    @app.route("/")
    def catalog():
        """
        список объектов недвижимости
        """
        return render_template("catalog.html")
    
    @app.route("/description/<object_id>")
    def description(object_id):
        """
        детальная страница объекта
        """
        return render_template("description.html", object_id=object_id)
    
    return app
