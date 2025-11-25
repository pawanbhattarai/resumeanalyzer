from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from extensions import db
from models import User
from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app
from datetime import datetime
from forms import RegistrationForm, LoginForm
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Create new user (no email verification needed)
            user = User(
                username=form.username.data.lower().strip(),
                email=form.email.data.lower().strip(),
                first_name=form.first_name.data.strip(),
                last_name=form.last_name.data.strip(),
                is_verified=True  # Auto-verify since we removed email verification
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration error: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'error')
    
    return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        
        if user and user.check_password(form.password.data):
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            login_user(user, remember=form.remember_me.data)
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('dashboard')
            
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(next_page)
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))