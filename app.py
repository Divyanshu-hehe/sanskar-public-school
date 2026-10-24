import os
from datetime import datetime
from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models import db, AdminUser, WebsiteSetting
from seed import seed_database
from routes.main import main_bp
from routes.api import api_bp
from routes.admin import admin_bp

def create_app(config_class=Config):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, 'templates'),
        static_folder=os.path.join(base_dir, 'static')
    )
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Please log in to access the administrative portal.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(AdminUser, int(user_id))

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)

    # Global Template Context Processor
    @app.context_processor
    def inject_global_data():
        settings_dict = {}
        try:
            settings = WebsiteSetting.query.all()
            for s in settings:
                settings_dict[s.key] = s.value
        except Exception:
            pass

        return {
            'settings': settings_dict,
            'current_year': datetime.now().year,
            'school_name': settings_dict.get('school_name', 'Sanskar Public School'),
            'school_motto': settings_dict.get('school_motto', 'विद्या ददाति विनयम्'),
            'school_tagline': settings_dict.get('school_tagline', 'Nurturing Knowledge. Building Character.'),
            'school_phone': settings_dict.get('school_phone', '+91 79790 48493'),
            'school_email': settings_dict.get('school_email', 'sanskarpublicskl2000@gmail.com'),
            'school_address': settings_dict.get('school_address', 'Sanskar Knowledge Park, Sector 14, Education City'),
            'admissions_open': settings_dict.get('admissions_open', 'true') == 'true'
        }

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # Auto create and seed on start
    with app.app_context():
        db.create_all()
        # Seed if empty
        if WebsiteSetting.query.count() == 0:
            seed_database(app)

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
