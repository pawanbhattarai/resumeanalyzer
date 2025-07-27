
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user
from models import db, User, AnalysisHistory
from forms import AnalysisForm
from auth import auth
from email_service import mail
from ml_engine import ResumeAnalyzer
import os
import json
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///resume_analyzer.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@resumeanalyzer.com')

# Initialize extensions
CORS(app)
db.init_app(app)
mail.init_app(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth, url_prefix='/auth')

# Initialize ML engine
analyzer = ResumeAnalyzer()

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """Landing page with free analysis option"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # Check if user has already used their free analysis
    has_used_free = session.get('used_free_analysis', False)
    
    return render_template('index.html', has_used_free=has_used_free)

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    # Get user's recent analyses
    recent_analyses = AnalysisHistory.query.filter_by(user_id=current_user.id)\
                                          .order_by(AnalysisHistory.created_at.desc())\
                                          .limit(5).all()
    
    # Get statistics
    total_analyses = AnalysisHistory.query.filter_by(user_id=current_user.id).count()
    
    avg_score = db.session.query(db.func.avg(AnalysisHistory.compatibility_score))\
                         .filter_by(user_id=current_user.id).scalar()
    avg_score = round(avg_score, 2) if avg_score else 0
    
    return render_template('dashboard.html', 
                         recent_analyses=recent_analyses,
                         total_analyses=total_analyses,
                         avg_score=avg_score)

@app.route('/analyze', methods=['GET', 'POST'])
@login_required
def analyze():
    """Resume analysis page"""
    form = AnalysisForm()
    
    if form.validate_on_submit():
        try:
            # Perform analysis
            result = analyzer.analyze_compatibility(
                form.resume_text.data, 
                form.job_description.data
            )
            
            # Save to history if requested
            if form.save_analysis.data:
                analysis = AnalysisHistory(
                    user_id=current_user.id,
                    job_title=form.job_title.data or 'Untitled Position',
                    company_name=form.company_name.data or 'Unknown Company',
                    compatibility_score=result['compatibility_score'],
                    compatibility_level=result['compatibility_level'],
                    resume_text=form.resume_text.data,
                    job_description=form.job_description.data,
                    analysis_result=result
                )
                db.session.add(analysis)
                db.session.commit()
                flash('Analysis saved to your history!', 'success')
            
            return render_template('results.html', result=result, form=form)
            
        except Exception as e:
            flash(f'Analysis failed: {str(e)}', 'error')
    
    return render_template('analyze.html', form=form)

@app.route('/history')
@login_required
def history():
    """Analysis history page"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    analyses = AnalysisHistory.query.filter_by(user_id=current_user.id)\
                                   .order_by(AnalysisHistory.created_at.desc())\
                                   .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('history.html', analyses=analyses)

@app.route('/history/<int:analysis_id>')
@login_required
def view_analysis(analysis_id):
    """View specific analysis"""
    analysis = AnalysisHistory.query.filter_by(id=analysis_id, user_id=current_user.id).first_or_404()
    return render_template('view_analysis.html', analysis=analysis)

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for analysis (for AJAX requests)"""
    try:
        data = request.get_json()
        
        if not data or 'resume' not in data or 'job_description' not in data:
            return jsonify({'error': 'Missing resume or job description'}), 400
        
        # Check if user is authenticated or can use free analysis
        if not current_user.is_authenticated:
            if session.get('used_free_analysis', False):
                return jsonify({
                    'error': 'Free analysis limit reached. Please register for unlimited access.',
                    'require_login': True
                }), 401
            # Mark free analysis as used
            session['used_free_analysis'] = True
        
        resume_text = data['resume'].strip()
        job_text = data['job_description'].strip()
        
        if not resume_text or not job_text:
            return jsonify({'error': 'Resume and job description cannot be empty'}), 400
        
        # Perform analysis
        result = analyzer.analyze_compatibility(resume_text, job_text)
        
        # Add free analysis indicator
        if not current_user.is_authenticated:
            result['is_free_analysis'] = True
            result['message'] = 'This was your free analysis! Register for unlimited access and to save your results.'
        
        # Save to history if user is authenticated and requested
        if current_user.is_authenticated and data.get('save_analysis', False):
            analysis = AnalysisHistory(
                user_id=current_user.id,
                job_title=data.get('job_title', 'Untitled Position'),
                company_name=data.get('company_name', 'Unknown Company'),
                compatibility_score=result['compatibility_score'],
                compatibility_level=result['compatibility_level'],
                resume_text=resume_text,
                job_description=job_text,
                analysis_result=result
            )
            db.session.add(analysis)
            db.session.commit()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/status')
def api_status():
    """API status check"""
    return jsonify({
        'status': 'ok',
        'ml_engine_trained': analyzer.is_trained(),
        'user_authenticated': current_user.is_authenticated,
        'version': '2.0.0'
    })

@app.route('/api/health')
def api_health():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/training-info')
def training_info():
    """Training data information page"""
    return render_template('training_info.html')

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Page Not Found</title></head>
    <body style="font-family: Arial; text-align: center; margin-top: 100px;">
        <h1>404 - Page Not Found</h1>
        <p>The page you're looking for doesn't exist.</p>
        <a href="/" style="color: #2563eb;">← Back to Home</a>
    </body>
    </html>
    """, 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Server Error</title></head>
    <body style="font-family: Arial; text-align: center; margin-top: 100px;">
        <h1>500 - Server Error</h1>
        <p>Something went wrong on our end.</p>
        <a href="/" style="color: #2563eb;">← Back to Home</a>
    </body>
    </html>
    """, 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
