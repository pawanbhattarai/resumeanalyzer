
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

## 🧠 How the Custom Machine Learning Engine Works

### Custom Implementation Philosophy
Our system implements machine learning **from scratch** without external ML libraries like scikit-learn or TensorFlow. This provides:
- **Full Control**: Complete understanding of every algorithm step
- **No Dependencies**: Lightweight deployment without heavy ML frameworks  
- **Educational Value**: Transparent algorithms you can inspect and understand
- **Custom Features**: Tailored specifically for resume-job matching

### Training Phase (Happens when system starts)

**1. Authentic Training Data Loading:**
```python
# From data/real_training_data.py - 4,926 real examples
REAL_TRAINING_DATA = [
    ('Mid Information Technology with 4 years of experience in python, aws, docker...',
     'Seeking Senior Python Developer with AWS experience...',
     "high"),
    # ... 4,925 more real examples
]
```

**2. Custom Text Preprocessing:**
```python
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation with regex
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Tokenize and filter stop words
    tokens = text.split()
    filtered_tokens = [token for token in tokens 
                      if token not in stop_words and len(token) > 2]
    
    return filtered_tokens

# Example:
# Input: "I'm a Senior Python Developer with 5+ years of AWS experience!"
# Output: ["senior", "python", "developer", "years", "aws", "experience"]
```

**3. Vocabulary Building:**
```python
def train_model(training_data):
    class_counts = Counter()  # Count of each compatibility class
    word_class_counts = defaultdict(Counter)  # Word counts per class
    vocabulary = set()  # All unique words
    
    for resume, job_desc, compatibility in training_data:
        combined_text = resume + " " + job_desc
        tokens = preprocess_text(combined_text)
        
        class_counts[compatibility] += 1
        vocabulary.update(tokens)
        
        # Count each word in each class
        for token in tokens:
            word_class_counts[compatibility][token] += 1
```

**4. Probability Calculation with Laplace Smoothing:**
```python
# Calculate class probabilities
total_docs = sum(class_counts.values())
class_probs = {cls: count / total_docs for cls, count in class_counts.items()}

# Calculate word probabilities with Laplace smoothing
vocab_size = len(vocabulary)
word_probs = {}

for cls in class_counts:
    word_probs[cls] = {}
    total_words = sum(word_class_counts[cls].values())
    
    for word in vocabulary:
        word_count = word_class_counts[cls][word]
        # Laplace smoothing: (word_count + 1) / (total_words + vocab_size)
        word_probs[cls][word] = (word_count + 1) / (total_words + vocab_size)
```

### Prediction Phase (When user clicks "Analyze")

**1. Multi-Factor Score Calculation:**
```python
def analyze_compatibility(resume, job_description):
    # Factor 1: Naive Bayes Prediction (40% weight)
    predicted_class, class_probabilities = predict_compatibility_class(resume, job_description)
    base_score = class_probabilities.get('high', 0) * 0.8 + \
                class_probabilities.get('medium', 0) * 0.5 + \
                class_probabilities.get('low', 0) * 0.2
    
    # Factor 2: Skill Matching (35% weight)
    resume_skills = extract_skills(resume)
    job_skills = extract_skills(job_description)
    skill_match_score = calculate_skill_overlap(resume_skills, job_skills)
    
    # Factor 3: Jaccard Text Similarity (15% weight)
    text_similarity = calculate_jaccard_similarity(resume, job_description)
    
    # Factor 4: Experience Level Match (10% weight)
    resume_exp = extract_experience_level(resume)
    job_exp = extract_experience_level(job_description)
    exp_match_score = 1.0 if resume_exp == job_exp else 0.5
    
    # Combine all factors
    final_score = (base_score * 0.4 + 
                  skill_match_score * 0.35 + 
                  text_similarity * 0.15 + 
                  exp_match_score * 0.1)
    
    return min(final_score, 1.0)  # Cap at 100%
```

