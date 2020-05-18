import os
import pathlib

from flask import Flask

from . import db
from . import views
from . import utils


def create_app():
    """
    Flask app factory
    """
    app = Flask(__name__)
    
    # Load secrets
    app.config.from_pyfile("local_config.py")
    
    # Show all metro stations in filter form
    app.config["X_METRO_CHOICES"] = db.preload_metro_choices(app)
    
    # Auto close connections after done with requests
    app.teardown_appcontext(db.close_connection)
    
    # Register views
    app.add_url_rule("/", view_func=views.catalog)
    app.add_url_rule("/description/<object_id>", view_func=views.description)
    
    # Some filter for templates
    app.add_template_filter(utils.integer_if_possible, "integer_if_possible")
    
    return app
