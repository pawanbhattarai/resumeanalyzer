"""
Training data for the Resume-Job Compatibility Analyzer
Contains labeled examples across different skill levels and domains
"""

TRAINING_DATA = [
    # High compatibility examples
    ("Senior Python Developer with 7 years experience in Django, Flask, PostgreSQL, AWS, Docker, Git. Built scalable web applications, REST APIs, microservices architecture.", 
     "Senior Python Developer position requiring 5+ years Django/Flask experience, PostgreSQL, AWS cloud services, Docker containerization, Git version control.", 
     "high"),
    
    ("Full Stack JavaScript Developer 5 years React, Node.js, Express, MongoDB, TypeScript, Jest testing, Agile methodologies, CI/CD pipelines.", 
     "Full Stack Developer role with React, Node.js, Express framework, MongoDB database, TypeScript, automated testing experience.", 
     "high"),
    
    ("DevOps Engineer 6 years Kubernetes, Jenkins, AWS, Terraform, Ansible, Linux administration, monitoring tools, infrastructure as code.", 
     "DevOps Engineer position requiring Kubernetes orchestration, Jenkins CI/CD, AWS cloud platform, infrastructure automation tools.", 
     "high"),
    
    ("Data Scientist PhD Machine Learning, Python, TensorFlow, PyTorch, scikit-learn, pandas, numpy, SQL, statistical analysis, deep learning.", 
     "Senior Data Scientist role requiring advanced ML knowledge, Python ecosystem, TensorFlow/PyTorch, statistical modeling, big data.", 
     "high"),
    
    ("Mobile App Developer 4 years Swift iOS development, Objective-C, Xcode, App Store deployment, RESTful APIs, Core Data, UI/UX design.", 
     "iOS Developer position requiring Swift programming, Xcode IDE, App Store experience, API integration, database management.", 
     "high"),
    
    # Medium compatibility examples
    ("Python Developer 3 years Django experience, MySQL, basic AWS knowledge, Git version control, some REST API development.", 
     "Senior Python Developer requiring 5+ years Django, PostgreSQL, advanced AWS services, microservices architecture, Docker.", 
     "medium"),
    
    ("Frontend Developer 2 years React, HTML, CSS, JavaScript, Bootstrap, responsive design, some Node.js exposure.", 
     "Full Stack Developer role requiring React, Node.js, Express, database management, backend API development.", 
     "medium"),
    
    ("Java Developer 4 years Spring Boot, MySQL, Maven, JUnit testing, basic microservices knowledge.", 
     "Senior Java Architect position requiring Spring ecosystem, microservices design, cloud platforms, team leadership.", 
     "medium"),
    
    ("Web Developer 3 years PHP Laravel, MySQL, jQuery, basic JavaScript, WordPress customization.", 
     "Full Stack Developer requiring modern JavaScript frameworks, Node.js, NoSQL databases, cloud deployment.", 
     "medium"),
    
    ("System Administrator 2 years Linux, Apache, MySQL, basic scripting, network configuration.", 
     "DevOps Engineer requiring Kubernetes, containerization, infrastructure automation, cloud platforms, CI/CD.", 
     "medium"),
    
    ("Software Engineer 1 year Python, basic web development, university projects, internship experience.", 
     "Mid-level Python Developer requiring 3+ years commercial experience, framework expertise, database design.", 
     "medium"),
    
    # Low compatibility examples
    ("Recent Computer Science graduate with coursework in Java basics, data structures, algorithms, academic projects only.", 
     "Senior Software Architect requiring 8+ years enterprise experience, system design, team leadership, multiple technologies.", 
     "low"),
    
    ("Customer Service Representative 5 years retail experience, basic computer skills, Microsoft Office, no programming background.", 
     "Software Developer position requiring programming languages, frameworks, database management, technical expertise.", 
     "low"),
    
    ("Graphic Designer 4 years Adobe Creative Suite, print design, basic HTML/CSS, freelance projects.", 
     "Backend Developer role requiring server-side programming, databases, API development, system architecture.", 
     "low"),
    
    ("Marketing Coordinator 3 years social media management, content creation, basic analytics, no technical experience.", 
     "Data Engineer position requiring ETL pipelines, big data technologies, cloud platforms, programming skills.", 
     "low"),
    
    ("Hardware Technician 2 years computer repair, basic networking, troubleshooting, no software development.", 
     "Full Stack Developer requiring web frameworks, databases, version control, software architecture.", 
     "low"),
    
    ("Business Analyst 3 years requirements gathering, documentation, stakeholder management, basic SQL queries.", 
     "Machine Learning Engineer requiring advanced mathematics, Python/R, ML frameworks, model deployment.", 
     "low"),
    
    ("Technical Writer 2 years documentation, API documentation, basic HTML, content management systems.", 
     "Cloud Solutions Architect requiring multi-cloud expertise, infrastructure design, enterprise architecture.", 
     "low"),
    
    ("Quality Assurance Tester 1 year manual testing, test case creation, bug reporting, basic automation exposure.", 
     "Senior DevOps Engineer requiring infrastructure automation, containerization, cloud orchestration, CI/CD expertise.", 
     "low"),
]
