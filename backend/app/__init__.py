from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from app.routes.estimation import estimation_bp
from app.routes.finance import finance_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)
    CORS(app)

    app.register_blueprint(estimation_bp, url_prefix='/api')
    app.register_blueprint(finance_bp, url_prefix='/api/finance')

    return app
