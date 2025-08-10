# Database Setup Guide

## Current Setup
- **Database Type:** PostgreSQL 16.9
- **Status:** ✅ Connected and Running
- **Tables:** Automatically created by Flask-SQLAlchemy

## Database Commands

### Check Database Status
```bash
# View tables in the database
python -c "from app import app, db; app.app_context().push(); print([table.name for table in db.metadata.tables.values()])"
```

### Database Operations
The application uses Flask-SQLAlchemy with automatic table creation. No manual migrations needed.

## Environment Variables (Already Set)
- `DATABASE_URL` - PostgreSQL connection string
- `PGHOST` - Database host
- `PGPORT` - Database port
- `PGUSER` - Database user
- `PGPASSWORD` - Database password
- `PGDATABASE` - Database name

## Models
- **User** - User accounts with authentication
- **AnalysisHistory** - Saved resume analyses
- **EmailVerification** - Email verification tokens
- **PasswordReset** - Password reset tokens

## For Local Development
1. Set up a local PostgreSQL database
2. Copy the environment variables from Replit
3. Update DATABASE_URL to point to your local database
4. Run: `python main.py`

The Flask app will automatically create all tables on first run.