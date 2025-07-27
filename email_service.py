
from flask import current_app, url_for, render_template_string
from flask_mail import Mail, Message
from models import User, EmailVerification, PasswordReset, db
import os

mail = Mail()

def send_verification_email(user):
    """Send email verification to new user"""
    try:
        # Create verification token
        verification = EmailVerification(user.id)
        db.session.add(verification)
        db.session.commit()
        
        # Create verification URL
        verify_url = url_for('auth.verify_email', token=verification.token, _external=True)
        
        # Email template
        email_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #2563eb; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background: #f9f9f9; }}
                .button {{ display: inline-block; padding: 12px 24px; background: #2563eb; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to Resume Analyzer!</h1>
                </div>
                <div class="content">
                    <h2>Hi {user.first_name},</h2>
                    <p>Thank you for signing up for our Resume-Job Compatibility Analyzer!</p>
                    <p>To complete your registration and start analyzing your resume compatibility, please verify your email address:</p>
                    <p><a href="{verify_url}" class="button">Verify My Email</a></p>
                    <p>If the button doesn't work, copy and paste this link in your browser:</p>
                    <p><a href="{verify_url}">{verify_url}</a></p>
                    <p>This verification link will expire in 24 hours.</p>
                    <p>If you didn't create this account, please ignore this email.</p>
                </div>
                <div class="footer">
                    <p>© 2025 Resume-Job Compatibility Analyzer</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = Message(
            subject='Verify Your Email - Resume Analyzer',
            recipients=[user.email],
            html=email_body,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        
        mail.send(msg)
        return True
        
    except Exception as e:
        current_app.logger.error(f"Failed to send verification email: {str(e)}")
        return False

def send_password_reset_email(user):
    """Send password reset email"""
    try:
        # Create reset token
        reset_token = PasswordReset(user.id)
        db.session.add(reset_token)
        db.session.commit()
        
        # Create reset URL
        reset_url = url_for('auth.reset_password', token=reset_token.token, _external=True)
        
        # Email template
        email_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #dc2626; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background: #f9f9f9; }}
                .button {{ display: inline-block; padding: 12px 24px; background: #dc2626; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Password Reset Request</h1>
                </div>
                <div class="content">
                    <h2>Hi {user.first_name},</h2>
                    <p>We received a request to reset your password for your Resume Analyzer account.</p>
                    <p>Click the button below to reset your password:</p>
                    <p><a href="{reset_url}" class="button">Reset My Password</a></p>
                    <p>If the button doesn't work, copy and paste this link in your browser:</p>
                    <p><a href="{reset_url}">{reset_url}</a></p>
                    <p>This reset link will expire in 1 hour.</p>
                    <p>If you didn't request this password reset, please ignore this email.</p>
                </div>
                <div class="footer">
                    <p>© 2025 Resume-Job Compatibility Analyzer</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = Message(
            subject='Password Reset - Resume Analyzer',
            recipients=[user.email],
            html=email_body,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        
        mail.send(msg)
        return True
        
    except Exception as e:
        current_app.logger.error(f"Failed to send password reset email: {str(e)}")
        return False
