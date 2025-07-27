import re
import math
import json
from collections import defaultdict, Counter
from data.training_data import TRAINING_DATA

class ResumeAnalyzer:
    """Custom Resume-Job Compatibility Analyzer with Naive Bayes Classification"""
    
    def __init__(self):
        self.trained = False
        self.vocabulary = set()
        self.class_probs = {}
        self.word_probs = {}
        self.skill_categories = {
            'programming': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'swift', 'kotlin', 'scala', 'r', 'php', 'ruby', 'objective-c', 'solidity'],
            'frameworks': ['django', 'flask', 'fastapi', 'react', 'angular', 'vue', 'nextjs', 'nuxt', 'spring', 'spring boot', 'express', 'nestjs', 'laravel', 'rails', 'dotnet', 'asp.net', 'unity', 'react native', 'flutter'],
            'cloud': ['aws', 'azure', 'gcp', 'lambda', 'ec2', 's3', 'rds', 'eks', 'ecs', 'cloudformation', 'terraform', 'serverless', 'firebase', 'heroku', 'digitalocean'],
            'devops': ['docker', 'kubernetes', 'jenkins', 'gitlab', 'github actions', 'ansible', 'terraform', 'helm', 'argocd', 'prometheus', 'grafana', 'elk', 'ci/cd', 'gitops'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'sql server', 'dynamodb', 'cassandra', 'elasticsearch', 'snowflake', 'bigquery', 'redshift'],
            'frontend': ['html', 'css', 'javascript', 'typescript', 'react', 'vue', 'angular', 'sass', 'less', 'webpack', 'vite', 'bootstrap', 'tailwind', 'material-ui', 'styled-components'],
            'mobile': ['swift', 'kotlin', 'java', 'react native', 'flutter', 'xamarin', 'ionic', 'objective-c', 'android', 'ios', 'xcode', 'android studio'],
            'data_science': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'jupyter', 'matplotlib', 'seaborn', 'plotly', 'tableau', 'power bi', 'r', 'stata', 'spss'],
            'big_data': ['apache spark', 'hadoop', 'kafka', 'airflow', 'dbt', 'databricks', 'snowflake', 'redshift', 'bigquery', 'hive', 'pig', 'storm', 'flink'],
            'testing': ['junit', 'pytest', 'jest', 'cypress', 'selenium', 'testng', 'mocha', 'chai', 'enzyme', 'react testing library', 'espresso', 'xctest'],
            'monitoring': ['prometheus', 'grafana', 'datadog', 'new relic', 'splunk', 'elk stack', 'jaeger', 'zipkin', 'pagerduty', 'sentry'],
            'security': ['owasp', 'penetration testing', 'vulnerability assessment', 'encryption', 'oauth', 'jwt', 'ssl/tls', 'firewall', 'iam', 'security audit'],
            'version_control': ['git', 'github', 'gitlab', 'bitbucket', 'svn', 'mercurial', 'perforce'],
            'apis': ['rest', 'graphql', 'grpc', 'soap', 'api gateway', 'swagger', 'postman', 'insomnia', 'openapi'],
            'methodologies': ['agile', 'scrum', 'kanban', 'lean', 'devops', 'tdd', 'bdd', 'ci/cd', 'microservices', 'mvp', 'design patterns']
        }
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those',
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself'
        }
        
        # Train model with default data
        self.train_model()
    
    def preprocess_text(self, text):
        """Preprocess text: lowercase, remove punctuation, filter stop words, tokenize"""
        if not text:
            return []
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation using regex
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Tokenize
        tokens = text.split()
        
        # Filter stop words
        filtered_tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        
        return filtered_tokens
    
    def extract_experience_level(self, text):
        """Extract experience level from text using regex patterns"""
        text = text.lower()
        
        # Pattern for years of experience
        year_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)\+?\s*yrs?\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)\+?\s*years?\s*in',
            r'(\d+)\+?\s*yrs?\s*in'
        ]
        
        years = 0
        for pattern in year_patterns:
            matches = re.findall(pattern, text)
            if matches:
                years = max(years, int(matches[0]))
        
        # Pattern for experience levels
        if 'senior' in text or 'lead' in text or 'architect' in text or years >= 5:
            return 'senior'
        elif 'mid' in text or 'intermediate' in text or (2 <= years < 5):
            return 'mid'
        elif 'junior' in text or 'entry' in text or 'fresh' in text or (0 <= years < 2):
            return 'junior'
        else:
            return 'unknown'
    
    def extract_skills(self, text):
        """Extract skills from text based on predefined categories"""
        tokens = self.preprocess_text(text)
        found_skills = defaultdict(list)
        
        for category, skills in self.skill_categories.items():
            for skill in skills:
                if skill in tokens:
                    found_skills[category].append(skill)
        
        return dict(found_skills)
    
    def calculate_jaccard_similarity(self, text1, text2):
        """Calculate Jaccard similarity between two texts"""
        tokens1 = set(self.preprocess_text(text1))
        tokens2 = set(self.preprocess_text(text2))
        
        if not tokens1 and not tokens2:
            return 1.0
        
        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def train_model(self, training_data=None):
        """Train Naive Bayes model with training data"""
        if training_data is None:
            training_data = TRAINING_DATA
        
        # Initialize counters
        class_counts = Counter()
        word_class_counts = defaultdict(Counter)
        vocabulary = set()
        
        # Process training data
        for resume, job_desc, compatibility in training_data:
            # Combine resume and job description for feature extraction
            combined_text = resume + " " + job_desc
            tokens = self.preprocess_text(combined_text)
            
            class_counts[compatibility] += 1
            vocabulary.update(tokens)
            
            for token in tokens:
                word_class_counts[compatibility][token] += 1
        
        # Calculate class probabilities
        total_docs = sum(class_counts.values())
        self.class_probs = {cls: count / total_docs for cls, count in class_counts.items()}
        
        # Calculate word probabilities with Laplace smoothing
        self.vocabulary = vocabulary
        vocab_size = len(vocabulary)
        
        self.word_probs = {}
        for cls in class_counts:
            self.word_probs[cls] = {}
            total_words = sum(word_class_counts[cls].values())
            
            for word in vocabulary:
                word_count = word_class_counts[cls][word]
                # Laplace smoothing
                self.word_probs[cls][word] = (word_count + 1) / (total_words + vocab_size)
        
        self.trained = True
    
    def predict_compatibility_class(self, resume, job_description):
        """Predict compatibility class using Naive Bayes"""
        if not self.trained:
            raise Exception("Model not trained")
        
        combined_text = resume + " " + job_description
        tokens = self.preprocess_text(combined_text)
        
        class_scores = {}
        
        for cls in self.class_probs:
            # Start with log of class probability
            score = math.log(self.class_probs[cls])
            
            # Add log probabilities for each word
            for token in tokens:
                if token in self.vocabulary:
                    score += math.log(self.word_probs[cls][token])
            
            class_scores[cls] = score
        
        # Get the class with highest probability
        predicted_class = max(class_scores, key=class_scores.get)
        
        # Convert log scores to probabilities for confidence
        max_score = max(class_scores.values())
        exp_scores = {cls: math.exp(score - max_score) for cls, score in class_scores.items()}
        total_exp = sum(exp_scores.values())
        probabilities = {cls: exp_score / total_exp for cls, exp_score in exp_scores.items()}
        
        return predicted_class, probabilities
    
    def generate_recommendations(self, resume, job_description):
        """Generate improvement recommendations based on gap analysis"""
        resume_skills = self.extract_skills(resume)
        job_skills = self.extract_skills(job_description)
        
        recommendations = []
        
        # Skill gap analysis
        for category, required_skills in job_skills.items():
            resume_category_skills = set(resume_skills.get(category, []))
            required_skills_set = set(required_skills)
            missing_skills = required_skills_set - resume_category_skills
            
            if missing_skills:
                priority = "High" if len(missing_skills) >= len(required_skills_set) * 0.7 else "Medium"
                impact = f"Can improve compatibility by {len(missing_skills) * 5}%"
                
                recommendations.append({
                    "category": f"{category.title()} Skills",
                    "priority": priority,
                    "suggestion": f"Consider learning {', '.join(list(missing_skills)[:3])}",
                    "impact": impact
                })
        
        # Experience level recommendation
        resume_exp = self.extract_experience_level(resume)
        job_exp = self.extract_experience_level(job_description)
        
        if resume_exp == 'junior' and job_exp in ['mid', 'senior']:
            recommendations.append({
                "category": "Experience",
                "priority": "High",
                "suggestion": "Gain more hands-on project experience or consider additional certifications",
                "impact": "Can improve compatibility by 20%"
            })
        
        # Generic recommendations if no specific gaps found
        if not recommendations:
            recommendations.append({
                "category": "Profile Enhancement",
                "priority": "Low",
                "suggestion": "Consider highlighting specific achievements and quantifiable results",
                "impact": "Can improve compatibility by 5-10%"
            })
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def analyze_compatibility(self, resume, job_description):
        """Main analysis function that returns comprehensive compatibility report"""
        try:
            # Predict compatibility class
            predicted_class, class_probabilities = self.predict_compatibility_class(resume, job_description)
            
            # Calculate base compatibility score
            base_score = class_probabilities.get('high', 0) * 0.8 + class_probabilities.get('medium', 0) * 0.5 + class_probabilities.get('low', 0) * 0.2
            
            # Extract skills for detailed analysis
            resume_skills = self.extract_skills(resume)
            job_skills = self.extract_skills(job_description)
            
            # Calculate skill match percentages
            skill_matches = {}
            overall_skill_match = 0
            total_categories = 0
            
            for category in self.skill_categories.keys():
                resume_category_skills = set(resume_skills.get(category, []))
                job_category_skills = set(job_skills.get(category, []))
                
                if job_category_skills:
                    match_percentage = len(resume_category_skills.intersection(job_category_skills)) / len(job_category_skills)
                    skill_matches[category.title()] = f"{int(match_percentage * 100)}%"
                    overall_skill_match += match_percentage
                    total_categories += 1
                else:
                    skill_matches[category.title()] = "N/A"
            
            if total_categories > 0:
                overall_skill_match /= total_categories
            
            # Calculate text similarity
            text_similarity = self.calculate_jaccard_similarity(resume, job_description)
            
            # Calculate experience match
            resume_exp = self.extract_experience_level(resume)
            job_exp = self.extract_experience_level(job_description)
            exp_match_score = 1.0 if resume_exp == job_exp else 0.5 if resume_exp == 'unknown' or job_exp == 'unknown' else 0.3
            
            # Combine all factors for final score
            final_score = (base_score * 0.4 + overall_skill_match * 0.35 + text_similarity * 0.15 + exp_match_score * 0.1)
            final_score = min(final_score, 1.0)  # Cap at 1.0
            
            # Determine compatibility level
            if final_score >= 0.8:
                compatibility_level = "Excellent Match"
            elif final_score >= 0.6:
                compatibility_level = "Good Match"
            elif final_score >= 0.4:
                compatibility_level = "Fair Match"
            else:
                compatibility_level = "Poor Match"
            
            # Generate recommendations
            recommendations = self.generate_recommendations(resume, job_description)
            
            # Calculate improvement potential
            current_percentage = int(final_score * 100)
            max_improvement = min(100 - current_percentage, 25)
            improvement_potential = f"+{max_improvement}%"
            
            return {
                "compatibility_score": round(final_score, 2),
                "compatibility_level": compatibility_level,
                "detailed_analysis": {
                    "skill_matches": skill_matches,
                    "experience_match": f"{int(exp_match_score * 100)}%",
                    "text_similarity": f"{int(text_similarity * 100)}%"
                },
                "recommendations": recommendations,
                "improvement_potential": improvement_potential
            }
            
        except Exception as e:
            raise Exception(f"Analysis failed: {str(e)}")
    
    def is_trained(self):
        """Check if model is trained"""
        return self.trained
