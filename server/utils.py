from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user['role_id'] != role:
                return jsonify({"message": "Access forbidden: incorrect role"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator