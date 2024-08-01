import click
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Project, Role
from app import db
from flask_jwt_extended import create_access_token, decode_token
from functools import wraps

def get_role_id_by_name(role_name):
    """Get the role ID by role name."""
    role = Role.query.filter_by(name=role_name).first()
    if role:
        return role.id
    return None

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = kwargs.get('token', None)
            if not token:
                click.echo("Missing token")
                return
            
            try:
                decoded_token = decode_token(token)
                user_role_id = decoded_token['sub']['role_id']
                user_role = Role.query.get(user_role_id).name
            except Exception as e:
                click.echo("Invalid token")
                return

            if user_role != required_role:
                click.echo(f"Access forbidden: {user_role} cannot perform this action")
                return

            return func(*args, **kwargs)
        return wrapper
    return decorator

@app.cli.command('register')
@click.argument('username')
@click.argument('email')
@click.argument('password')
@click.argument('role_name')
def register(username, email, password, role_name):
    """Register a new user."""
    with app.app_context():
        if User.query.filter_by(email=email).first():
            click.echo('User already exists')
            return
        
        role_id = get_role_id_by_name(role_name)
        if role_id is None:
            click.echo(f'Role {role_name} not found')
            return

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password, role_id=role_id)
        db.session.add(new_user)
        db.session.commit()
        click.echo(f'User {username} registered successfully')

@app.cli.command('login')
@click.argument('email')
@click.argument('password')
def login(email, password):
    """Login a user."""
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            token = create_access_token(identity={'id': user.id, 'role_id': user.role_id})
            click.echo(f"JWT Token: {token}")
        else:
            click.echo('Invalid email or password')

@app.cli.command('create-project')
@click.argument('name')
@click.argument('description')
@click.argument('github_link')
@click.argument('owner_email')
@click.argument('token')
@role_required('admin')
def create_project(name, description, github_link, owner_email, token):
    """Create a new project."""
    with app.app_context():
        owner = User.query.filter_by(email=owner_email).first()
        if not owner:
            click.echo('Owner not found')
            return

        new_project = Project(name=name, description=description, owner_id=owner.id, github_link=github_link)
        db.session.add(new_project)
        db.session.commit()
        click.echo(f'Project {name} created successfully')

@app.cli.command('list-projects')
@click.argument('token')
@role_required('student')
def list_projects(token):
    """List all projects."""
    with app.app_context():
        projects = Project.query.all()
        for project in projects:
            click.echo(f'ID: {project.id}, Name: {project.name}, Description: {project.description}, GitHub: {project.github_link}')
