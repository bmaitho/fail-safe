from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Ensure your config is set correctly
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    from models import User, Project, Cohort, ProjectMember, ProjectCohort  # Ensure models are imported
    
    with app.app_context():
        import cli # Ensure CLI commands are imported within app context

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
