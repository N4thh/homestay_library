from flask import Flask, send_from_directory
import os
from utils import format_price
import json
from PIL import Image
from database import init_db
from models import HomestayJSONManager, User
from auth import UserLogin
import base64
from datetime import timedelta
from extensions import init_extensions, login_manager
from config import config
import logging
from logging.handlers import RotatingFileHandler

TMP_DIR = '/tmp'

def create_app(config_name='default'):
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    init_extensions(app)
    
    # Configure logging
    log_dir = os.path.join(TMP_DIR, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    if not app.debug:
        file_handler = RotatingFileHandler(os.path.join(log_dir, 'homestay.log'), maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Homestay startup')
    
    # Add cache headers to static files
    @app.after_request
    def add_header(response):
        if 'Cache-Control' not in response.headers:
            if response.mimetype in ['text/css', 'application/javascript']:
                response.headers['Cache-Control'] = 'public, max-age=31536000'  # 1 year
            elif response.mimetype in ['image/jpeg', 'image/png', 'image/webp']:
                response.headers['Cache-Control'] = 'public, max-age=2592000'  # 30 days
            else:
                response.headers['Cache-Control'] = 'public, max-age=3600'  # 1 hour
        return response
    
    # Custom static file handler with fallback
    @app.route('/static/<path:filename>')
    def custom_static(filename):
        try:
            return send_from_directory(app.static_folder, filename)
        except FileNotFoundError:
            # Fallback to default image for missing images
            if filename.startswith('images/') and not filename.endswith('default.jpg'):
                return send_from_directory(app.static_folder, 'images/default.jpg')
            return send_from_directory(app.static_folder, filename), 404
    
    @login_manager.user_loader
    def load_user(user_id):
        user_data = User.get_by_phone(user_id)
        if user_data:
            return UserLogin(user_data)
        return None
    
    # Add custom filters to Jinja
    app.jinja_env.filters['format_price'] = format_price
    app.jinja_env.filters['b64encode'] = lambda data: base64.b64encode(data).decode('utf-8')
    
    # Initialize database
    init_db()
    
    # Initialize JSON data for homestays
    init_homestay_data()
    
    # Register routes
    from routes import register_routes
    register_routes(app)
    
    return app

def init_homestay_data():
    # Create a default image if it doesn't exist
    static_img_dir = os.path.join(TMP_DIR, 'static', 'images')
    os.makedirs(static_img_dir, exist_ok=True)
    default_img_path = os.path.join(static_img_dir, 'default.jpg')
    if not os.path.exists(default_img_path):
        img = Image.new('RGB', (800, 600), color = (76, 175, 80)) 
        img.save(default_img_path, optimize=True, quality=85)
    hero_bg_path = os.path.join(static_img_dir, 'new_bg.jpg')
    if not os.path.exists(hero_bg_path):
        hero_img = Image.new('RGB', (1920, 1080), color = (76, 175, 80))  
        hero_img.save(hero_bg_path, optimize=True, quality=85)

# Create application instance
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
