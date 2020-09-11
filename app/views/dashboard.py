from flask import Blueprint, render_template
from app.utilities import database_functions

bp = Blueprint("dashboard", __name__)

@bp.route("/", methods=["GET"])
def index():
    stats = database_functions.total_stats()
    return render_template("dashboard/index.html", stats=stats)

@bp.route("/test", methods=["GET"])
def test():
    return render_template("tests/bootstrap_learning.html")
