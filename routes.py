from flask import render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import login_required, current_user
from models import User, AnalysisHistory, SavedResume
from forms import AnalysisForm, ProfileForm, ChangePasswordForm, SavedResumeForm
from app import db
from ml_engine import ResumeAnalyzer
from datetime import datetime

# Initialize ML engine
analyzer = ResumeAnalyzer()

def register_routes(app):
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

    @app.route('/profile')
    @login_required
    def profile():
        """User profile management page"""
        form = ProfileForm(
            original_username=current_user.username,
            original_email=current_user.email,
            obj=current_user
        )
        password_form = ChangePasswordForm()
        resume_form = SavedResumeForm()
        
        # Get user's saved resumes
        saved_resumes = SavedResume.query.filter_by(user_id=current_user.id)\
                                        .order_by(SavedResume.is_default.desc(), SavedResume.updated_at.desc())\
                                        .all()
        
        return render_template('profile.html', 
                             form=form, 
                             password_form=password_form,
                             resume_form=resume_form,
                             saved_resumes=saved_resumes)

    @app.route('/profile/update', methods=['POST'])
    @login_required
    def update_profile():
        """Update user profile information"""
        form = ProfileForm(
            original_username=current_user.username,
            original_email=current_user.email
        )
        
        if form.validate_on_submit():
            try:
                current_user.first_name = form.first_name.data.strip()
                current_user.last_name = form.last_name.data.strip()
                current_user.username = form.username.data.lower().strip()
                current_user.email = form.email.data.lower().strip()
                
                db.session.commit()
                flash('Profile updated successfully!', 'success')
                
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating profile: {str(e)}', 'error')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{getattr(form, field).label.text}: {error}', 'error')
        
        return redirect(url_for('profile'))

    @app.route('/profile/change-password', methods=['POST'])
    @login_required
    def change_password():
        """Change user password"""
        form = ChangePasswordForm()
        
        if form.validate_on_submit():
            if current_user.check_password(form.current_password.data):
                try:
                    current_user.set_password(form.new_password.data)
                    db.session.commit()
                    flash('Password changed successfully!', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash(f'Error changing password: {str(e)}', 'error')
            else:
                flash('Current password is incorrect.', 'error')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{getattr(form, field).label.text}: {error}', 'error')
        
        return redirect(url_for('profile'))

    @app.route('/profile/delete-history', methods=['POST'])
    @login_required
    def delete_analysis_history():
        """Delete all user's analysis history"""
        try:
            AnalysisHistory.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            flash('All analysis history deleted successfully.', 'success')
            return jsonify({'status': 'success'})
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting history: {str(e)}', 'error')
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @app.route('/profile/delete-account', methods=['POST'])
    @login_required
    def delete_account():
        """Delete user account and all associated data"""
        try:
            user_id = current_user.id
            
            # Delete all analysis history first (due to foreign key constraint)
            AnalysisHistory.query.filter_by(user_id=user_id).delete()
            
            # Delete all saved resumes
            SavedResume.query.filter_by(user_id=user_id).delete()
            
            # Delete the user account
            db.session.delete(current_user)
            db.session.commit()
            
            flash('Account deleted successfully.', 'info')
            return jsonify({'status': 'success'})
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting account: {str(e)}', 'error')
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @app.route('/profile/save-resume', methods=['POST'])
    @login_required
    def save_resume():
        """Save a new resume"""
        form = SavedResumeForm()
        
        if form.validate_on_submit():
            try:
                # If setting as default, unset other defaults
                if form.is_default.data:
                    SavedResume.query.filter_by(user_id=current_user.id, is_default=True)\
                                   .update({'is_default': False})
                
                resume = SavedResume(
                    user_id=current_user.id,
                    title=form.title.data.strip(),
                    content=form.content.data.strip(),
                    is_default=form.is_default.data
                )
                
                db.session.add(resume)
                db.session.commit()
                
                flash('Resume saved successfully!', 'success')
                
            except Exception as e:
                db.session.rollback()
                flash(f'Error saving resume: {str(e)}', 'error')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{getattr(form, field).label.text}: {error}', 'error')
        
        return redirect(url_for('profile'))

    @app.route('/profile/edit-resume/<int:resume_id>', methods=['POST'])
    @login_required
    def edit_resume(resume_id):
        """Edit an existing resume"""
        resume = SavedResume.query.filter_by(id=resume_id, user_id=current_user.id).first_or_404()
        
        data = request.get_json()
        
        try:
            resume.title = data.get('title', '').strip()
            resume.content = data.get('content', '').strip()
            
            # Handle default setting
            if data.get('is_default', False):
                SavedResume.query.filter_by(user_id=current_user.id, is_default=True)\
                                .update({'is_default': False})
                resume.is_default = True
            
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Resume updated successfully'})
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @app.route('/profile/delete-resume/<int:resume_id>', methods=['POST'])
    @login_required
    def delete_resume(resume_id):
        """Delete a saved resume"""
        resume = SavedResume.query.filter_by(id=resume_id, user_id=current_user.id).first_or_404()
        
        try:
            db.session.delete(resume)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Resume deleted successfully'})
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @app.route('/api/saved-resumes')
    @login_required
    def get_saved_resumes():
        """Get user's saved resumes for analysis page"""
        resumes = SavedResume.query.filter_by(user_id=current_user.id)\
                                  .order_by(SavedResume.is_default.desc(), SavedResume.updated_at.desc())\
                                  .all()
        
        return jsonify([{
            'id': resume.id,
            'title': resume.title,
            'content': resume.content,
            'is_default': resume.is_default,
            'created_at': resume.created_at.isoformat()
        } for resume in resumes])

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