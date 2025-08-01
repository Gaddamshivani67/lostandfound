from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from .models import db, User, Item

# ✅ Create a Blueprint
routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('index.html')

@routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        roll_number = request.form['roll_no']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(email=email).first():
            flash('Email already registered.')
            return redirect(url_for('routes.signup'))

        user = User(username=name, name=name, roll_number=roll_number, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Signup successful. Please log in.')
        return redirect(url_for('routes.login'))

    return render_template('signup.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            print(f"Email entered: {email}, Password entered: {password}")
            
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                print("Login successful")
                return redirect(url_for('routes.dashboard'))
            else:
                flash("Invalid email or password", "danger")
                return redirect(url_for('routes.login'))
        except Exception as e:
            import traceback
            print("Error during login:\n", traceback.format_exc())
            flash("An unexpected error occurred.", "danger")
            return redirect(url_for('routes.login'))
    return render_template('login.html')




@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('routes.home'))

@routes.route('/dashboard')
@login_required
def dashboard():
    items = Item.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', items=items)

@routes.route('/post', methods=['GET', 'POST'])
@login_required
def post_item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_type = request.form['item_type']
        description = request.form['description']
        status = request.form['status']
        branch = request.form['branch']

        new_item = Item(
            item_name=item_name,
            item_type=item_type,
            description=description,
            status=status,
            branch=branch,
            user_id=current_user.id
        )

        db.session.add(new_item)
        db.session.commit()
        flash('Item posted successfully!', 'success')
        return redirect(url_for('routes.dashboard'))

    return render_template('post_item.html')

@routes.route('/items')
def view_items():
    items = Item.query.all()
    return render_template('view_items.html', items=items)

@routes.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Password reset successfully.', 'success')
            return redirect(url_for('routes.login'))
        else:
            flash('User not found.', 'danger')
    return render_template('forgot_password.html')
