from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def catalog():
    """
    список объектов недвижимости
    """
    return render_template("catalog.html")


@app.route('/description/<object_id>')
def description(object_id):
    """
    детальная страница объекта
    """
    return render_template("description.html", object_id=object_id)
