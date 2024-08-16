# from flask import Flask

from slugify import slugify
from web.utils import time_ago, user_role, entry
from nltk.tokenize import sent_tokenize
from os import getenv

# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()

# from flask_login import LoginManager
# s_manager = LoginManager()

from flask_mail import Mail
mail = Mail()

#from flask_bootstrap import Bootstrap
#bootstrap = Bootstrap()

from flask_moment import Moment
moment = Moment()

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask_cors import CORS
cors = CORS()  # This will enable CORS for all routes
# cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:5001"}})


""" from flask_scrypt import Scrypt
scrypt = Scrypt() """

from flask_socketio import SocketIO
socketio = SocketIO(manage_session=False, cors_allowed_origins="*")

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

from flask_oauthlib.client import OAuth
oauth = OAuth()

from dotenv import load_dotenv
load_dotenv()

from redis import Redis
redis = Redis.from_url(getenv('redis_url', 'redis://'))

""" from flask_limiter import Limiter
limiter = Limiter(
    storage_uri=getenv('redis_url'),
    key_func=lambda: request.remote_addr,
)
 """
 
from flask_caching import Cache
from config import Config 
#cache = Cache()
cache = Cache(config=Config.REDIS_CONFIG)

from flask_migrate import Migrate
migrate = Migrate()


# openai.api_key = current_app.config['OPENAI_API_KEY']
from openai import OpenAI
client = OpenAI()

def make_available():

    # Create a context dictionary with the variables you want to make available
    app_socials = {}

    app_data = {
        'app_name': 'Intellect . Techa',
        'app_desc': 'Building a future where learning fits seamlessly into your everyday life.',
        'app_location': 'adesanya, lekki, lagos, nigeria.',
        'app_email': 'chrisjsmez@gmail.com',
        'app_logo': getenv('logo_url'),
        'fb_link': 'https://www.facebook.com/Chrisjsmes.fb.co',
        'x_link': 'https://twitter.com/chris_jsmes', 
        'instagram_link': 'https://www.instagram.com/chrisjsmz/',
        'linkedin_link': 'www.linkedin.com/in/chrisjsm',
        'dribble_link': ' https://dribbble.com/chrisjsm',
        'youtube_link': 'https://www.facebook.com/Chrisjsmes.fb.co',
        'utchannel_link': 'https://www.youtube.com/@russian_developer',
        #'utchannel_link': 'https://www.youtube.com/channel/UCrhOMa4obL92-HZHKCh4Kmw',
        # Add other data like logo URL
    }

    from web.apis.tokens import hash_auth
    context = {
        'hash_auth': hash_auth,
        **app_data #merge the 2 using dictionary unpacking ** operator.
    }
    
    return context

def init_ext(app):

    # client.init_app(app)

    from web.models import s_manager
    s_manager.init_app(app)

    from web.models import db
    db.init_app(app)

    migrate.init_app(app, db)

    cors.init_app(app)

    csrf.init_app(app)
    #f_session.init_app(app) #enable this on cpanel for file-session type, good alternative is redis-server instead.
    bcrypt.init_app(app)

    # scrypt.init_app(app)

    # s_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    oauth.init_app(app)
    # limiter.init_app(app)
    socketio.init_app(app, manage_session=False, async_mode='threading', cors_allowed_origins="*")
    # socketio.init_app(app)
    #cache.init_app(app, config=app.config['REDIS_CONFIG'])
    cache.init_app(app)
    

def confiq_app(app, config_name):
    from config import app_config
    app.config.from_object(app_config[config_name])
    
    from elasticsearch import Elasticsearch
    # print(app.config['ELASTICSEARCH_URL'])
    # app.elasticsearch = Elasticsearch([getenv('ELASTICSEARCH_URL', None)]) # Create an Elasticsearch client instance
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']])


    if config_name == 'production':
        app.config.from_object('config.ProductionConfig')
        
    elif config_name == 'development':
        app.config.from_object('config.DevelopmentConfig')
    



