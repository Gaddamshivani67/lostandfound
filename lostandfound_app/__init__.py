from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lostandfound.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    from lostandfound_app.routes import routes
    app.register_blueprint(routes)

    return app

app = create_app()
import traceback
@app.errorhandler(Exception)
def all_exception_handler(error):
    trace = traceback.format_exc()
    print("\n===== ERROR TRACEBACK =====")
    print(trace)
    print("===========================\n")
    return f"<h3>Internal Server Error</h3><pre>{trace}</pre>", 500

