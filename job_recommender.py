
import os
import sys
import argparse
import docx2txt
import PyPDF2
import requests
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Import configuration
try:
    from config import SERPAPI_API_KEY, DEFAULT_LOCATION, DEFAULT_TOP_RESULTS, DEFAULT_MODEL, check_api_key
except ImportError:
    # Fallback if config.py doesn't exist
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "")
    DEFAULT_LOCATION = "Bangalore"
    DEFAULT_TOP_RESULTS = 10
    DEFAULT_MODEL = "all-MiniLM-L6-v2"
    
    def check_api_key():
        if not SERPAPI_API_KEY:
            print("⚠️  WARNING: SerpApi API key not configured!")
            print("   Please set your API key in one of these ways:")
            print("   1. Edit config.py and set SERPAPI_API_KEY")
            print("   2. Set environment variable: $env:SERPAPI_API_KEY='your_key'")
            print("   3. Use command line: --api-key 'your_key'")
            print("   4. Get free API key from: https://serpapi.com")
            return False
        return True

# -------------------------------
# Resume text extraction
# -------------------------------
def extract_resume_text(resume_path: str) -> str:
    if resume_path.endswith(".pdf"):
        text = ""
        with open(resume_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    elif resume_path.endswith(".docx"):
        return docx2txt.process(resume_path)

    elif resume_path.endswith(".txt"):
        with open(resume_path, "r", encoding="utf-8") as f:
            return f.read()

    else:
        raise ValueError("Unsupported resume format. Use PDF, DOCX, or TXT.")

# -------------------------------
# Advanced Smart Query Builder
# -------------------------------
def generate_smart_query(resume_analysis: dict, location: str = "Bangalore") -> str:
    """
    Generates highly specific and relevant job search queries based on detected resume type.
    Creates perfect queries for JavaScript/Full Stack, Python, Java, etc.
    """
    
    primary_domain = resume_analysis["primary_domain"]
    subdomain = resume_analysis.get("subdomain", "")
    top_domains = resume_analysis["top_domains"]
    
    # Get the most relevant keywords from the primary domain
    primary_data = resume_analysis["all_domains"][primary_domain]
    
    # Domain-specific query templates with subdomain detection
    if primary_domain == "javascript_fullstack":
        return generate_javascript_query(primary_data, subdomain, location)
    
    elif primary_domain == "python_development":
        return generate_python_query(primary_data, subdomain, location)
    
    elif primary_domain == "java_development":
        return generate_java_query(primary_data, subdomain, location)
    
    elif primary_domain == "cybersecurity":
        return generate_cybersecurity_query(primary_data, subdomain, location)
    
    elif primary_domain == "data_science":
        return generate_data_science_query(primary_data, subdomain, location)
    
    elif primary_domain == "devops":
        return generate_devops_query(primary_data, subdomain, location)
    
    elif primary_domain == "cloud_engineering":
        return generate_cloud_query(primary_data, subdomain, location)
    
    # Fallback
    return f"Software Developer {location} jobs"

def generate_javascript_query(primary_data: dict, subdomain: str, location: str) -> str:
    """Generate specific queries for JavaScript/Full Stack development."""
    
    # Get the most relevant technologies
    frameworks = primary_data["framework_matches"][:3]  # Top 3 frameworks
    tools = primary_data["tool_matches"][:2]  # Top 2 tools
    databases = primary_data["database_matches"][:2]  # Top 2 databases
    
    # Build query based on subdomain
    if subdomain == "full_stack":
        if frameworks and databases:
            return f"Full Stack Developer {' '.join(frameworks)} {' '.join(databases)} {location} jobs"
        else:
            return f"Full Stack Developer JavaScript React Node.js {location} jobs"
    
    elif subdomain == "mern_stack":
        return f"MERN Stack Developer MongoDB Express React Node.js {location} jobs"
    
    elif subdomain == "frontend":
        if frameworks:
            return f"Frontend Developer {' '.join(frameworks)} {location} jobs"
        else:
            return f"Frontend Developer JavaScript React {location} jobs"
    
    elif subdomain == "backend":
        if frameworks and databases:
            return f"Backend Developer {' '.join(frameworks)} {' '.join(databases)} {location} jobs"
        else:
            return f"Backend Developer Node.js Express {location} jobs"
    
    else:  # javascript_developer
        if frameworks:
            return f"JavaScript Developer {' '.join(frameworks)} {location} jobs"
        else:
            return f"JavaScript Developer {location} jobs"

def generate_python_query(primary_data: dict, subdomain: str, location: str) -> str:
    """Generate specific queries for Python development."""
    
    frameworks = primary_data["framework_matches"][:2]
    
    if subdomain == "django_developer":
        return f"Django Developer Python {location} jobs"
    elif subdomain == "flask_developer":
        return f"Flask Developer Python {location} jobs"
    elif subdomain == "fastapi_developer":
        return f"FastAPI Developer Python {location} jobs"
    else:
        if frameworks:
            return f"Python Developer {' '.join(frameworks)} {location} jobs"
        else:
            return f"Python Developer {location} jobs"

def generate_java_query(primary_data: dict, subdomain: str, location: str) -> str:
    """Generate specific queries for Java development."""
    
    frameworks = primary_data["framework_matches"][:2]
    
    if subdomain == "spring_developer":
        return f"Spring Developer Java {location} jobs"
    elif subdomain == "hibernate_developer":
        return f"Hibernate Developer Java {location} jobs"
    else:
        if frameworks:
            return f"Java Developer {' '.join(frameworks)} {location} jobs"
        else:
            return f"Java Developer {location} jobs"

def generate_cybersecurity_query(primary_data: dict, subdomain: str, location: str) -> str:
    """Generate specific queries for cybersecurity."""
    
    tools = primary_data["tool_matches"][:2]
    
    if subdomain == "penetration_tester":
        return f"Penetration Tester Ethical Hacker {location} jobs"
    elif subdomain == "incident_response":
        return f"Incident Response Analyst {location} jobs"
    elif subdomain == "soc_analyst":
        return f"SOC Analyst Security Operations {location} jobs"
    else:
        if tools:
            return f"Cybersecurity Engineer {' '.join(tools)} {location} jobs"
        else:
            return f"Cybersecurity Engineer {location} jobs"

def generate_data_science_query(primary_data: dict, subdomain: str, location: str) -> str:
    """Generate specific queries for data science."""
    
    tools = primary_data["tool_matches"][:2]
    
    if subdomain == "ml_engineer":
        return f"Machine Learning Engineer Python {location} jobs"
    elif subdomain == "nlp_engineer":
        return f"NLP Engineer Natural Language Processing {location} jobs"
    elif subdomain == "computer_vision_engineer":
        return f"Computer Vision Engineer Python {location} jobs"
    else:
        if tools:
            return f"Data Scientist {' '.join(tools)} {location} jobs"
        else:
            return f"Data Scientist {location} jobs"

def generate_devops_query(primary_data: dict, subdomain: str, location: str) -> str:
    """Generate specific queries for DevOps."""
    
    tools = primary_data["tool_matches"][:2]
    
    if subdomain == "ci_cd_engineer":
        return f"CI/CD Engineer Jenkins GitLab {location} jobs"
    elif subdomain == "kubernetes_engineer":
        return f"Kubernetes Engineer DevOps {location} jobs"
    elif subdomain == "infrastructure_engineer":
        return f"Infrastructure Engineer Terraform {location} jobs"
    else:
        if tools:
            return f"DevOps Engineer {' '.join(tools)} {location} jobs"
        else:
            return f"DevOps Engineer {location} jobs"

def generate_cloud_query(primary_data: dict, subdomain: str, location: str) -> str:
    """Generate specific queries for cloud engineering."""
    
    cloud_platforms = primary_data["cloud_matches"][:2]
    
    if subdomain == "aws_engineer":
        return f"AWS Engineer Cloud {location} jobs"
    elif subdomain == "azure_engineer":
        return f"Azure Engineer Cloud {location} jobs"
    elif subdomain == "gcp_engineer":
        return f"GCP Engineer Cloud {location} jobs"
    else:
        if cloud_platforms:
            return f"Cloud Engineer {' '.join(cloud_platforms)} {location} jobs"
        else:
            return f"Cloud Engineer {location} jobs"

# -------------------------------
# Fetch jobs from SerpApi
# -------------------------------
def fetch_jobs_from_serpapi(query: str, api_key: str):
    url = "https://serpapi.com/search"
    params = {"engine": "google_jobs", "q": query, "api_key": api_key}
    resp = requests.get(url, params=params)

    if resp.status_code != 200:
        print("SerpApi Error:", resp.text)
        return []

    data = resp.json()
    return data.get("jobs_results", [])

def filter_linkedin(jobs):
    return [j for j in jobs if "linkedin" in j.get("via", "").lower()]

def extract_job_link(job):
    return job.get("share_link") or job.get("link") or ""

# -------------------------------
# Advanced Domain-Aware Job Ranking
# -------------------------------
def rank_jobs_domain_aware(resume_text, jobs, resume_analysis, model_name="all-MiniLM-L6-v2"):
    """
    Advanced job ranking using precise domain and subdomain detection.
    Provides much better matches for JavaScript/Full Stack, Python, Java, etc.
    """
    model = SentenceTransformer(model_name)
    resume_emb = model.encode(resume_text, convert_to_tensor=True)

    ranked = []
    primary_domain = resume_analysis["primary_domain"]
    subdomain = resume_analysis.get("subdomain", "")
    
    for job in jobs:
        job_text = f"{job.get('title','')} {job.get('company_name','')} {job.get('description','')}"
        job_emb = model.encode(job_text, convert_to_tensor=True)
        base_sim = util.cos_sim(resume_emb, job_emb).item()
        
        # Advanced domain-specific scoring
        domain_boost = calculate_advanced_domain_boost(job_text, primary_domain, subdomain, resume_analysis)
        
        # Calculate final similarity
        final_similarity = min(base_sim + domain_boost, 1.0)
        
        job["similarity"] = final_similarity
        job["base_similarity"] = base_sim
        job["domain_boost"] = domain_boost
        job["primary_domain"] = primary_domain
        job["subdomain"] = subdomain
        ranked.append(job)

    ranked.sort(key=lambda x: x["similarity"], reverse=True)
    return ranked

def calculate_advanced_domain_boost(job_text: str, primary_domain: str, subdomain: str, resume_analysis: dict) -> float:
    """
    Advanced domain-specific boost calculation with subdomain precision.
    """
    job_lower = job_text.lower()
    boost = 0.0
    
    # Domain-specific scoring with subdomain precision
    if primary_domain == "javascript_fullstack":
        boost = calculate_javascript_boost(job_lower, subdomain, resume_analysis)
    
    elif primary_domain == "python_development":
        boost = calculate_python_boost(job_lower, subdomain, resume_analysis)
    
    elif primary_domain == "java_development":
        boost = calculate_java_boost(job_lower, subdomain, resume_analysis)
    
    elif primary_domain == "cybersecurity":
        boost = calculate_cybersecurity_boost(job_lower, subdomain, resume_analysis)
    
    elif primary_domain == "data_science":
        boost = calculate_data_science_boost(job_lower, subdomain, resume_analysis)
    
    elif primary_domain == "devops":
        boost = calculate_devops_boost(job_lower, subdomain, resume_analysis)
    
    elif primary_domain == "cloud_engineering":
        boost = calculate_cloud_boost(job_lower, subdomain, resume_analysis)
    
    # Cap the total boost at 0.5 (50%)
    return min(boost, 0.5)

def calculate_javascript_boost(job_text: str, subdomain: str, resume_analysis: dict) -> float:
    """Calculate boost for JavaScript/Full Stack jobs."""
    boost = 0.0
    
    # High-value JavaScript/Full Stack keywords
    js_keywords = {
        "high": ["javascript", "js", "typescript", "ts", "react", "angular", "vue", "node.js", "nodejs"],
        "medium": ["express", "mongodb", "mysql", "firebase", "full stack", "fullstack", "mern", "mean"],
        "low": ["npm", "yarn", "webpack", "babel", "eslint", "jest", "mocha", "tailwindcss", "html5", "css3"]
    }
    
    # Subdomain-specific scoring
    if subdomain == "full_stack":
        if "full stack" in job_text or "fullstack" in job_text:
            boost += 0.3
        if "frontend" in job_text and "backend" in job_text:
            boost += 0.2
    
    elif subdomain == "mern_stack":
        if "mern" in job_text or ("mongodb" in job_text and "express" in job_text and "react" in job_text and "node" in job_text):
            boost += 0.4
    
    elif subdomain == "frontend":
        if "frontend" in job_text or "front-end" in job_text:
            boost += 0.3
        if "react" in job_text or "angular" in job_text or "vue" in job_text:
            boost += 0.2
    
    elif subdomain == "backend":
        if "backend" in job_text or "back-end" in job_text:
            boost += 0.3
        if "node.js" in job_text or "express" in job_text:
            boost += 0.2
    
    # General JavaScript boost
    for level, keywords in js_keywords.items():
        level_boost = {"high": 0.15, "medium": 0.10, "low": 0.05}[level]
        for keyword in keywords:
            if keyword in job_text:
                boost += level_boost
    
    return boost

def calculate_python_boost(job_text: str, subdomain: str, resume_analysis: dict) -> float:
    """Calculate boost for Python development jobs."""
    boost = 0.0
    
    python_keywords = {
        "high": ["python", "django", "flask", "fastapi"],
        "medium": ["pyramid", "bottle", "cherrypy", "api developer", "backend developer"],
        "low": ["pip", "virtualenv", "conda", "pytest", "unittest"]
    }
    
    # Subdomain-specific scoring
    if subdomain == "django_developer" and "django" in job_text:
        boost += 0.3
    elif subdomain == "flask_developer" and "flask" in job_text:
        boost += 0.3
    elif subdomain == "fastapi_developer" and "fastapi" in job_text:
        boost += 0.3
    
    # General Python boost
    for level, keywords in python_keywords.items():
        level_boost = {"high": 0.15, "medium": 0.10, "low": 0.05}[level]
        for keyword in keywords:
            if keyword in job_text:
                boost += level_boost
    
    return boost

def calculate_java_boost(job_text: str, subdomain: str, resume_analysis: dict) -> float:
    """Calculate boost for Java development jobs."""
    boost = 0.0
    
    java_keywords = {
        "high": ["java", "spring", "spring boot", "hibernate"],
        "medium": ["maven", "gradle", "junit", "mockito"],
        "low": ["ant", "intellij", "eclipse", "enterprise java"]
    }
    
    # Subdomain-specific scoring
    if subdomain == "spring_developer" and "spring" in job_text:
        boost += 0.3
    elif subdomain == "hibernate_developer" and "hibernate" in job_text:
        boost += 0.3
    
    # General Java boost
    for level, keywords in java_keywords.items():
        level_boost = {"high": 0.15, "medium": 0.10, "low": 0.05}[level]
        for keyword in keywords:
            if keyword in job_text:
                boost += level_boost
    
    return boost

def calculate_cybersecurity_boost(job_text: str, subdomain: str, resume_analysis: dict) -> float:
    """Calculate boost for cybersecurity jobs."""
    boost = 0.0
    
    security_keywords = {
        "high": ["security", "cybersecurity", "penetration", "ethical hacker", "vulnerability"],
        "medium": ["incident response", "soc", "siem", "firewall", "ids", "ips"],
        "low": ["forensics", "compliance", "audit", "risk", "wireshark", "nmap"]
    }
    
    # Subdomain-specific scoring
    if subdomain == "penetration_tester" and ("penetration" in job_text or "ethical hacker" in job_text):
        boost += 0.3
    elif subdomain == "incident_response" and "incident response" in job_text:
        boost += 0.3
    elif subdomain == "soc_analyst" and "soc" in job_text:
        boost += 0.3
    
    # General security boost
    for level, keywords in security_keywords.items():
        level_boost = {"high": 0.15, "medium": 0.10, "low": 0.05}[level]
        for keyword in keywords:
            if keyword in job_text:
                boost += level_boost
    
    return boost

def calculate_data_science_boost(job_text: str, subdomain: str, resume_analysis: dict) -> float:
    """Calculate boost for data science jobs."""
    boost = 0.0
    
    ds_keywords = {
        "high": ["data scientist", "machine learning", "ml", "deep learning", "ai"],
        "medium": ["analytics", "statistics", "predictive modeling", "data visualization"],
        "low": ["python", "r", "sql", "pandas", "numpy", "scikit-learn"]
    }
    
    # Subdomain-specific scoring
    if subdomain == "ml_engineer" and ("machine learning" in job_text or "ml" in job_text):
        boost += 0.3
    elif subdomain == "nlp_engineer" and "nlp" in job_text:
        boost += 0.3
    elif subdomain == "computer_vision_engineer" and "computer vision" in job_text:
        boost += 0.3
    
    # General data science boost
    for level, keywords in ds_keywords.items():
        level_boost = {"high": 0.15, "medium": 0.10, "low": 0.05}[level]
        for keyword in keywords:
            if keyword in job_text:
                boost += level_boost
    
    return boost

def calculate_devops_boost(job_text: str, subdomain: str, resume_analysis: dict) -> float:
    """Calculate boost for DevOps jobs."""
    boost = 0.0
    
    devops_keywords = {
        "high": ["devops", "ci/cd", "continuous integration", "continuous deployment"],
        "medium": ["docker", "kubernetes", "jenkins", "gitlab", "terraform"],
        "low": ["monitoring", "logging", "prometheus", "grafana", "ansible"]
    }
    
    # Subdomain-specific scoring
    if subdomain == "ci_cd_engineer" and ("ci/cd" in job_text or "continuous" in job_text):
        boost += 0.3
    elif subdomain == "kubernetes_engineer" and "kubernetes" in job_text:
        boost += 0.3
    elif subdomain == "infrastructure_engineer" and "terraform" in job_text:
        boost += 0.3
    
    # General DevOps boost
    for level, keywords in devops_keywords.items():
        level_boost = {"high": 0.15, "medium": 0.10, "low": 0.05}[level]
        for keyword in keywords:
            if keyword in job_text:
                boost += level_boost
    
    return boost

def calculate_cloud_boost(job_text: str, subdomain: str, resume_analysis: dict) -> float:
    """Calculate boost for cloud engineering jobs."""
    boost = 0.0
    
    cloud_keywords = {
        "high": ["cloud engineer", "cloud architect", "aws engineer", "azure engineer"],
        "medium": ["ec2", "s3", "lambda", "rds", "vpc", "iam", "cloudformation"],
        "low": ["serverless", "microservices", "kubernetes", "docker"]
    }
    
    # Subdomain-specific scoring
    if subdomain == "aws_engineer" and "aws" in job_text:
        boost += 0.3
    elif subdomain == "azure_engineer" and "azure" in job_text:
        boost += 0.3
    elif subdomain == "gcp_engineer" and "gcp" in job_text:
        boost += 0.3
    
    # General cloud boost
    for level, keywords in cloud_keywords.items():
        level_boost = {"high": 0.15, "medium": 0.10, "low": 0.05}[level]
        for keyword in keywords:
            if keyword in job_text:
                boost += level_boost
    
    return boost

# -------------------------------
# Save to CSV
# -------------------------------
def save_to_csv(jobs, out_file):
    # Prepare data for CSV with advanced domain-aware columns
    csv_data = []
    for job in jobs:
        csv_data.append({
            "Title": job.get("title", ""),
            "Company": job.get("company_name", ""),
            "Location": job.get("location", ""),
            "Source": job.get("via", ""),
            "Primary Domain": job.get("primary_domain", "").replace("_", " ").title(),
            "Subdomain": job.get("subdomain", "").replace("_", " ").title() if job.get("subdomain") else "N/A",
            "Base Match %": round(job.get("base_similarity", 0.0) * 100, 2),
            "Domain Boost %": round(job.get("domain_boost", 0.0) * 100, 2),
            "Final Match %": round(job.get("similarity", 0.0) * 100, 2),
            "Apply Link": job.get("share_link") or job.get("link") or ""
        })
    
    df = pd.DataFrame(csv_data)
    df.to_csv(out_file, index=False)
    return df

# -------------------------------
# Advanced Resume Type Detection and Analysis
# -------------------------------
def analyze_resume_type(resume_text: str) -> dict:
    """
    Advanced resume analysis that detects specific domains and subdomains.
    Provides much more precise detection for JavaScript, Full Stack, Frontend, Backend, etc.
    """
    
    # Define comprehensive keyword categories with subdomains
    domain_keywords = {
        "javascript_fullstack": {
            "keywords": [
                "javascript", "js", "es6", "es6+", "typescript", "ts", "node.js", "nodejs",
                "react", "react.js", "angular", "vue", "vue.js", "next.js", "nuxt.js",
                "express.js", "express", "mern", "mean", "full stack", "fullstack",
                "frontend", "backend", "web development", "web developer", "frontend developer",
                "backend developer", "full stack developer", "fullstack developer"
            ],
            "tools": ["npm", "yarn", "webpack", "babel", "eslint", "prettier", "jest", "mocha"],
            "frameworks": ["react", "angular", "vue", "express", "fastify", "koa", "next.js", "nuxt.js"],
            "databases": ["mongodb", "mysql", "postgresql", "firebase", "redis"],
            "cloud": ["aws", "vercel", "netlify", "heroku", "digitalocean"]
        },
        "python_development": {
            "keywords": [
                "python", "django", "flask", "fastapi", "pyramid", "bottle", "cherrypy",
                "python developer", "django developer", "flask developer", "backend developer",
                "api developer", "python engineer", "software engineer python"
            ],
            "tools": ["pip", "virtualenv", "conda", "pytest", "unittest", "black", "flake8"],
            "frameworks": ["django", "flask", "fastapi", "pyramid", "bottle"],
            "databases": ["postgresql", "mysql", "sqlite", "mongodb", "redis"],
            "cloud": ["aws", "azure", "gcp", "heroku", "digitalocean"]
        },
        "java_development": {
            "keywords": [
                "java", "spring", "spring boot", "spring framework", "hibernate", "maven",
                "gradle", "java developer", "spring developer", "backend developer",
                "java engineer", "software engineer java", "enterprise java"
            ],
            "tools": ["maven", "gradle", "ant", "junit", "mockito", "intellij", "eclipse"],
            "frameworks": ["spring", "spring boot", "spring mvc", "hibernate", "struts"],
            "databases": ["oracle", "mysql", "postgresql", "mongodb", "redis"],
            "cloud": ["aws", "azure", "gcp", "openshift", "kubernetes"]
        },
        "cybersecurity": {
            "keywords": [
                "security", "cybersecurity", "cyber security", "penetration", "ethical hacker",
                "vulnerability", "threat", "incident response", "soc", "siem", "firewall",
                "ids", "ips", "malware", "forensics", "compliance", "audit", "risk"
            ],
            "tools": ["wireshark", "nmap", "metasploit", "burp suite", "nessus", "owasp"],
            "frameworks": ["owasp", "nist", "iso 27001", "pci dss"],
            "databases": ["splunk", "elk", "qradar", "fireeye"],
            "cloud": ["aws security", "azure defender", "gcp security"]
        },
        "data_science": {
            "keywords": [
                "data scientist", "data analyst", "machine learning", "ml", "deep learning",
                "ai", "artificial intelligence", "statistics", "predictive modeling",
                "data visualization", "nlp", "computer vision", "big data"
            ],
            "tools": ["python", "r", "sql", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch"],
            "frameworks": ["scikit-learn", "tensorflow", "pytorch", "keras", "spark"],
            "databases": ["postgresql", "mysql", "mongodb", "hadoop", "spark"],
            "cloud": ["aws", "azure", "gcp", "databricks", "sagemaker"]
        },
        "devops": {
            "keywords": [
                "devops", "ci/cd", "continuous integration", "continuous deployment",
                "infrastructure", "automation", "monitoring", "logging", "deployment"
            ],
            "tools": ["docker", "kubernetes", "jenkins", "gitlab", "github actions", "terraform", "ansible"],
            "frameworks": ["kubernetes", "docker swarm", "jenkins", "gitlab ci"],
            "databases": ["prometheus", "grafana", "elk", "splunk"],
            "cloud": ["aws", "azure", "gcp", "digitalocean", "linode"]
        },
        "cloud_engineering": {
            "keywords": [
                "cloud engineer", "cloud architect", "aws engineer", "azure engineer",
                "gcp engineer", "cloud developer", "infrastructure engineer"
            ],
            "tools": ["terraform", "cloudformation", "ansible", "docker", "kubernetes"],
            "frameworks": ["aws", "azure", "gcp", "kubernetes", "docker"],
            "databases": ["rds", "dynamodb", "cosmos db", "firestore"],
            "cloud": ["aws", "azure", "gcp", "digitalocean", "linode"]
        }
    }
    
    # Calculate detailed scores for each domain
    domain_scores = {}
    for domain, data in domain_keywords.items():
        # Count keyword matches
        keyword_matches = [kw for kw in data["keywords"] if kw.lower() in resume_text.lower()]
        tool_matches = [tool for tool in data["tools"] if tool.lower() in resume_text.lower()]
        framework_matches = [fw for fw in data["frameworks"] if fw.lower() in resume_text.lower()]
        database_matches = [db for db in data["databases"] if db.lower() in resume_text.lower()]
        cloud_matches = [cloud for cloud in data["cloud"] if cloud.lower() in resume_text.lower()]
        
        # Calculate weighted score
        keyword_score = len(keyword_matches) / len(data["keywords"]) * 40  # 40% weight
        tool_score = len(tool_matches) / len(data["tools"]) * 25  # 25% weight
        framework_score = len(framework_matches) / len(data["frameworks"]) * 20  # 20% weight
        database_score = len(database_matches) / len(data["databases"]) * 10  # 10% weight
        cloud_score = len(cloud_matches) / len(data["cloud"]) * 5  # 5% weight
        
        total_score = keyword_score + tool_score + framework_score + database_score + cloud_score
        
        domain_scores[domain] = {
            "score": round(total_score, 1),
            "keyword_matches": keyword_matches,
            "tool_matches": tool_matches,
            "framework_matches": framework_matches,
            "database_matches": database_matches,
            "cloud_matches": cloud_matches,
            "total_keywords": len(data["keywords"]),
            "total_tools": len(data["tools"]),
            "total_frameworks": len(data["frameworks"]),
            "total_databases": len(data["databases"]),
            "total_cloud": len(data["cloud"])
        }
    
    # Determine primary domain
    primary_domain = max(domain_scores.items(), key=lambda x: x[1]["score"])
    
    # Get top 3 domains
    top_domains = sorted(domain_scores.items(), key=lambda x: x[1]["score"], reverse=True)[:3]
    
    # Detect subdomain (e.g., Frontend, Backend, Full Stack)
    subdomain = detect_subdomain(resume_text, primary_domain[0])
    
    return {
        "primary_domain": primary_domain[0],
        "primary_score": primary_domain[1]["score"],
        "subdomain": subdomain,
        "all_domains": domain_scores,
        "top_domains": top_domains,
        "resume_text_length": len(resume_text),
        "analysis": {
            "is_strong_focus": primary_domain[1]["score"] > 30,
            "has_multiple_skills": len([d for d in domain_scores.values() if d["score"] > 20]) > 1,
            "is_specialized": primary_domain[1]["score"] > 50
        }
    }

def detect_subdomain(resume_text: str, primary_domain: str) -> str:
    """Detect specific subdomain within the primary domain."""
    resume_lower = resume_text.lower()
    
    if primary_domain == "javascript_fullstack":
        if "frontend" in resume_lower and "backend" in resume_lower:
            return "full_stack"
        elif "frontend" in resume_lower:
            return "frontend"
        elif "backend" in resume_lower:
            return "backend"
        elif "mern" in resume_lower or "mean" in resume_lower:
            return "mern_stack"
        else:
            return "javascript_developer"
    
    elif primary_domain == "python_development":
        if "django" in resume_lower:
            return "django_developer"
        elif "flask" in resume_lower:
            return "flask_developer"
        elif "fastapi" in resume_lower:
            return "fastapi_developer"
        else:
            return "python_developer"
    
    elif primary_domain == "java_development":
        if "spring" in resume_lower:
            return "spring_developer"
        elif "hibernate" in resume_lower:
            return "hibernate_developer"
        else:
            return "java_developer"
    
    elif primary_domain == "cybersecurity":
        if "penetration" in resume_lower or "ethical hacker" in resume_lower:
            return "penetration_tester"
        elif "incident response" in resume_lower:
            return "incident_response"
        elif "soc" in resume_lower:
            return "soc_analyst"
        else:
            return "security_analyst"
    
    elif primary_domain == "data_science":
        if "machine learning" in resume_lower or "ml" in resume_lower:
            return "ml_engineer"
        elif "nlp" in resume_lower:
            return "nlp_engineer"
        elif "computer vision" in resume_lower:
            return "computer_vision_engineer"
        else:
            return "data_scientist"
    
    elif primary_domain == "devops":
        if "ci/cd" in resume_lower:
            return "ci_cd_engineer"
        elif "kubernetes" in resume_lower:
            return "kubernetes_engineer"
        elif "terraform" in resume_lower:
            return "infrastructure_engineer"
        else:
            return "devops_engineer"
    
    elif primary_domain == "cloud_engineering":
        if "aws" in resume_lower:
            return "aws_engineer"
        elif "azure" in resume_lower:
            return "azure_engineer"
        elif "gcp" in resume_lower:
            return "gcp_engineer"
        else:
            return "cloud_engineer"
    
    return "general"

# -------------------------------
# Main
# -------------------------------
def main():
    parser = argparse.ArgumentParser(description="Resume → Job Recommendation using SerpApi Google Jobs + Sentence Transformers")
    parser.add_argument("--resume", required=True, help="Path to resume file (PDF, DOCX, or TXT)")
    parser.add_argument("--api-key", default=SERPAPI_API_KEY, help="SerpApi API key")
    parser.add_argument("--top", type=int, default=DEFAULT_TOP_RESULTS, help="Number of top jobs to output")
    parser.add_argument("--linkedin-only", action="store_true", help="Filter to LinkedIn jobs only")
    parser.add_argument("--out", default="job_recommendations.csv", help="Path to save CSV output")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Sentence-Transformer model name")
    parser.add_argument("--location", default=DEFAULT_LOCATION, help="Preferred job location")
    parser.add_argument("--focus", default="cybersecurity", choices=["cybersecurity", "data-science", "software-engineering", "devops"], 
                       help="Focus area for job recommendations")
    args = parser.parse_args()

    if not args.api_key:
        print("ERROR: Provide SerpApi API key via --api-key or SERPAPI_API_KEY env var.", file=sys.stderr)
        print("\n🔑 How to set your API key:", file=sys.stderr)
        print("   1. Edit config.py and set SERPAPI_API_KEY = 'your_key'", file=sys.stderr)
        print("   2. Set environment variable: $env:SERPAPI_API_KEY='your_key'", file=sys.stderr)
        print("   3. Use command line: --api-key 'your_key'", file=sys.stderr)
        print("   4. Get free API key from: https://serpapi.com", file=sys.stderr)
        sys.exit(1)

    # Check if API key looks valid
    if len(args.api_key) < 20:
        print("WARNING: API key seems too short. Please check if it's correct.", file=sys.stderr)
    
    print("🔑 API Key configured successfully")

    print("📄 Reading resume:", args.resume)
    resume_text = extract_resume_text(args.resume)
    if not resume_text.strip():
        print("ERROR: Could not extract text from resume.", file=sys.stderr)
        sys.exit(1)

    # Validate cybersecurity focus
    print("🔍 Analyzing resume for domain focus...")
    resume_analysis = analyze_resume_type(resume_text)
    
    # Display comprehensive resume analysis
    print(f"\n📋 Resume Analysis Results:")
    print(f"   🎯 Primary Domain: {resume_analysis['primary_domain'].replace('_', ' ').title()}")
    print(f"   🔍 Subdomain: {resume_analysis.get('subdomain', 'N/A').replace('_', ' ').title()}")
    print(f"   📊 Primary Score: {resume_analysis['primary_score']}%")
    print(f"   📏 Resume Length: {resume_analysis['resume_text_length']} characters")
    
    print(f"\n🏆 Top 3 Detected Domains:")
    for i, (domain, data) in enumerate(resume_analysis['top_domains'], 1):
        domain_name = domain.replace('_', ' ').title()
        print(f"   {i}. {domain_name}: {data['score']}%")
        
        # Show detailed breakdown for the primary domain
        if domain == resume_analysis['primary_domain']:
            if data['keyword_matches']:
                print(f"      Keywords: {', '.join(data['keyword_matches'][:5])}")
            if data['framework_matches']:
                print(f"      Frameworks: {', '.join(data['framework_matches'][:3])}")
            if data['tool_matches']:
                print(f"      Tools: {', '.join(data['tool_matches'][:3])}")
            if data['database_matches']:
                print(f"      Databases: {', '.join(data['database_matches'][:2])}")
    
    if resume_analysis['analysis']['is_strong_focus']:
        print(f"\n✅ Strong focus detected in {resume_analysis['primary_domain'].replace('_', ' ').title()}")
    else:
        print(f"\n⚠️  Limited focus detected. Consider adding more domain-specific keywords.")
    
    if resume_analysis['analysis']['has_multiple_skills']:
        print(f"🔄 Multiple skill areas detected - this can be beneficial for hybrid roles!")
    
    if resume_analysis['analysis']['is_specialized']:
        print(f"🎯 Highly specialized profile - excellent for targeted job matching!")
    
    print("🔍 Generating optimized job query...")
    auto_query = generate_smart_query(resume_analysis, location=args.location)
    print("🔍 Job Query:", auto_query)

    jobs = fetch_jobs_from_serpapi(auto_query, args.api_key)
    print(f"✅ Fetched {len(jobs)} jobs from SerpApi")

    if args.linkedin_only:
        before = len(jobs)
        jobs = filter_linkedin(jobs)
        print(f"🔗 Filtered LinkedIn-only: {len(jobs)} / {before}")

    if not jobs:
        print("⚠️ No jobs found. Try changing query or location.", file=sys.stderr)
        sys.exit(0)

    print("📊 Ranking jobs by similarity...")
    ranked = rank_jobs_domain_aware(resume_text, jobs, resume_analysis, model_name=args.model)

    top_n = ranked[: args.top]
    domain_name = resume_analysis["primary_domain"].replace("_", " ").title()
    subdomain_name = resume_analysis.get("subdomain", "").replace("_", " ").title()
    
    if subdomain_name and subdomain_name != "N/A":
        print(f"\n🎯 Top {subdomain_name} {domain_name} Job Recommendations:\n")
    else:
        print(f"\n🎯 Top {domain_name} Job Recommendations:\n")
    
    for i, j in enumerate(top_n, 1):
        # Highlight domain-relevant jobs
        domain_indicators = []
        if j.get("domain_boost", 0) > 0:
            domain_indicators.append(f"🚀 {domain_name} Boost Applied")
        
        # Check if it's a domain-focused job
        job_text = f"{j.get('title','')} {j.get('company_name','')} {j.get('description','')}".lower()
        primary_domain_data = resume_analysis["all_domains"][j.get("primary_domain", "")]
        
        # Check for exact subdomain matches
        if j.get("subdomain") and j.get("subdomain") == resume_analysis.get("subdomain"):
            domain_indicators.append(f"🎯 Perfect {subdomain_name} Match")
        
        # Check for framework/tool matches
        if primary_domain_data.get("framework_matches"):
            framework_matches = [fw for fw in primary_domain_data["framework_matches"][:3] if fw.lower() in job_text]
            if framework_matches:
                domain_indicators.append(f"⚡ {', '.join(framework_matches)} Match")
        
        print(f"{i}. {j.get('title','')} - {j.get('company_name','')}")
        print(f"   📍 {j.get('location','')} | Source: {j.get('via','')}")
        print(f"   📊 Match: {round(j.get('similarity', 0.0) * 100, 2)}% "
              f"(Base: {round(j.get('base_similarity', 0.0) * 100, 2)}% + "
              f"Domain: +{round(j.get('domain_boost', 0.0) * 100, 2)}%)")
        
        if domain_indicators:
            print(f"   {' | '.join(domain_indicators)}")
        
        print(f"   🔗 Apply: {extract_job_link(j)}")
        print()

    save_to_csv(top_n, args.out)
    print(f"\n💾 Saved top {len(top_n)} recommendations to: {args.out}")


if __name__ == "__main__":
    main()
