from flask import current_app
from wtforms import Form, FloatField, SelectMultipleField, validators


class FiltersForm(Form):
    """
    Form on catalog page that filters estate objects
    """
    area_min = FloatField("Area min", [validators.Optional()])
    area_max = FloatField("Area max", [validators.Optional()])
    floor_min = FloatField("Floor min", [validators.Optional()])
    floor_max = FloatField("Floor max", [validators.Optional()])
    metro_stations = SelectMultipleField("Metro station(s)", [validators.Optional()], coerce=int)


def get_form(values):
    """
    Return instance of filters form
    """
    form = FiltersForm(values)
    form.metro_stations.choices = current_app.config["X_METRO_CHOICES"]
    return form
