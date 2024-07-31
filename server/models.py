from app import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates
import re
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    role = relationship('Role', back_populates='users')
    projects = relationship('Project', back_populates='owner')
    project_memberships = relationship('ProjectMember', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role_id': self.role_id
        }

class Role(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    users = relationship('User', back_populates='role')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Project(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    description = Column(String(500))
    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    github_link = Column(String(200))
    image_url = Column(String(200))  # New column for image URL
    owner = relationship('User', back_populates='projects')
    project_members = relationship('ProjectMember', back_populates='project')
    project_cohorts = relationship('ProjectCohort', back_populates='project')

    @validates('name')
    def validate_name(self, key, name):
        if len(name) < 7:
            raise AssertionError('Project name must be at least 7 characters long')
        return name

    @validates('github_link')
    def validate_github_link(self, key, github_link):
        if not github_link.startswith('https://github.com/'):
            raise AssertionError('GitHub link must start with "https://github.com/"')
        return github_link

    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise AssertionError('Project description must be at least 20 characters long')
        return description

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'github_link': self.github_link,
            'image_url': self.image_url
        }

class Cohort(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(200))
    project_cohorts = relationship('ProjectCohort', back_populates='cohort')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class ProjectMember(db.Model):
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    project = relationship('Project', back_populates='project_members')
    user = relationship('User', back_populates='project_memberships')

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id
        }

class ProjectCohort(db.Model):
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    cohort_id = Column(Integer, ForeignKey('cohort.id'), nullable=False)
    project = relationship('Project', back_populates='project_cohorts')
    cohort = relationship('Cohort', back_populates='project_cohorts')

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'cohort_id': self.cohort_id
        }