**2. Custom Naive Bayes Implementation:**
```python
def predict_compatibility_class(resume, job_description):
    combined_text = resume + " " + job_description
    tokens = preprocess_text(combined_text)
    
    class_scores = {}
    
    for cls in class_probs:
        # Start with log of class probability
        score = math.log(class_probs[cls])
        
        # Add log probabilities for each word
        for token in tokens:
            if token in vocabulary:
                score += math.log(word_probs[cls][token])
        
        class_scores[cls] = score
    
    # Convert back to probabilities
    max_score = max(class_scores.values())
    exp_scores = {cls: math.exp(score - max_score) for cls, score in class_scores.items()}
    total_exp = sum(exp_scores.values())
    probabilities = {cls: exp_score / total_exp for cls, exp_score in exp_scores.items()}
    
    predicted_class = max(class_scores, key=class_scores.get)
    return predicted_class, probabilities
```

### Why Custom Implementation?

**Mathematical Transparency:**
- Every probability calculation is visible and explainable
- No "black box" algorithms - you can trace every decision
- Custom feature engineering for resume-specific patterns

**Performance Benefits:**  
- Lightweight: No heavy ML frameworks (TensorFlow = 500MB+, our engine = <1MB)
- Fast training: Optimized for our specific use case
- Instant predictions: No external API calls or model loading delays

**Domain-Specific Optimizations:**
- 15 custom skill categories tailored for tech jobs
- Experience level extraction using regex patterns
- Resume-specific text preprocessing (removing common resume words)
- Multi-factor scoring that combines ML with rule-based logic

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

**A. Skill Detection Algorithm:**

The system searches through 15 predefined skill categories:

```python
skill_categories = {
    'programming': ['python', 'java', 'javascript', 'typescript', 'c++', 'go', 'rust'],
    'frameworks': ['react', 'angular', 'django', 'flask', 'spring', 'express'],
    'cloud': ['aws', 'azure', 'gcp', 'lambda', 'ec2', 's3', 'kubernetes'],
    'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'sqlite'],
    # ... and 11 more categories
}

def extract_skills(text):
    tokens = preprocess_text(text)  # Clean and tokenize
    found_skills = {}
    
    for category, skills in skill_categories.items():
        for skill in skills:
            if skill in tokens:
                found_skills[category].append(skill)
    
    return found_skills
```

**Real Example:**
```
Input: "I'm a senior Python developer with 5 years of AWS and Docker experience"
Tokens: ["senior", "python", "developer", "5", "years", "aws", "docker", "experience"]

Skill Detection Result:
- Programming: ["python"]
- Cloud: ["aws"] 
- DevOps: ["docker"]
- Other categories: [] (empty)
```

**B. Experience Level Detection:**

```python
def extract_experience_level(text):
    text = text.lower()
    
    # Pattern matching for years
    year_patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
        r'(\d+)\+?\s*yrs?\s*(?:of\s*)?(?:experience|exp)'
    ]
    
    years = 0
    for pattern in year_patterns:
        matches = re.findall(pattern, text)
        if matches:
            years = max(years, int(matches[0]))
    
    # Keyword-based detection
    if 'senior' in text or 'lead' in text or years >= 5:
        return 'senior'
    elif 'mid' in text or years >= 2:
        return 'mid'
    else:
        return 'junior'
```

**C. Skill Matching Percentage:**

```python
def calculate_skill_matches(resume_skills, job_skills):
    skill_matches = {}
    
    for category in skill_categories.keys():
        resume_category_skills = set(resume_skills.get(category, []))
        job_category_skills = set(job_skills.get(category, []))
        
        if job_category_skills:  # Only if job requires skills in this category
            match_percentage = len(resume_category_skills.intersection(job_category_skills)) / len(job_category_skills)
            skill_matches[category] = f"{int(match_percentage * 100)}%"
    
    return skill_matches
```

