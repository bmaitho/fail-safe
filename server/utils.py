from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify
from models import User, Role

def role_required(role_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            user = User.query.filter_by(id=current_user['id']).first()
            if not user or user.role.name != role_name:
                return jsonify({"message": "Access forbidden: incorrect role"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
