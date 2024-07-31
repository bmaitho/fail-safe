import click
from flask import Flask
from app import create_app, db
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Role, Project, Cohort, ProjectMember, ProjectCohort

app = create_app()

def get_role_id_by_name(role_name):
    """Get the role ID by role name."""
    role = Role.query.filter_by(name=role_name).first()
    if role:
        return role.id
    return None

@app.cli.command('register')
@click.argument('username')
@click.argument('email')
@click.argument('password')
@click.argument('role_name')
def register(username, email, password, role_name):
    """Register a new user with a specified role."""
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
            click.echo(f'User {user.username} logged in successfully')
        else:
            click.echo('Invalid email or password')

@app.cli.command('create-project')
@click.argument('name')
@click.argument('description')
@click.argument('github_link')
@click.argument('owner_email')
def create_project(name, description, github_link, owner_email):
    """Create a new project."""
    with app.app_context():
        owner = User.query.filter_by(email=owner_email).first()
        if not owner:
            click.echo('Owner not found')
            return
        
        project = Project(name=name, description=description, github_link=github_link, owner_id=owner.id)
        db.session.add(project)
        db.session.commit()
        click.echo(f'Project {name} created successfully')

@app.cli.command('update-project')
@click.argument('project_id', type=int)
@click.argument('name')
@click.argument('description')
@click.argument('github_link')
def update_project(project_id, name, description, github_link):
    """Update a project."""
    with app.app_context():
        project = Project.query.get(project_id)
        if not project:
            click.echo('Project not found')
            return
        
        project.name = name
        project.description = description
        project.github_link = github_link
        db.session.commit()
        click.echo(f'Project {name} updated successfully')

@app.cli.command('delete-project')
@click.argument('project_id', type=int)
def delete_project(project_id):
    """Delete a project."""
    with app.app_context():
        project = Project.query.get(project_id)
        if not project:
            click.echo('Project not found')
            return
        
        db.session.delete(project)
        db.session.commit()
        click.echo(f'Project {project_id} deleted successfully')

@app.cli.command('assign-project-to-cohort')
@click.argument('project_id', type=int)
@click.argument('cohort_id', type=int)
def assign_project_to_cohort(project_id, cohort_id):
    """Assign a project to a cohort."""
    with app.app_context():
        project = Project.query.get(project_id)
        cohort = Cohort.query.get(cohort_id)
        if not project or not cohort:
            click.echo('Project or Cohort not found')
            return
        
        project_cohort = ProjectCohort(project_id=project.id, cohort_id=cohort.id)
        db.session.add(project_cohort)
        db.session.commit()
        click.echo(f'Project {project_id} assigned to Cohort {cohort_id}')

@app.cli.command('list-projects')
def list_projects():
    """List all projects."""
    with app.app_context():
        projects = Project.query.all()
        for project in projects:
            click.echo(f'ID: {project.id}, Name: {project.name}, Description: {project.description}, Owner ID: {project.owner_id}, GitHub Link: {project.github_link}')

@app.cli.command('list-cohorts')
def list_cohorts():
    """List all cohorts."""
    with app.app_context():
        cohorts = Cohort.query.all()
        for cohort in cohorts:
            click.echo(f'ID: {cohort.id}, Name: {cohort.name}, Description: {cohort.description}')

@app.cli.command('assign-cohort-to-project')
@click.argument('project_id', type=int)
@click.argument('cohort_id', type=int)
def assign_cohort_to_project(project_id, cohort_id):
    """Assign a cohort to a project."""
    with app.app_context():
        project = Project.query.get(project_id)
        cohort = Cohort.query.get(cohort_id)
        if not project or not cohort:
            click.echo('Project or Cohort not found')
            return
        
        project_cohort = ProjectCohort.query.filter_by(project_id=project_id, cohort_id=cohort_id).first()
        if project_cohort:
            click.echo('Project already assigned to this cohort')
            return
        
        project_cohort = ProjectCohort(project_id=project_id, cohort_id=cohort_id)
        db.session.add(project_cohort)
        db.session.commit()
        click.echo(f'Cohort {cohort_id} assigned to Project {project_id}')

@app.cli.command('list-students')
def list_students():
    """List all students."""
    with app.app_context():
        student_role_id = get_role_id_by_name('student')
        students = User.query.filter_by(role_id=student_role_id).all()
        for student in students:
            click.echo(f'ID: {student.id}, Username: {student.username}, Email: {student.email}')

if __name__ == '__main__':
    app.run()
