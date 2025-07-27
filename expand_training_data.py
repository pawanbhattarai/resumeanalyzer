
import json
import time
from data_collector import TechJobDataCollector
from data.training_data import TRAINING_DATA

def expand_training_data():
    """Expand training data with real-world job postings"""
    print("🚀 Starting comprehensive training data expansion...")
    print(f"📊 Current training data size: {len(TRAINING_DATA)} examples")
    
    # Initialize data collector
    collector = TechJobDataCollector()
    
    # Collect new training data
    new_training_data = collector.run_data_collection()
    
    # Combine with existing data
    combined_data = TRAINING_DATA + new_training_data
    
    print(f"✅ Expansion complete!")
    print(f"📈 New training data size: {len(combined_data)} examples")
    print(f"🆕 Added {len(new_training_data)} new examples")
    
    # Save expanded training data
    with open('data/expanded_training_data.py', 'w', encoding='utf-8') as f:
        f.write('"""\\nExpanded Training Dataset for Tech Resume-Job Compatibility Analyzer\\n')
        f.write(f'Total Examples: {len(combined_data)}\\n')
        f.write('Generated from real-world job postings and industry analysis\\n')
        f.write('Sources: Stack Overflow, GitHub, LinkedIn, Indeed, RemoteOK, Startup Job Boards\\n')
        f.write('"""\\n\\n')
        f.write('EXPANDED_TRAINING_DATA = [\\n')
        
        for i, (resume, job_desc, compatibility) in enumerate(combined_data):
            # Escape quotes and format properly
            resume_escaped = resume.replace('"', '\\"').replace('\\', '\\\\')
            job_desc_escaped = job_desc.replace('"', '\\"').replace('\\', '\\\\')
            
            f.write(f'    ("{resume_escaped}",\\n')
            f.write(f'     "{job_desc_escaped}",\\n')
            f.write(f'     "{compatibility}"),\\n')
            
            if i > 0 and i % 50 == 0:
                print(f"💾 Processed {i}/{len(combined_data)} examples...")
    
        f.write(']\\n')
    
    # Generate statistics
    stats = generate_training_stats(combined_data)
    
    # Save statistics
    with open('data/training_stats.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    print("\\n📊 Training Data Statistics:")
    print(f"   Total Examples: {stats['total_examples']}")
    print(f"   High Compatibility: {stats['high_compatibility']} ({stats['high_percentage']:.1f}%)")
    print(f"   Medium Compatibility: {stats['medium_compatibility']} ({stats['medium_percentage']:.1f}%)")
    print(f"   Low Compatibility: {stats['low_compatibility']} ({stats['low_percentage']:.1f}%)")
    print(f"   Unique Skills Covered: {len(stats['unique_skills'])}")
    print(f"   Role Types: {len(stats['role_types'])}")
    
    return combined_data

def generate_training_stats(training_data):
    """Generate comprehensive statistics about training data"""
    stats = {
        'total_examples': len(training_data),
        'high_compatibility': 0,
        'medium_compatibility': 0,
        'low_compatibility': 0,
        'unique_skills': set(),
        'role_types': set(),
        'experience_levels': set()
    }
    
    for resume, job_desc, compatibility in training_data:
        # Count compatibility levels
        if compatibility == 'high':
            stats['high_compatibility'] += 1
        elif compatibility == 'medium':
            stats['medium_compatibility'] += 1
        elif compatibility == 'low':
            stats['low_compatibility'] += 1
        
        # Extract skills and roles for diversity analysis
        combined_text = (resume + ' ' + job_desc).lower()
        
        # Common tech skills
        tech_skills = [
            'python', 'java', 'javascript', 'react', 'node.js', 'aws', 'docker', 
            'kubernetes', 'tensorflow', 'pytorch', 'mysql', 'postgresql', 'mongodb',
            'git', 'jenkins', 'django', 'spring', 'angular', 'vue', 'typescript'
        ]
        
        for skill in tech_skills:
            if skill in combined_text:
                stats['unique_skills'].add(skill)
        
        # Role types
        role_keywords = [
            'software engineer', 'data scientist', 'devops engineer', 'frontend developer',
            'backend developer', 'full stack', 'machine learning engineer', 'cloud architect'
        ]
        
        for role in role_keywords:
            if role in combined_text:
                stats['role_types'].add(role)
        
        # Experience levels
        exp_keywords = ['junior', 'senior', 'lead', 'principal', 'staff', 'entry level']
        for exp in exp_keywords:
            if exp in combined_text:
                stats['experience_levels'].add(exp)
    
    # Calculate percentages
    total = stats['total_examples']
    stats['high_percentage'] = (stats['high_compatibility'] / total) * 100
    stats['medium_percentage'] = (stats['medium_compatibility'] / total) * 100
    stats['low_percentage'] = (stats['low_compatibility'] / total) * 100
    
    # Convert sets to lists for JSON serialization
    stats['unique_skills'] = list(stats['unique_skills'])
    stats['role_types'] = list(stats['role_types'])
    stats['experience_levels'] = list(stats['experience_levels'])
    
    return stats

if __name__ == "__main__":
    expanded_data = expand_training_data()
    print("\\n🎉 Training data expansion completed successfully!")
    print("💡 You can now update your ML engine to use the expanded dataset.")
