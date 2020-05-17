import os
import pathlib

from flask import Flask, current_app, g, make_response, render_template, request

from . import db
from . import filters
from . import utils


def create_app():
    """
    Flask app factory
    """
    app = Flask(__name__)
    app.config.from_pyfile("local_config.py")
    app.teardown_appcontext(db.close_connection)
    app.add_template_filter(utils.integer_if_possible, "integer_if_possible")
    app.config["X_METRO_CHOICES"] = db.preload_metro_choices(app)
    
    @app.route("/")
    def catalog():
        """
        список объектов недвижимости
        """
        form = filters.get_form(request.args)
        if form.validate():
            estate_objects = db.get_estate_objects(form.data)
        else:
            estate_objects = []
        return render_template("catalog.html", **locals())
    
    @app.route("/description/<object_id>")
    def description(object_id):
        """
        детальная страница объекта
        """
        estate = db.get_estate_object(object_id)
        return render_template("description.html", **locals())
    
    return app
