from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_talisman import Talisman

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Ensure your config is set correctly
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    Talisman(app)  # Enforce HTTPS

    from models import User, Project, Cohort, ProjectMember, Role, Class  # Ensure models are imported
    
    with app.app_context():
        import cli  # Ensure CLI commands are imported within app context
        from routes import register_blueprints
        register_blueprints(app)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(ssl_context=('path_to_cert.pem', 'path_to_key.pem'))
