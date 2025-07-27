import os
import json
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from ml_engine import ResumeAnalyzer

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key-for-development")

# Enable CORS for API calls
CORS(app)

# Initialize ML engine
analyzer = ResumeAnalyzer()

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/training-info')
def training_info():
    """Serve the training data information page"""
    return render_template('training_info.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        return jsonify({
            'status': 'healthy',
            'model_trained': analyzer.is_trained(),
            'version': '1.0.0'
        }), 200
    except Exception as e:
        logging.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    """Analyze resume-job compatibility"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400
        
        resume_text = data.get('resume', '').strip()
        job_description = data.get('job_description', '').strip()
        
        # Validate input
        if not resume_text or len(resume_text) < 10:
            return jsonify({
                'error': 'Resume text is too short (minimum 10 characters)'
            }), 400
            
        if not job_description or len(job_description) < 10:
            return jsonify({
                'error': 'Job description is too short (minimum 10 characters)'
            }), 400
        
        # Perform analysis
        result = analyzer.analyze_compatibility(resume_text, job_description)
        
        return jsonify(result), 200
        
    except Exception as e:
        logging.error(f"Analysis failed: {str(e)}")
        return jsonify({
            'error': 'Analysis failed. Please try again.',
            'details': str(e)
        }), 500

@app.route('/api/train', methods=['POST'])
def retrain_model():
    """Retrain the ML model"""
    try:
        data = request.get_json()
        
        # Use default training data if none provided
        training_data = data.get('training_data', None) if data else None
        
        analyzer.train_model(training_data)
        
        return jsonify({
            'status': 'success',
            'message': 'Model retrained successfully'
        }), 200
        
    except Exception as e:
        logging.error(f"Training failed: {str(e)}")
        return jsonify({
            'error': 'Training failed',
            'details': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
