from flask import Blueprint, render_template
from flask_login import login_user, logout_user, login_required
from .extensions import db, bcrypt
from .models import User, Item

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('home.html')
