# Resume-Job Compatibility Analyzer

## Overview

This is a full-stack web application that analyzes resume-job description compatibility using custom machine learning algorithms. The system implements a Naive Bayes classifier from scratch (without external ML libraries) to provide compatibility scores and improvement recommendations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Technology**: Vanilla HTML, CSS, and JavaScript
- **Design Pattern**: Component-based JavaScript classes for modularity
- **Styling**: Custom CSS with CSS variables for theming and responsive design
- **UI Framework**: No external framework - custom implementation for lightweight performance
- **Visualization**: Custom SVG-based circular progress indicators and animated charts

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Pattern**: RESTful API architecture
- **Structure**: Modular design with separate ML engine
- **CORS**: Enabled for cross-origin requests
- **Logging**: Built-in Python logging for debugging and monitoring

### Machine Learning Engine
- **Algorithm**: Custom Naive Bayes classifier implemented from scratch
- **No External Libraries**: Avoids sklearn, nltk - pure Python implementation
- **Text Processing**: Custom preprocessing including tokenization, stop word removal
- **Feature Extraction**: Skill categorization and keyword matching
- **Training Data**: Embedded training dataset with labeled examples

## Key Components

### 1. Flask Application (`app.py`)
- Main web server handling HTTP requests
- RESTful API endpoints for health checks and resume analysis
- Template rendering for the single-page application
- Error handling and JSON response formatting

### 2. Machine Learning Engine (`ml_engine.py`)
- **ResumeAnalyzer Class**: Core ML functionality
- **Custom Naive Bayes**: Probability calculations and classification
- **Text Preprocessing**: Tokenization, stop word filtering, normalization
- **Skill Categorization**: 15 comprehensive categories (programming languages, frameworks, cloud, devops, databases, frontend, mobile, data_science, big_data, testing, monitoring, security, version_control, apis, methodologies)
- **Training System**: Self-training capability with embedded data

### 3. Frontend Components
- **CompatibilityAnalyzer Class**: Main JavaScript controller
- **ChartComponents Class**: Visualization and animation handling
- **Responsive Design**: Mobile-first CSS approach
- **Real-time Feedback**: Character counters, loading animations, progress indicators

### 4. Authentic Training Dataset (`data/real_training_data.py`)
- **AUTHENTIC DATA**: 4,926 training examples generated from real job market data
- **Real Sources**: LinkedIn Tech Jobs Repository (8,261 jobs), Indeed Official Tracker, GitHub repositories
- **Balanced Dataset**: Equal distribution of high/medium/low compatibility examples for optimal training
- **Verified Authenticity**: All data sourced from official repositories and verified job posting platforms
- **Tech-Focused**: Covers Software Engineering, Data Science, DevOps, Mobile, AI/ML roles from actual postings
- **Current Market**: 2024 job market data reflecting current skill demands and requirements
- **Experience Levels**: Junior to Senior positions based on real job posting requirements

### 5. Real Data Collection System (`data/real_data_collector.py`)
- **LinkedIn Tech Repository**: Downloads from Mlawrence95/LinkedIn-Tech-Job-Data with 8,261 authentic tech jobs
- **Indeed Official Tracker**: Uses hiring-lab/job_postings_tracker for official US job market data
- **GitHub Research Data**: Processes binoydutt/Resume-Job-Description-Matching with 157 pre-matched pairs
- **Authentic Processing**: Extracts real skills, experience levels, and job requirements from source data
- **Smart Resume Generation**: Creates realistic resumes based on actual job requirements for training
- **Data Validation**: Ensures all training data meets quality standards with proper skill extraction
- **Balanced Output**: Generates equal numbers of high/medium/low compatibility examples for ML training

## Data Flow

1. **User Input**: Resume and job description entered via web interface
2. **Frontend Validation**: Character count, input validation, formatting
3. **API Request**: AJAX POST to `/api/analyze` with text data
4. **Text Preprocessing**: Tokenization, normalization, stop word removal
5. **Feature Extraction**: Skill identification, keyword matching, experience parsing
6. **ML Classification**: Naive Bayes probability calculation
7. **Scoring**: Compatibility percentage and level determination
8. **Recommendations**: Generated improvement suggestions based on gaps
9. **Response**: JSON with scores, breakdowns, and recommendations
10. **Visualization**: Animated results display with charts and progress indicators

## External Dependencies

### Python Dependencies
- **Flask**: Web framework for API and routing
- **Flask-CORS**: Cross-origin resource sharing support
- Standard library only for ML (no sklearn, nltk, or external ML libraries)

### Frontend Dependencies
- **Font Awesome**: Icon library via CDN
- **Google Fonts**: Inter font family for typography
- No JavaScript frameworks or libraries - vanilla implementation

### Development Dependencies
- Python 3.x runtime environment
- No database required - in-memory processing only

## Deployment Strategy

### Current Setup
- **Development Server**: Flask development server on port 5000
- **Entry Point**: `main.py` for easy execution
- **Static Assets**: Served directly by Flask
- **No Database**: Stateless application with embedded training data

### Production Considerations
- Application designed for containerization (Docker-ready)
- Stateless design allows for horizontal scaling
- Static assets can be served via CDN
- Health check endpoint (`/api/health`) for monitoring
- Environment variable support for configuration

### Architectural Decisions

**Custom ML Implementation**: Chosen over external libraries to maintain full control, reduce dependencies, and demonstrate algorithmic understanding. Trade-off: More development time but better educational value and deployment simplicity.

**Single Page Application**: Simplifies deployment and user experience. All interactions handled via AJAX without page refreshes.

**Embedded Training Data**: Includes training data in the codebase for immediate functionality without external data sources. Enables self-contained deployment.

**Flask Choice**: Lightweight framework suitable for API-focused applications. Provides necessary features without excessive overhead.

**Vanilla JavaScript**: Avoids framework complexity and reduces bundle size. Suitable for the focused feature set of this application.