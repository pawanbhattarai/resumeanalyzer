
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from models import User, EmailVerification, PasswordReset, db
from forms import RegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from email_service import send_verification_email, send_password_reset_email
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Create new user
            user = User(
                username=form.username.data.lower().strip(),
                email=form.email.data.lower().strip(),
                first_name=form.first_name.data.strip(),
                last_name=form.last_name.data.strip()
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            # Send verification email
            if send_verification_email(user):
                flash('Registration successful! Please check your email to verify your account.', 'success')
            else:
                flash('Registration successful! However, we could not send the verification email. Please contact support.', 'warning')
            
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration error: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'error')
    
    return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        
        if user and user.check_password(form.password.data):
            if not user.is_verified:
                flash('Please verify your email address before logging in. Check your inbox for the verification link.', 'warning')
                return render_template('auth/login.html', form=form)
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            login_user(user, remember=form.remember_me.data)
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.dashboard')
            
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
    return redirect(url_for('main.index'))

@auth.route('/verify-email/<token>')
def verify_email(token):
    verification = EmailVerification.query.filter_by(token=token).first()
    
    if not verification:
        flash('Invalid verification link.', 'error')
        return redirect(url_for('auth.login'))
    
    if not verification.is_valid():
        flash('Verification link has expired. Please request a new one.', 'error')
        return redirect(url_for('auth.resend_verification'))
    
    # Verify the user
    user = verification.user
    user.is_verified = True
    verification.is_used = True
    
    db.session.commit()
    
    flash('Email verified successfully! You can now log in.', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/resend-verification', methods=['GET', 'POST'])
def resend_verification():
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        user = User.query.filter_by(email=email).first()
        
        if user:
            if user.is_verified:
                flash('This email is already verified.', 'info')
                return redirect(url_for('auth.login'))
            
            if send_verification_email(user):
                flash('Verification email sent! Please check your inbox.', 'success')
            else:
                flash('Failed to send verification email. Please try again later.', 'error')
        else:
            flash('No account found with this email address.', 'error')
    
    return render_template('auth/resend_verification.html')

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        
        if user:
            if send_password_reset_email(user):
                flash('Password reset instructions sent to your email.', 'info')
            else:
                flash('Failed to send reset email. Please try again later.', 'error')
        else:
            # Don't reveal if email exists for security
            flash('If an account with this email exists, you will receive password reset instructions.', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html', form=form)

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    reset_token = PasswordReset.query.filter_by(token=token).first()
    
    if not reset_token or not reset_token.is_valid():
        flash('Invalid or expired reset link. Please request a new one.', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = reset_token.user
        user.set_password(form.password.data)
        reset_token.is_used = True
        
        db.session.commit()
        
        flash('Password reset successful! You can now log in with your new password.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form, token=token)

@auth.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', user=current_user)