**Real Skill Matching Example:**
```
Resume Skills:
- Programming: ["python", "javascript"]  
- Cloud: ["aws"]
- Frameworks: ["react", "django"]

Job Requirements:
- Programming: ["python", "java"]
- Cloud: ["aws", "azure"] 
- Frameworks: ["react"]

Skill Match Calculation:
- Programming: intersection["python"] / required["python", "java"] = 1/2 = 50%
- Cloud: intersection["aws"] / required["aws", "azure"] = 1/2 = 50%  
- Frameworks: intersection["react"] / required["react"] = 1/1 = 100%

Overall Skill Match: (50% + 50% + 100%) / 3 = 66.7%
```

### Step 4: Machine Learning Prediction

**Custom Naive Bayes Algorithm:**

Our system uses a custom-built Naive Bayes classifier (no external ML libraries) that works on probability principles:

```python
# Training Phase (happens when system starts)
def train_model(training_data):
    for resume, job_desc, compatibility_label in training_data:
        combined_text = resume + " " + job_desc
        tokens = preprocess_text(combined_text)
        
        # Count how often each word appears in each class
        for token in tokens:
            word_counts[compatibility_label][token] += 1
        
        class_counts[compatibility_label] += 1
```

**Prediction Phase (when you click analyze):**
```python
# For each compatibility class (high, medium, low)
def predict_compatibility(resume, job_desc):
    combined_text = resume + " " + job_desc
    tokens = preprocess_text(combined_text)
    
    for each_class in ['high', 'medium', 'low']:
        # Start with base probability of this class
        score = log(class_probability[each_class])
        
        # For each word in the input
        for token in tokens:
            # Add log probability of seeing this word in this class
            score += log(word_probability[each_class][token])
        
        class_scores[each_class] = score
    
    # Pick class with highest score
    return max(class_scores)
```

**Real Example:**
```
Input: "Python developer with 5 years AWS experience"
Tokens: ["python", "developer", "years", "aws", "experience"]

High Class Score:
- Base probability: log(0.4) = -0.916
- P("python"|high): log(0.8) = -0.223  
- P("developer"|high): log(0.7) = -0.357
- P("years"|high): log(0.6) = -0.511
- P("aws"|high): log(0.9) = -0.105
- P("experience"|high): log(0.8) = -0.223
Total Score: -0.916 + (-0.223) + (-0.357) + (-0.511) + (-0.105) + (-0.223) = -2.335

Medium Class Score: -3.127
Low Class Score: -4.892

Result: HIGH compatibility (highest score)
```

**Laplace Smoothing:**
To handle words not seen during training:
```python
# Instead of probability = word_count / total_words
# We use: probability = (word_count + 1) / (total_words + vocabulary_size)
# This prevents zero probabilities that would break the calculation
```

### Step 4.5: Jaccard Similarity Calculation

**Jaccard Similarity Algorithm:**

This measures how similar two texts are by comparing their word overlap:

```python
def calculate_jaccard_similarity(text1, text2):
    # Convert texts to sets of unique words
    tokens1 = set(preprocess_text(text1))
    tokens2 = set(preprocess_text(text2))
    
    # Find intersection (shared words) and union (all unique words)
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    
    # Jaccard = |intersection| / |union|
    return len(intersection) / len(union)
```

**Real Example:**
```
Resume: "Python developer with React experience and AWS skills"
Job Description: "Seeking Python engineer with AWS and Docker expertise"

After preprocessing:
Resume tokens: {"python", "developer", "react", "experience", "aws", "skills"}
Job tokens: {"python", "engineer", "aws", "docker", "expertise"}

Intersection (shared): {"python", "aws"} = 2 words
Union (all unique): {"python", "developer", "react", "experience", "aws", "skills", "engineer", "docker", "expertise"} = 9 words

Jaccard Similarity = 2/9 = 0.22 = 22%
```

**Why Jaccard Similarity Matters:**
- Measures overall text overlap beyond just skills
- Catches context and terminology alignment
- Helps identify if candidate uses similar language to job posting
- Contributes 15% to final compatibility score

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
