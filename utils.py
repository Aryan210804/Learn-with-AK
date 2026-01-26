from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    """Decorator to require admin privileges for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def format_date(date):
    """Format datetime object to readable string"""
    if date:
        return date.strftime('%B %d, %Y')
    return 'N/A'


def format_datetime(date):
    """Format datetime object to readable string with time"""
    if date:
        return date.strftime('%B %d, %Y at %I:%M %p')
    return 'N/A'
