import os
import pathlib

from flask import Flask, current_app, render_template

from . import db
from . import utils


def create_app():
    """
    Flask app factory
    """
    app = Flask(__name__)
    app.config.from_pyfile("local_config.py")
    app.teardown_appcontext(db.close_connection)
    app.add_template_filter(utils.integer_if_possible, "integer_if_possible")
    
    @app.route("/")
    def catalog():
        """
        список объектов недвижимости
        """
        estate_objects = db.get_estate_objects()
        return render_template(
            "catalog.html",
            estate_objects=estate_objects,
        )
    
    @app.route("/description/<object_id>")
    def description(object_id):
        """
        детальная страница объекта
        """
        estate = db.get_estate_object(object_id)
        return render_template("description.html", estate=estate)
    
    return app
