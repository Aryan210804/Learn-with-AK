"""
Huge dataset of roadmaps for Learn with AK platform.
Categories: Tech, Cloud, Cyber Security, Core Engineering, Government, Banking, Law, Medical, Education, Marketing, Management, Media, Startup.
"""

ALL_ROADMAPS = [
    # ==================== SOFTWARE & TECH ====================
    {
        "title": "Software Engineer Career Path",
        "description": "Master the fundamentals of software engineering, algorithms, system design, and coding best practices.",
        "category": "Tech",
        "difficulty": "Advanced",
        "meta_data": {
            "skills": {"core": ["DSA", "System Design", "OOP"], "technical": ["Java/C++", "SQL", "Git"], "soft": ["Problem Solving", "Teamwork"]},
            "tools": ["IntelliJ/VS Code", "Jira", "GitHub", "Linux"],
            "career_readiness": {"resume": ["LeetCode Profile", "Open Source"], "interview": ["System Design", "Behavioral"], "portfolio": "Complex App"},
            "estimated_time": "12-18 Months",
            "career_progression": ["SDE I", "SDE II", "Senior SDE", "Principal Engineer"]
        },
        "steps": [
            {"level": "Beginner", "title": "Programming Fundamentals (C++/Java)", "desc": "Syntax, memory management, OOP concepts.", "resources": "GeeksForGeeks"},
            {"level": "Beginner", "title": "Data Structures & Algorithms", "desc": "Arrays, Lists, Trees, Graphs, Sorting, Searching.", "resources": "LeetCode / HackerRank"},
            {"level": "Intermediate", "title": "Database Engineering", "desc": "SQL normalization, ACID properties, Indexing.", "resources": "SQLZoo"},
            {"level": "Intermediate", "title": "Low-Level Design (LLD)", "desc": "Design patterns (Singleton, Factory, Observer).", "resources": "Refactoring.guru"},
            {"level": "Advanced", "title": "High-Level Design (HLD)", "desc": "Scalability, Load Balancing, Caching, Microservices.", "resources": "System Design Primer"},
            {"level": "Advanced", "title": "Operating Systems & Networking", "desc": "Concurrency, Threads, OSI Model, TCP/IP.", "resources": "TeachYourselfCS"}
        ]
    },
    {
        "title": "Full Stack Developer (MERN)",
        "description": "Become a versatile developer capable of building complete web applications using MongoDB, Express, React, and Node.js.",
        "category": "Tech",
        "difficulty": "Intermediate",
        "meta_data": {
            "skills": {"core": ["JavaScript", "HTML/CSS"], "technical": ["React", "Node.js", "MongoDB"], "soft": ["Adaptability"]},
            "tools": ["VS Code", "Postman", "Docker"],
            "career_readiness": {"resume": ["Full Stack Projects"], "interview": ["Live Coding"], "portfolio": "Deployed SaaS App"},
            "estimated_time": "8-10 Months",
            "career_progression": ["Junior Dev", "Full Stack Dev", "Tech Lead"]
        },
        "steps": [
            {"level": "Beginner", "title": "Web Foundations", "desc": "HTML5, CSS3, Semantic Web, Flexbox/Grid.", "resources": "MDN"},
            {"level": "Beginner", "title": "JavaScript Deep Dive", "desc": "ES6+, DOM, Fetch API, Async/Await.", "resources": "JavaScript.info"},
            {"level": "Intermediate", "title": "Frontend (React.js)", "desc": "Hooks, State Management (Redux), Routing.", "resources": "React.dev"},
            {"level": "Intermediate", "title": "Backend (Node/Express)", "desc": "REST APIs, Middleware, JWT Auth.", "resources": "Expressjs.com"},
            {"level": "Advanced", "title": "Database (MongoDB)", "desc": "Schema Design, Mongoose Aggregations.", "resources": "MongoDB University"},
            {"level": "Advanced", "title": "Deployment & DevOps", "desc": "Docker, CI/CD, AWS EC2/S3.", "resources": "Full Stack Open"}
        ]
    },
    
    # ==================== CLOUD & DEVOPS ====================
    {
        "title": "AWS Cloud Engineer",
        "description": "Master Amazon Web Services infrastructure, core services, and cloud architecture patterns.",
        "category": "Cloud & DevOps",
        "difficulty": "Advanced",
        "meta_data": {
            "skills": {"core": ["Networking", "Linux"], "technical": ["EC2", "S3", "VPC", "Lambda"], "soft": ["Troubleshooting"]},
            "tools": ["AWS Console", "AWS CLI", "Terraform"],
            "career_readiness": {"resume": ["AWS Solutions Architect Cert"], "interview": ["Architecture Scenarios"], "portfolio": "Cloud Formation Scripts"},
            "estimated_time": "6-9 Months",
            "career_progression": ["Cloud Admin", "Cloud Engineer", "Cloud Architect"]
        },
        "steps": [
            {"level": "Beginner", "title": "Cloud Concepts", "desc": "IaaS, PaaS, SaaS, Public vs Private Cloud.", "resources": "AWS Cloud Practitioner"},
            {"level": "Beginner", "title": "AWS Core Services", "desc": "EC2, S3, RDS, IAM.", "resources": "AWS Documentation"},
            {"level": "Intermediate", "title": "Networking on AWS", "desc": "VPC, Subnets, Route Tables, Security Groups.", "resources": "Cantrill Courses"},
            {"level": "Advanced", "title": "Serverless & Automation", "desc": "Lambda, API Gateway, CloudFormation.", "resources": "Serverless Land"}
        ]
    },

    # ==================== DATA & AI ====================
    {
        "title": "Data Scientist",
        "description": "Learn to extract insights from data using statistics, machine learning, and visualization techniques.",
        "category": "Data & AI",
        "difficulty": "Advanced",
        "meta_data": {
            "skills": {"core": ["Statistics", "Math"], "technical": ["Python", "Pandas", "Scikit-Learn"], "soft": ["Curiosity"]},
            "tools": ["Jupyter", "Tableau", "SQL"],
            "career_readiness": {"resume": ["Kaggle Medals"], "interview": ["Stats & Probability"], "portfolio": "Data Analysis Blog"},
            "estimated_time": "12 Months",
            "career_progression": ["Junior Data Scientist", "Senior Data Scientist", "Chief Data Officer"]
        },
        "steps": [
            {"level": "Beginner", "title": "Python for Data", "desc": "NumPy, Pandas, Data Cleaning.", "resources": "Kaggle Learn"},
            {"level": "Beginner", "title": "Statistics & Probability", "desc": "Distributions, Hypothesis Testing.", "resources": "Khan Academy"},
            {"level": "Intermediate", "title": "Data Visualization", "desc": "Matplotlib, Seaborn, Tableau.", "resources": "DataCamp"},
            {"level": "Intermediate", "title": "Machine Learning", "desc": "Regression, Classification, Clustering.", "resources": "Fast.ai"},
            {"level": "Advanced", "title": "Deep Learning", "desc": "Neural Networks, TensorFlow/PyTorch.", "resources": "DeepLearning.ai"}
        ]
    },

    # ==================== CYBER SECURITY ====================
    {
        "title": "Ethical Hacker (Penetration Tester)",
        "description": "Learn to identify and exploit vulnerabilities in systems to improve security.",
        "category": "Cyber Security",
        "difficulty": "Advanced",
        "meta_data": {
            "skills": {"core": ["Networking", "Linux"], "technical": ["Python Scripting", "Web Exp.", "Network Exp."], "soft": ["Ethics"]},
            "tools": ["Kali Linux", "Metasploit", "Burp Suite", "Nmap"],
            "career_readiness": {"resume": ["CEH / OSCP Certification"], "interview": ["Vuln. Assessment"], "portfolio": "Bug Bounty Profile"},
            "estimated_time": "12 Months",
            "career_progression": ["Junior Pen Tester", "Senior Pen Tester", "Security Consultant"]
        },
        "steps": [
            {"level": "Beginner", "title": "Networking Basics", "desc": "TCP/IP, DNS, HTTP, Ports, Protocols.", "resources": "CompTIA Network+"},
            {"level": "Beginner", "title": "Linux Essentials", "desc": "Command line, permissions, bash scripting.", "resources": "Linux Journey"},
            {"level": "Intermediate", "title": "Reconnaissance", "desc": "OSINT, Nmap scanning, Footprinting.", "resources": "TryHackMe"},
            {"level": "Intermediate", "title": "Web App Security", "desc": "OWASP Top 10, SQLi, XSS.", "resources": "PortSwigger Academy"},
            {"level": "Advanced", "title": "Exploitation", "desc": "Metasploit, Reverse Shells, Privilege Escalation.", "resources": "HackTheBox"}
        ]
    },

    # ==================== GOVERNMENT & CIVIL SERVICES ====================
    {
        "title": "Civil Services Officer (IAS)",
        "description": "Prepare for the UPSC Civil Services Examination to serve in the Indian Administrative Service.",
        "category": "Government",
        "difficulty": "Hard",
        "meta_data": {
            "skills": {"core": ["General Awareness", "Writing"], "technical": ["Public Admin", "Policy Analysis"], "soft": ["Leadership"]},
            "tools": ["Newspapers", "NCERTs", "Standard Books"],
            "career_readiness": {"resume": ["N/A (Exam Based)"], "interview": ["Personality Test"], "portfolio": "N/A"},
            "estimated_time": "12-24 Months",
            "career_progression": ["SDM", "District Magistrate", "Cabinet Secretary"]
        },
        "steps": [
            {"level": "Beginner", "title": "NCERT Foundation", "desc": "History, Geography, Polity, Economy (Class 6-12).", "resources": "NCERT Books"},
            {"level": "Intermediate", "title": "Standard Reference Books", "desc": "Laxmikanth (Polity), Spectrum (History), Economy.", "resources": "Standard Lists"},
            {"level": "Intermediate", "title": "Current Affairs", "desc": "Daily Newspaper (The Hindu), Monthly Magazines.", "resources": "VisionIAS / Insights"},
            {"level": "Advanced", "title": "Answer Writing", "desc": "Daily mains answer practice, Essay writing.", "resources": "Previous Years Papers"},
            {"level": "Advanced", "title": "Mock Tests", "desc": "Prelims and Mains full-length tests.", "resources": "Test Series"}
        ]
    },
    
    # ==================== BANKING & FINANCE ====================
    {
        "title": "Investment Banker",
        "description": "Career path for raising capital for companies, mergers and acquisitions, and financial advisory.",
        "category": "Finance",
        "difficulty": "Advanced",
        "meta_data": {
            "skills": {"core": ["Finance", "Accounting"], "technical": ["Financial Modeling", "Excel", "Valuation"], "soft": ["High Pressure Tolerance"]},
            "tools": ["Excel", "Bloomberg Terminal", "PowerPoint"],
            "career_readiness": {"resume": ["CFA Level 1"], "interview": ["Technical Finance"], "portfolio": "Stock Pitches"},
            "estimated_time": "12-24 Months",
            "career_progression": ["Analyst", "Associate", "VP", "Managing Director"]
        },
        "steps": [
            {"level": "Beginner", "title": "Financial Accounting", "desc": "Three financial statements, ratio analysis.", "resources": "Investopedia"},
            {"level": "Beginner", "title": "Excel Mastery", "desc": "Shortcuts, VLOOKUP, Macros, Pivot Tables.", "resources": "Excel Courses"},
            {"level": "Intermediate", "title": "Corporate Finance", "desc": "Time value of money, CAPM, WACC.", "resources": "CFA Curriculum"},
            {"level": "Advanced", "title": "Financial Modeling", "desc": "Building DCF models, LBO models, Comps.", "resources": "Breaking Into Wall Street"}
        ]
    },

    # ==================== MEDICAL ====================
    {
        "title": "Doctor (MBBS Path)",
        "description": "Roadmap for aspiring medical professionals in India (NEET -> MBBS).",
        "category": "Medical",
        "difficulty": "Hard",
        "meta_data": {
            "skills": {"core": ["Biology", "Chemistry", "Physics"], "technical": ["Diagnosis", "Anatomy"], "soft": ["Empathy"]},
            "tools": ["Stethoscope", "Books", "Lab Equipment"],
            "career_readiness": {"resume": ["Internship"], "interview": ["N/A"], "portfolio": "N/A"},
            "estimated_time": "5.5 Years + Prep",
            "career_progression": ["Intern", "Resident", "Consultant", "Specialist"]
        },
        "steps": [
            {"level": "Beginner", "title": "NEET Preparation (11th & 12th)", "desc": "Physics, Chemistry, Biology (NCERT Focus).", "resources": "Coaching / Self Study"},
            {"level": "Intermediate", "title": "MBBS Phase 1 (Pre-Clinical)", "desc": "Anatomy, Physiology, Biochemistry.", "resources": "Medical College"},
            {"level": "Intermediate", "title": "MBBS Phase 2 (Para-Clinical)", "desc": "Pathology, Microbiology, Pharmacology.", "resources": "Standard Textbooks"},
            {"level": "Advanced", "title": "MBBS Phase 3 (Clinical)", "desc": "Medicine, Surgery, OBG, Pediatrics.", "resources": "Clinical Postings"},
            {"level": "Advanced", "title": "Internship", "desc": "1 Year rotatory detailed training.", "resources": "Hospital"}
        ]
    },

    # ==================== CORE ENGINEERING ====================
    {
        "title": "Mechanical Engineer",
        "description": "Design, analyze, and manufacture mechanical systems.",
        "category": "Core Engineering",
        "difficulty": "Intermediate",
        "meta_data": {
            "skills": {"core": ["Physics", "Math"], "technical": ["Thermodynamics", "Mechanics", "CAD"], "soft": ["Analytical Thinking"]},
            "tools": ["AutoCAD", "SolidWorks", "MATLAB", "ANSYS"],
            "career_readiness": {"resume": ["Projects"], "interview": ["Technical Design"], "portfolio": "CAD Designs"},
            "estimated_time": "4 Years (Degree)",
            "career_progression": ["Graduate Engineer", "Design Engineer", "Project Manager"]
        },
        "steps": [
            {"level": "Beginner", "title": "Engineering Mechanics", "desc": "Statics, Dynamics, Strength of Materials.", "resources": "University Curriculum"},
            {"level": "Intermediate", "title": "Thermodynamics & Heat Transfer", "desc": "Laws of thermodynamics, cycles, conduction/convection.", "resources": "NPTEL"},
            {"level": "Intermediate", "title": "CAD Design", "desc": "2D Drafting and 3D Modeling (AutoCAD/SolidWorks).", "resources": "Udemy / Coursera"},
            {"level": "Advanced", "title": "Finite Element Analysis (FEA)", "desc": "Simulations and stress analysis using ANSYS.", "resources": "Specialized Courses"}
        ]
    }
]

