
# Resume-Job Compatibility Analyzer System

## 🎯 What is this System?

This is a smart web application that helps job seekers understand how well their resume matches a specific job posting. Think of it like a compatibility test between your resume and a job description - it gives you a percentage score and tells you what you can improve!

## 🏗️ System Architecture (How Everything Works Together)

```
User Interface (Web Pages) 
        ↓
Flask Web Server (Backend)
        ↓
Machine Learning Engine (Brain)
        ↓
Database (Storage)
```

## 📱 Role of Each Page

### 1. **Home Page (`index.html`)**
- **Purpose**: Welcome page for visitors
- **What it does**: Introduces the system and lets users try a free analysis without registering

### 2. **Registration/Login Pages (`auth/register.html`, `auth/login.html`)**
- **Purpose**: User account management
- **What they do**: Allow users to create accounts and login to save their analysis history

### 3. **Dashboard (`dashboard.html`)**
- **Purpose**: User's main control center
- **What it shows**: 
  - Total number of analyses done
  - Average compatibility score
  - Recent analysis history
  - Quick access to start new analysis

### 4. **Analysis Page (`analyze.html`)**
- **Purpose**: The main workspace where magic happens
- **What it contains**:
  - Text box for resume content
  - Text box for job description
  - "Use Saved Resume" toggle (lets users select from previously saved resumes)
  - Analyze button to start the comparison
  - Results display area

### 5. **Results Page (`results.html`)**
- **Purpose**: Shows the analysis results
- **What it displays**:
  - Compatibility percentage (like 75%)
  - Compatibility level (Excellent, Good, Fair, or Poor)
  - Skill breakdown by category
  - Specific recommendations for improvement

### 6. **History Page (`history.html`)**
- **Purpose**: Shows all past analyses
- **What it contains**: List of all previous resume-job comparisons with dates and scores

### 7. **Profile Page (`profile.html`)**
- **Purpose**: Account management and resume storage
- **Features**:
  - Edit personal information
  - Save multiple resumes for future use
  - Set default resume
  - Delete account option

## 🧠 How the Machine Learning Model Works

### Training Phase (Happens when system starts)

1. **Training Data Collection**:
   - The system has 4,926 real examples from LinkedIn, Indeed, and GitHub
   - Each example contains: a resume, job description, and compatibility label (high/medium/low)

2. **Text Processing**:
   - Converts all text to lowercase
   - Removes punctuation and common words (like "the", "and", "is")
   - Breaks text into individual words (tokens)

3. **Skill Categorization**:
   - Groups skills into 15 categories:
     - Programming languages (Python, Java, JavaScript)
     - Frameworks (React, Django, Spring)
     - Cloud platforms (AWS, Azure, Google Cloud)
     - DevOps tools (Docker, Kubernetes)
     - Databases (MySQL, MongoDB)
     - And 10 more categories...

4. **Model Training (Naive Bayes Algorithm)**:
   - Learns probability patterns from training data
   - Calculates: "If I see word X, what's the probability of high/medium/low compatibility?"
   - Creates a "vocabulary" of important words and their importance

### Prediction Phase (When user clicks "Analyze")

1. **Text Preprocessing**: Same cleaning process as training
2. **Feature Extraction**: Identifies skills and experience level
3. **Probability Calculation**: Uses trained model to predict compatibility class
4. **Score Generation**: Combines multiple factors for final percentage

## 🔄 What Happens When You Click "Analyze"

Let me walk you through the complete process step by step:

### Step 1: Input Validation
```
User inputs resume and job description
        ↓
System checks if both texts have at least 10 characters
        ↓
If valid, proceed; if not, show error message
```

### Step 2: Text Processing
```
Raw text: "I have 5 years of experience with Python and AWS"
        ↓
Lowercase: "i have 5 years of experience with python and aws"
        ↓
Remove punctuation and common words: "5 years experience python aws"
        ↓
Extract tokens: ["5", "years", "experience", "python", "aws"]
```

### Step 3: Feature Extraction

**A. Skill Detection:**
- Searches for keywords in 15 skill categories
- Example: "python" → Programming category, "aws" → Cloud category

**B. Experience Level Detection:**
- Looks for patterns like "5 years", "senior", "junior"
- Classifies as: Junior (0-2 years), Mid (2-5 years), Senior (5+ years)

**C. Text Similarity:**
- Compares common words between resume and job description
- Uses Jaccard similarity: (shared words) / (total unique words)

