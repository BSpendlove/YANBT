from flask import Blueprint, request
from app.models import BackupJob
from app.utilities import generic_responses, validators
from app import db

bp = Blueprint("api_backupjob", __name__, url_prefix="/api/v1/backupjob")

@bp.route("/", methods=["GET"])
def get_backup_jobs():
    jobs = BackupJob.query.all()
    return generic_responses.data_response([_job.as_dict() for _job in jobs])