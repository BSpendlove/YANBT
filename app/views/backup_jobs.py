from flask import Blueprint, render_template

bp = Blueprint("backup_jobs", __name__, url_prefix="/backup_jobs")

@bp.route("/", methods=["GET"])
def index():
    return render_template("backup_jobs/index.html")
