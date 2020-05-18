from flask import render_template, request

from . import db
from . import filters


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


def description(object_id):
    """
    детальная страница объекта
    """
    estate = db.get_estate_object(object_id)
    return render_template("description.html", **locals())
