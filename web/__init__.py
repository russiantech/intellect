# web/__init__.py
#from web.extensions import *

from  web.extensions import (
    confiq_app, init_ext, make_available
)

def create_app(config_name):

    from flask import Flask
    app = Flask(__name__, instance_relative_config=True)

    # Debugging statements
    # print(f"Configuring app for: {config_name}")

    confiq_app(app, config_name) #configure app, it needs the Flask instance to work

    init_ext(app) #initialize extensions. imported from extensions.py, also needs a configured Flask instance 
    
    # Debugging statements
    # print("App configured and extensions initialized")
    
    app.context_processor(make_available) #make some-data available through-out
    
    #//blue-prints
    
    from web.auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    
    from web.main.routes import main
    app.register_blueprint(main)
    
    from web.chatme.routes import chat
    app.register_blueprint(chat)

    from web.pays.routes import pay
    app.register_blueprint(pay)


    from web.errors.handlers import errors
    app.register_blueprint(errors)

    from web.socketio.route import socket_bp
    app.register_blueprint(socket_bp)

    #My-New APi Endpoints
    from web.apis.x_courses.x_recommend_bak import x_recommend_bp
    app.register_blueprint(x_recommend_bp)

    from web.apis.x_courses.x_categories import x_category_bp
    app.register_blueprint(x_category_bp)

    from web.apis.x_courses.x_course import x_course_bp
    app.register_blueprint(x_course_bp)

    from web.apis.x_courses.x_lesson import x_lesson_bp
    app.register_blueprint(x_lesson_bp)

    from web.apis.x_courses.x_topic import x_topic_bp
    app.register_blueprint(x_topic_bp)

    from web.apis.x_courses.x_path import x_path_bp
    app.register_blueprint(x_path_bp)
    
    from slugify import slugify
    from web.utils import time_ago, user_role
    from nltk.tokenize import sent_tokenize

    app.jinja_env.filters['time_ago'] = time_ago.timeAgo
    app.jinja_env.filters['type'] = user_role.type
    app.jinja_env.filters['sent_tokenize'] = sent_tokenize
    app.jinja_env.filters['slugify'] = slugify
    
    with app.app_context():
        from web.models import db
        db.create_all()

    return app
