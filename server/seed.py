from faker import Faker
from app import create_app, db
from models import User, Role, Project, Cohort, ProjectMember, Class
from werkzeug.security import generate_password_hash
import random

fake = Faker()

def create_roles():
    roles = ['admin', 'student']
    for role_name in roles:
        role = Role(name=role_name)
        db.session.add(role)
    db.session.commit()

def get_role_by_name(role_name):
    return Role.query.filter_by(name=role_name).first()

def create_users(num_users):
    users = []
    student_role = get_role_by_name('student')
    for _ in range(num_users):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password_hash=generate_password_hash(fake.password()),  # Hash the password
            role_id=student_role.id  # Assign the role_id here
        )
        users.append(user)
        db.session.add(user)
    db.session.commit()
    return users

def create_projects(users, classes, num_projects):
    projects = []
    for _ in range(num_projects):
        owner = random.choice(users)
        class_ = random.choice(classes)  # Assign a random class to the project
        project = Project(
            name=fake.sentence(nb_words=4),
            description=fake.paragraph(),
            owner_id=owner.id,
            github_link=f"https://github.com/{fake.user_name()}/{fake.slug()}",
            class_id=class_.id  # Assign the class_id here
        )
        projects.append(project)
        db.session.add(project)
    db.session.commit()
    return projects

def create_cohorts(num_cohorts):
    cohorts = []
    for _ in range(num_cohorts):
        cohort = Cohort(
            name=fake.word(),
            description=fake.paragraph()
        )
        cohorts.append(cohort)
        db.session.add(cohort)
    db.session.commit()
    return cohorts

def create_classes(cohorts, num_classes):
    classes = []
    for _ in range(num_classes):
        cohort = random.choice(cohorts)  # Assign a random cohort to the class
        class_ = Class(
            name=fake.word(),
            description=fake.paragraph(),
            cohort_id=cohort.id  # Assign the cohort_id here
        )
        classes.append(class_)
        db.session.add(class_)
    db.session.commit()
    return classes

def assign_project_members(projects, users):
    for project in projects:
        num_members = random.randint(1, 5)
        members = random.sample(users, num_members)
        for member in members:
            project_member = ProjectMember(
                project_id=project.id,
                user_id=member.id
            )
            db.session.add(project_member)
    db.session.commit()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.drop_all()  # Drops all tables
        db.create_all()  # Creates all tables

        create_roles()
        num_users = 10
        num_projects = 15
        num_cohorts = 5
        num_classes = 5  # Define the number of classes to create

        users = create_users(num_users)
        cohorts = create_cohorts(num_cohorts)
        classes = create_classes(cohorts, num_classes)  # Create classes with assigned cohorts
        projects = create_projects(users, classes, num_projects)

        assign_project_members(projects, users)

        print("Database seeded successfully!")
