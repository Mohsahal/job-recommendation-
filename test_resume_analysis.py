#!/usr/bin/env python3
"""
Test script to demonstrate the resume analysis system.
This shows how the system automatically detects resume types and generates appropriate queries.
"""

from job_recommender import analyze_resume_type, generate_smart_query

def test_resume_analysis():
    """Test the resume analysis with different resume types."""
    
    # Test 1: Cybersecurity Resume
    print("=" * 60)
    print("🧪 TEST 1: CYBERSECURITY RESUME")
    print("=" * 60)
    
    cybersecurity_resume = """
    Cybersecurity Engineer with 5+ years experience in penetration testing, 
    vulnerability assessment, and incident response. Skilled in Wireshark, Nmap, 
    Metasploit, Burp Suite, and Nessus. Certified in CompTIA Security+ and CEH. 
    Experience with SOC operations, SIEM tools, and threat hunting.
    """
    
    analysis = analyze_resume_type(cybersecurity_resume)
    query = generate_smart_query(analysis, "Bangalore")
    
    print(f"Detected Domain: {analysis['primary_domain']}")
    print(f"Domain Score: {analysis['primary_score']}%")
    print(f"Generated Query: {query}")
    
    # Test 2: Software Development Resume
    print("\n" + "=" * 60)
    print("🧪 TEST 2: SOFTWARE DEVELOPMENT RESUME")
    print("=" * 60)
    
    software_resume = """
    Full Stack Developer with expertise in Python, JavaScript, React, Node.js, 
    Django, and Flask. Experience in building web applications, REST APIs, 
    and working with databases like PostgreSQL and MongoDB. Skilled in Git, 
    Docker, and AWS deployment.
    """
    
    analysis = analyze_resume_type(software_resume)
    query = generate_smart_query(analysis, "Mumbai")
    
    print(f"Detected Domain: {analysis['primary_domain']}")
    print(f"Domain Score: {analysis['primary_score']}%")
    print(f"Generated Query: {query}")
    
    # Test 3: Data Science Resume
    print("\n" + "=" * 60)
    print("🧪 TEST 3: DATA SCIENCE RESUME")
    print("=" * 60)
    
    data_science_resume = """
    Data Scientist with strong background in machine learning, deep learning, 
    and statistical analysis. Proficient in Python, R, SQL, Pandas, NumPy, 
    Scikit-learn, TensorFlow, and PyTorch. Experience in NLP, computer vision, 
    and predictive modeling. Skilled in data visualization with Tableau and Power BI.
    """
    
    analysis = analyze_resume_type(data_science_resume)
    query = generate_smart_query(analysis, "Delhi")
    
    print(f"Detected Domain: {analysis['primary_domain']}")
    print(f"Domain Score: {analysis['primary_score']}%")
    print(f"Generated Query: {query}")
    
    # Test 4: DevOps Resume
    print("\n" + "=" * 60)
    print("🧪 TEST 4: DEVOPS RESUME")
    print("=" * 60)
    
    devops_resume = """
    DevOps Engineer with expertise in CI/CD pipelines, Docker, Kubernetes, 
    Jenkins, GitLab, and Terraform. Experience with AWS, Azure, monitoring 
    tools like Prometheus and Grafana, and logging solutions like ELK stack. 
    Skilled in infrastructure as code and cloud automation.
    """
    
    analysis = analyze_resume_type(devops_resume)
    query = generate_smart_query(analysis, "Pune")
    
    print(f"Detected Domain: {analysis['primary_domain']}")
    print(f"Domain Score: {analysis['primary_score']}%")
    print(f"Generated Query: {query}")

if __name__ == "__main__":
    test_resume_analysis()
