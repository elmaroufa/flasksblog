from flask import Flask
#from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
app = Flask(__name__)
app.config.from_object(Config)
#bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from app import routes, models