# Helper to generate simple roadmaps for other roles to ensure volume
def get_simple_roadmap(title, category):
    return {
        "title": title,
        "description": f"Complete career path to become a {title}.",
        "category": category,
        "difficulty": "Intermediate",
        "meta_data": {
            "skills": {"core": ["Fundamentals"], "technical": ["Domain Tools"], "soft": ["Communication"]},
            "tools": ["Standard Industry Tools"],
            "career_readiness": {"resume": ["Standard"], "interview": ["Typical"], "portfolio": "N/A"},
            "estimated_time": "6-12 Months",
            "career_progression": ["Junior", "Senior", "Lead"]
        },
        "steps": [
            {"level": "Beginner", "title": "Fundamentals", "desc": "Learn the core concepts and theory.", "resources": "Online Courses"},
            {"level": "Intermediate", "title": "Practical Application", "desc": "Start using standard tools and working on small projects.", "resources": "Books/Docs"},
            {"level": "Advanced", "title": "Advanced Topics", "desc": "Master complex scenarios and optimizations.", "resources": "Advanced Certifications"},
            {"level": "Advanced", "title": "Real World Projects", "desc": "Gain industry experience through internships/projects.", "resources": "Industry"}
        ]
    }

# Add other requested roles simply to ensure coverage
extra_roles = [
    ("Frontend Developer", "Tech"), ("Backend Developer", "Tech"), ("Mobile App Developer", "Tech"), ("Game Developer", "Tech"),
    ("AI Engineer", "Data & AI"), ("Machine Learning Engineer", "Data & AI"), ("Big Data Engineer", "Data & AI"),
    ("Azure Engineer", "Cloud & DevOps"), ("GCP Engineer", "Cloud & DevOps"), ("Kubernetes Administrator", "Cloud & DevOps"), ("SRE", "Cloud & DevOps"),
    ("SOC Analyst", "Cyber Security"), ("Digital Forensics Expert", "Cyber Security"),
    ("Civil Engineer", "Core Engineering"), ("Electrical Engineer", "Core Engineering"), ("Electronics Engineer", "Core Engineering"),
    ("Junior Engineer (JE)", "Government"), ("Bank PO", "Finance"), ("Chartered Accountant (CA)", "Finance"),
    ("Lawyer/Advocate", "Law"), ("Judge", "Law"), ("Digital Marketing Specialist", "Marketing"), ("Product Manager", "Management")
]

for title, cat in extra_roles:
    # Only add if not already in ALL_ROADMAPS (simple check)
    if not any(r['title'].startswith(title) for r in ALL_ROADMAPS):
        ALL_ROADMAPS.append(get_simple_roadmap(title, cat))