### Step 4: Machine Learning Prediction

**Naive Bayes Calculation:**
```
For each compatibility class (high, medium, low):
    Start with base probability of that class
    For each word in the text:
        Multiply by probability of seeing that word in that class
    
Pick the class with highest probability
```

### Step 5: Score Generation

The final compatibility score combines 4 factors:
1. **ML Prediction (40%)**: From Naive Bayes model
2. **Skill Match (35%)**: Percentage of required skills found in resume
3. **Text Similarity (15%)**: How similar the texts are overall
4. **Experience Match (10%)**: Whether experience levels align

**Example Calculation:**
```
ML Prediction: 0.7 (70%)
Skill Match: 0.6 (60% of required skills found)
Text Similarity: 0.4 (40% text overlap)
Experience Match: 1.0 (perfect match)

Final Score = (0.7×0.4) + (0.6×0.35) + (0.4×0.15) + (1.0×0.1)
            = 0.28 + 0.21 + 0.06 + 0.10
            = 0.65 = 65%
```

### Step 6: Compatibility Level Assignment
```
Score ≥ 80% → "Excellent Match"
Score ≥ 60% → "Good Match"
Score ≥ 40% → "Fair Match"
Score < 40% → "Poor Match"
```

## 💡 How Recommendations are Generated

### 1. Skill Gap Analysis
```
Job requires: Python, AWS, Docker, React
Resume has: Python, React
Missing: AWS, Docker

Recommendation: "Consider learning AWS, Docker"
Priority: High (missing 50% of required skills)
Impact: "Can improve compatibility by 10%"
```

### 2. Experience Gap Analysis
```
Job requires: Senior level (5+ years)
Resume shows: Junior level (1 year)

Recommendation: "Gain more hands-on project experience"
Priority: High
Impact: "Can improve compatibility by 20%"
```

### 3. General Improvements
If no specific gaps found:
```
Recommendation: "Highlight specific achievements and quantifiable results"
Priority: Low
Impact: "Can improve compatibility by 5-10%"
```

## 🗄️ Database Structure

The system stores:
- **User accounts**: Name, email, password (encrypted)
- **Analysis history**: Resume text, job description, scores, dates
- **Saved resumes**: Multiple resumes per user for convenience

## 🔧 Technical Components

### Backend (Python Flask)
- **app.py**: Main server application
- **routes.py**: Handles web page requests and API calls
- **ml_engine.py**: Contains the machine learning brain
- **models.py**: Database structure definitions
- **auth.py**: User authentication system

### Frontend (HTML/CSS/JavaScript)
- **HTML templates**: Structure of web pages
- **CSS files**: Styling and appearance
- **JavaScript**: Interactive features and API calls

### Machine Learning Engine
- **Custom Naive Bayes**: Built from scratch (no external libraries)
- **Text preprocessing**: Custom tokenization and cleaning
- **Skill extraction**: Pattern matching for technical skills
- **Experience parsing**: Regex patterns for experience levels

## 🚀 System Flow Summary

```
1. User Registration/Login → Creates account in database
2. Navigate to Analysis → Loads analysis page
3. Input Resume & Job → Text entered in forms
4. Optional: Select Saved Resume → Loads pre-saved resume
5. Click Analyze → Sends data to backend
6. Text Processing → Cleans and prepares text
7. ML Analysis → Model predicts compatibility
8. Score Calculation → Combines multiple factors
9. Generate Recommendations → Identifies improvement areas
10. Display Results → Shows score, breakdown, recommendations
11. Optional: Save Analysis → Stores in database for history
```

## 🎓 Key Learning Points for Students

1. **Machine Learning isn't magic**: It's statistics and pattern recognition
2. **Data quality matters**: Good training data = better predictions
3. **Multiple factors**: Real-world problems need multiple approaches combined
4. **User experience**: Technical accuracy must be presented in understandable ways
5. **Iterative improvement**: System learns and improves with more data

## 🔍 System Advantages

1. **No external dependencies**: Custom ML engine means full control
2. **Real training data**: Based on actual job postings and resumes
3. **Practical recommendations**: Actionable advice for improvement
4. **User-friendly**: Complex analysis presented simply
5. **Scalable**: Can handle multiple users and analyses simultaneously

This system demonstrates how machine learning can solve real-world problems by combining text processing, statistical analysis, and user-friendly design!
