#!/usr/bin/env python3
"""
Test script for your cybersecurity resume.
This shows how the system analyzes your specific resume and generates relevant queries.
"""

from job_recommender import analyze_resume_type, generate_smart_query

def test_your_resume():
    """Test the system with your actual cybersecurity resume."""
    
    print("🔍 ANALYZING YOUR CYBERSECURITY RESUME")
    print("=" * 60)
    
    # Read your actual resume
    try:
        with open("resume.txt", "r", encoding="utf-8") as f:
            your_resume = f.read()
        
        print("✅ Successfully loaded your resume.txt file")
        print(f"📏 Resume length: {len(your_resume)} characters")
        
    except FileNotFoundError:
        print("❌ resume.txt not found. Using sample cybersecurity resume instead.")
        your_resume = """
        Mohammed Sahal
        Cybersecurity enthusiast with strong knowledge in network security, penetration testing, 
        cloud security, and incident response. Skilled at identifying vulnerabilities, implementing 
        defense strategies, and ensuring compliance with industry standards. Passionate about threat 
        analysis and secure software development.
        
        Key Skills:
        - Cybersecurity Tools: Wireshark, Nmap, Metasploit, Burp Suite, Nessus
        - Programming & Scripting: Python, Bash, PowerShell, SQL
        - Security Areas: Network Security, Web Application Security, Vulnerability Assessment, Penetration Testing
        - Cloud Security: AWS Security Groups, IAM, Azure Defender
        - Other Skills: SIEM (Splunk, ELK), Firewalls, IDS/IPS, Cryptography
        
        Certifications:
        - CompTIA Security+ (2024)
        - Certified Ethical Hacker (CEH) – In Progress
        - AWS Cloud Practitioner – Security Track
        """
    
    # Analyze your resume
    print("\n🔍 Analyzing resume for domain focus...")
    analysis = analyze_resume_type(your_resume)
    
    # Display comprehensive analysis
    print(f"\n📋 Resume Analysis Results:")
    print(f"   🎯 Primary Domain: {analysis['primary_domain'].replace('_', ' ').title()}")
    print(f"   📊 Primary Score: {analysis['primary_score']}%")
    print(f"   📏 Resume Length: {analysis['resume_text_length']} characters")
    
    print(f"\n🏆 Top 3 Detected Domains:")
    for i, (domain, data) in enumerate(analysis['top_domains'], 1):
        domain_name = domain.replace('_', ' ').title()
        print(f"   {i}. {domain_name}: {data['score']}% ({len(data['keywords_found'])} keywords)")
        if data['keywords_found']:
            print(f"      Keywords: {', '.join(data['keywords_found'][:8])}")
    
    if analysis['analysis']['is_strong_focus']:
        print(f"\n✅ Strong focus detected in {analysis['primary_domain'].replace('_', ' ').title()}")
    else:
        print(f"\n⚠️  Limited focus detected. Consider adding more domain-specific keywords.")
    
    if analysis['analysis']['has_multiple_skills']:
        print(f"🔄 Multiple skill areas detected - this can be beneficial for hybrid roles!")
    
    # Generate smart query
    print(f"\n🔍 Generating optimized job query...")
    query = generate_smart_query(analysis, "Bangalore")
    print(f"🚀 Generated Query: {query}")
    
    # Show what this means for job matching
    print(f"\n💡 What This Means:")
    print(f"   • Your resume is {analysis['primary_score']}% focused on {analysis['primary_domain'].replace('_', ' ').title()}")
    print(f"   • The system will search for: {query}")
    print(f"   • Jobs will be ranked with {analysis['primary_domain'].replace('_', ' ').title()} boost")
    print(f"   • You'll get better matches for security-focused positions")
    
    # Recommendations for improvement
    print(f"\n🎯 Recommendations:")
    if analysis['primary_score'] < 50:
        print(f"   • Consider adding more {analysis['primary_domain'].replace('_', ' ').title()} keywords")
        print(f"   • Include more specific tools and technologies")
        print(f"   • Add relevant certifications if applicable")
    else:
        print(f"   • Great focus! Your resume is well-optimized for {analysis['primary_domain'].replace('_', ' ').title()} roles")
        print(f"   • The system will provide excellent job matches")
    
    print(f"\n🚀 Ready to run the full job recommendation system!")
    print(f"   Command: python job_recommender.py --resume resume.txt")

if __name__ == "__main__":
    test_your_resume()
