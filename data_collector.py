"""
Real-time Tech Job Data Collector
Fetches authentic job descriptions from various sources to expand training data
"""

import trafilatura
import requests
import json
import time
import re
from typing import List, Dict, Tuple
import logging

class TechJobDataCollector:
    """Collect real tech job data from various sources"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.collected_jobs = []
        
    def fetch_job_content(self, url: str) -> str:
        """Fetch and extract clean text content from job posting URL"""
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                text = trafilatura.extract(downloaded)
                return text if text else ""
            return ""
        except Exception as e:
            logging.error(f"Error fetching {url}: {e}")
            return ""
    
    def collect_stackoverflow_jobs(self) -> List[Dict]:
        """Collect job data from Stack Overflow careers page"""
        jobs = []
        try:
            # Stack Overflow job search URLs for different roles
            search_urls = [
                "https://stackoverflow.com/jobs?q=python+developer",
                "https://stackoverflow.com/jobs?q=javascript+developer", 
                "https://stackoverflow.com/jobs?q=data+scientist",
                "https://stackoverflow.com/jobs?q=devops+engineer",
                "https://stackoverflow.com/jobs?q=machine+learning+engineer"
            ]
            
            for url in search_urls:
                content = self.fetch_job_content(url)
                if content:
                    # Extract job descriptions from the content
                    job_sections = self._extract_job_sections(content)
                    jobs.extend(job_sections)
                    
                time.sleep(2)  # Rate limiting
                
        except Exception as e:
            logging.error(f"Error collecting Stack Overflow jobs: {e}")
            
        return jobs
    
    def collect_github_jobs(self) -> List[Dict]:
        """Collect job data from GitHub careers"""
        jobs = []
        try:
            github_careers_url = "https://github.com/careers"
            content = self.fetch_job_content(github_careers_url)
            
            if content:
                job_sections = self._extract_job_sections(content)
                jobs.extend(job_sections)
                
        except Exception as e:
            logging.error(f"Error collecting GitHub jobs: {e}")
            
        return jobs
    
    def collect_ycombinator_jobs(self) -> List[Dict]:
        """Collect job data from Y Combinator job board"""
        jobs = []
        try:
            yc_jobs_url = "https://www.ycombinator.com/jobs"
            content = self.fetch_job_content(yc_jobs_url)
            
            if content:
                job_sections = self._extract_job_sections(content)
                jobs.extend(job_sections)
                
        except Exception as e:
            logging.error(f"Error collecting Y Combinator jobs: {e}")
            
        return jobs
    
    def _extract_job_sections(self, content: str) -> List[Dict]:
        """Extract individual job descriptions from page content"""
        jobs = []
        
        # Split content into potential job sections
        sections = re.split(r'\n\n+', content)
        
        for section in sections:
            if self._is_job_description(section):
                job_data = self._parse_job_description(section)
                if job_data:
                    jobs.append(job_data)
                    
        return jobs
    
    def _is_job_description(self, text: str) -> bool:
        """Check if text section is likely a job description"""
        job_indicators = [
            'years experience', 'required', 'responsibilities', 
            'qualifications', 'requirements', 'skills',
            'engineer', 'developer', 'scientist', 'architect',
            'python', 'javascript', 'java', 'react', 'aws'
        ]
        
        text_lower = text.lower()
        indicator_count = sum(1 for indicator in job_indicators if indicator in text_lower)
        
        return len(text) > 200 and indicator_count >= 3
    
    def _parse_job_description(self, text: str) -> Dict:
        """Parse job description text into structured data"""
        try:
            # Extract title (usually first line or contains role keywords)
            lines = text.strip().split('\n')
            title = self._extract_job_title(text)
            
            # Determine experience level and role type
            experience_level = self._extract_experience_level(text)
            role_type = self._extract_role_type(text)
            
            # Extract skills
            skills = self._extract_skills_from_text(text)
            
            return {
                'title': title,
                'description': text.strip(),
                'experience_level': experience_level,
                'role_type': role_type,
                'skills': skills,
                'length': len(text)
            }
            
        except Exception as e:
            logging.error(f"Error parsing job description: {e}")
            return None
    
    def _extract_job_title(self, text: str) -> str:
        """Extract job title from description"""
        lines = text.strip().split('\n')
        
        # Look for title patterns in first few lines
        title_patterns = [
            r'(Senior|Junior|Lead|Principal|Staff)?\s*(Software|Data|Machine Learning|DevOps|Cloud|Frontend|Backend|Full Stack)?\s*(Engineer|Developer|Scientist|Architect)',
            r'(React|Python|Java|JavaScript|iOS|Android)\s+(Developer|Engineer)',
            r'(Data|Machine Learning)\s+(Scientist|Engineer)',
            r'(DevOps|Cloud|Platform|Site Reliability)\s+Engineer'
        ]
        
        for line in lines[:3]:
            for pattern in title_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    return match.group().strip()
        
        return "Tech Role"
    
    def _extract_experience_level(self, text: str) -> str:
        """Extract experience level from job description"""
        text_lower = text.lower()
        
        if any(term in text_lower for term in ['senior', 'lead', 'principal', 'staff', '5+ years', '6+ years', '7+ years', '8+ years']):
            return 'senior'
        elif any(term in text_lower for term in ['junior', 'entry level', 'graduate', '0-2 years', '1-3 years']):
            return 'junior'
        else:
            return 'mid'
    
    def _extract_role_type(self, text: str) -> str:
        """Extract primary role type from job description"""
        text_lower = text.lower()
        
        role_keywords = {
            'data_science': ['data scientist', 'machine learning', 'ml engineer', 'data analyst', 'statistician'],
            'backend': ['backend', 'server-side', 'api development', 'microservices', 'database'],
            'frontend': ['frontend', 'react', 'vue', 'angular', 'ui/ux', 'javascript'],
            'fullstack': ['full stack', 'fullstack', 'full-stack'],
            'devops': ['devops', 'site reliability', 'platform engineer', 'infrastructure'],
            'mobile': ['ios', 'android', 'mobile', 'swift', 'kotlin', 'react native'],
            'security': ['security', 'cybersecurity', 'penetration testing'],
            'cloud': ['cloud architect', 'aws', 'azure', 'gcp', 'cloud engineer']
        }
        
        for role_type, keywords in role_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return role_type
                
        return 'general'
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract technical skills from job description"""
        text_lower = text.lower()
        
        # Comprehensive skill list based on real job data
        tech_skills = [
            'python', 'java', 'javascript', 'typescript', 'go', 'rust', 'c++', 'c#',
            'react', 'vue', 'angular', 'django', 'flask', 'spring', 'node.js',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'git', 'jenkins', 'gitlab', 'github actions', 'ci/cd',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            'spark', 'hadoop', 'kafka', 'airflow', 'snowflake',
            'prometheus', 'grafana', 'datadog', 'elk stack'
        ]
        
        found_skills = []
        for skill in tech_skills:
            if skill in text_lower:
                found_skills.append(skill)
                
        return found_skills
    
    def generate_training_examples(self, collected_jobs: List[Dict]) -> List[Tuple[str, str, str]]:
        """Generate training examples from collected job data"""
        training_examples = []
        
        for job in collected_jobs:
            # Create synthetic resume profiles that match at different levels
            resume_profiles = self._generate_matching_resumes(job)
            
            for resume, compatibility in resume_profiles:
                training_examples.append((
                    resume,
                    job['description'],
                    compatibility
                ))
                
        return training_examples
    
    def _generate_matching_resumes(self, job: Dict) -> List[Tuple[str, str]]:
        """Generate resume profiles that match job at different compatibility levels"""
        job_skills = job.get('skills', [])
        experience_level = job.get('experience_level', 'mid')
        role_type = job.get('role_type', 'general')
        
        resumes = []
        
        # High compatibility resume
        high_match_resume = self._create_high_match_resume(job_skills, experience_level, role_type)
        resumes.append((high_match_resume, 'high'))
        
        # Medium compatibility resume  
        medium_match_resume = self._create_medium_match_resume(job_skills, experience_level, role_type)
        resumes.append((medium_match_resume, 'medium'))
        
        # Low compatibility resume
        low_match_resume = self._create_low_match_resume(job_skills, experience_level, role_type)
        resumes.append((low_match_resume, 'low'))
        
        return resumes
    
    def _create_high_match_resume(self, job_skills: List[str], experience_level: str, role_type: str) -> str:
        """Create a resume with high compatibility to the job"""
        years_map = {'junior': '2', 'mid': '4', 'senior': '7'}
        years = years_map.get(experience_level, '4')
        
        # Include 80%+ of job skills
        resume_skills = job_skills[:int(len(job_skills) * 0.8)] if job_skills else ['python', 'aws', 'docker']
        
        resume = f"{experience_level.title()} {role_type.replace('_', ' ').title()} with {years}+ years experience in {', '.join(resume_skills[:10])}. "
        resume += f"Built production systems, led projects, mentored teams. Strong background in {role_type.replace('_', ' ')} development."
        
        return resume
    
    def _create_medium_match_resume(self, job_skills: List[str], experience_level: str, role_type: str) -> str:
        """Create a resume with medium compatibility to the job"""
        # Include 40-60% of job skills, different experience level
        resume_skills = job_skills[:int(len(job_skills) * 0.5)] if job_skills else ['python', 'sql']
        
        # Different experience level or transitioning role
        if experience_level == 'senior':
            resume_exp = 'Mid-level'
            years = '3'
        else:
            resume_exp = 'Junior'
            years = '2'
            
        resume = f"{resume_exp} developer with {years} years experience in {', '.join(resume_skills[:5])}. "
        resume += f"Some experience with {role_type.replace('_', ' ')}, looking to expand skills in advanced technologies."
        
        return resume
    
    def _create_low_match_resume(self, job_skills: List[str], experience_level: str, role_type: str) -> str:
        """Create a resume with low compatibility to the job"""
        # Very few matching skills, different domain
        different_roles = {
            'data_science': 'marketing analyst',
            'backend': 'frontend developer', 
            'frontend': 'data analyst',
            'devops': 'business analyst',
            'mobile': 'web developer'
        }
        
        different_role = different_roles.get(role_type, 'business analyst')
        basic_skills = ['excel', 'powerpoint', 'basic sql'] if role_type != 'general' else ['microsoft office']
        
        resume = f"{different_role.title()} with 3 years experience in {', '.join(basic_skills)}. "
        resume += f"Strong communication skills, project management experience. Limited technical programming background."
        
        return resume
    
    def run_data_collection(self) -> List[Tuple[str, str, str]]:
        """Run complete data collection process"""
        print("Starting real-world tech job data collection...")
        
        all_jobs = []
        
        # Collect from various sources
        print("Collecting Stack Overflow jobs...")
        all_jobs.extend(self.collect_stackoverflow_jobs())
        
        print("Collecting GitHub jobs...")
        all_jobs.extend(self.collect_github_jobs())
        
        print("Collecting Y Combinator jobs...")
        all_jobs.extend(self.collect_ycombinator_jobs())
        
        print(f"Collected {len(all_jobs)} job descriptions")
        
        # Generate training examples
        print("Generating training examples...")
        training_examples = self.generate_training_examples(all_jobs)
        
        print(f"Generated {len(training_examples)} training examples")
        
        return training_examples

if __name__ == "__main__":
    collector = TechJobDataCollector()
    training_data = collector.run_data_collection()
    
    # Save to file
    with open('data/collected_training_data.py', 'w') as f:
        f.write("# Real-world collected training data\n")
        f.write("COLLECTED_TRAINING_DATA = [\n")
        for resume, job_desc, compatibility in training_data:
            f.write(f'    ("{resume}", "{job_desc}", "{compatibility}"),\n')
        f.write("]\n")
    
    print(f"Saved {len(training_data)} training examples to collected_training_data.py")