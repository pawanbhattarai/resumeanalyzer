
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from ml_engine import ResumeAnalyzer
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize ML engine
analyzer = ResumeAnalyzer()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/training-info')
def training_info():
    """Training data information page"""
    return render_template('training_info.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze resume-job compatibility"""
    try:
        data = request.get_json()
        
        if not data or 'resume' not in data or 'job_description' not in data:
            return jsonify({'error': 'Missing resume or job description'}), 400
        
        resume_text = data['resume'].strip()
        job_text = data['job_description'].strip()
        
        if not resume_text or not job_text:
            return jsonify({'error': 'Resume and job description cannot be empty'}), 400
        
        # Perform analysis
        result = analyzer.analyze_compatibility(resume_text, job_text)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/status')
def status():
    """API status check"""
    return jsonify({
        'status': 'ok',
        'ml_engine_trained': analyzer.is_trained(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
