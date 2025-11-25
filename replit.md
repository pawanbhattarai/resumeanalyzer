# Resume-Job Compatibility Analyzer System

## Project Overview

This is a smart web application built with Flask that helps job seekers understand how well their resume matches a specific job posting. It uses a custom-built machine learning engine (Naive Bayes classifier) to analyze compatibility between resumes and job descriptions.

## Tech Stack

- **Backend**: Python 3.11, Flask 3.1.2
- **Database**: SQLite (development), PostgreSQL-ready
- **ML Engine**: Custom Naive Bayes implementation (no external ML libraries)
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Flask-Login with bcrypt password hashing
- **Email**: Flask-Mail for verification and password reset

## Project Structure

```
.
├── app.py                  # Main Flask application
├── routes.py               # Application routes and API endpoints
├── auth.py                 # Authentication blueprint
├── models.py               # Database models (User, AnalysisHistory, SavedResume)
├── ml_engine.py            # Custom ML engine with Naive Bayes classifier
├── forms.py                # WTForms for form validation
├── extensions.py           # Flask extensions initialization
├── data/
│   └── real_training_data.py  # Training dataset (4,926 examples)
├── templates/              # HTML templates
├── static/                 # CSS, JavaScript, images
└── instance/               # SQLite database location
```

## Key Features

1. **Resume Analysis**: Compare resumes against job descriptions with ML-powered compatibility scoring
2. **User Authentication**: Secure registration, login, and password reset
3. **Analysis History**: Save and review past analyses
4. **Saved Resumes**: Store multiple resumes for quick analysis
5. **Detailed Insights**: Skill matching, experience level comparison, and improvement recommendations

## Environment Variables

The following environment variables are configured:

- `SESSION_SECRET`: Flask session secret key (managed as secret)
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`: Email configuration (optional)

## Development Setup

The project is configured to run in Replit with:
- Flask development server on port 5000
- Hot reload enabled for development
- Cache disabled for proper preview in Replit iframe

## Deployment

The project is configured for deployment using:
- **Type**: Autoscale (stateless, scales with traffic)
- **Server**: Gunicorn with 4 workers
- **Port**: 5000
- **Database**: Can be migrated to PostgreSQL for production

## ML Engine Details

The custom ML engine uses:
- **Naive Bayes Classification**: Trained on 4,926 real resume-job pairs
- **Skill Extraction**: 15 predefined skill categories (programming, frameworks, cloud, etc.)
- **Multi-factor Scoring**: Combines ML prediction (40%), skill matching (35%), text similarity (15%), and experience match (10%)
- **Experience Level Detection**: Uses regex patterns to identify junior/mid/senior levels

## Recent Changes

- 2025-11-25: Complete website redesign with modern UI
  - **Hero Section**: Added modern hero with floating resume/recruiter cards, AI badge, and stats
  - **Why Section**: Created Q&A format explaining importance of resume-job compatibility
  - **How It Works**: Implemented 3-step process visualization with feature cards
  - **Analyze Section**: Redesigned input interface with modern card layout
  - **CTA Section**: Added compelling call-to-action with gradient background
  - **Footer**: Created comprehensive footer with links, social media, and branding
  - **Navigation**: Implemented smooth scrolling and active state management
  - **CSS**: Added extensive modern styling with gradients, animations, hover effects
  - **Responsive Design**: Made all sections mobile-friendly with media queries
  - **Visual Design**: Used modern color gradients, floating animations, and micro-interactions

- 2025-11-25: Initial setup for Replit environment
  - Installed Python 3.11 and all dependencies
  - Configured Flask to bind to 0.0.0.0:5000 for Replit preview
  - Added cache control headers to disable caching
  - Set up workflow for development server
  - Configured deployment with Gunicorn for production
  - Set DATABASE_URL to use absolute path for SQLite

## User Preferences

- Modern, clean, and professional design
- Easy navigation between sections
- Visual appeal with gradients and animations
- Mobile-responsive layout
