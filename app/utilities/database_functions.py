from app.models import User, Device

def total_stats():
    users = User.query.count()
    devices = Device.query.count()

    return {
        "total_jobs": 0,
        "total_users": users,
        "total_devices": devices
    }