#!/usr/bin/env python3
"""
Advanced Resume Parser with sophisticated parsing techniques.
Extracts detailed information including skills, experience, education, certifications, and projects.
"""

import re
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ContactInfo:
    """Contact information extracted from resume."""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None

@dataclass
class Education:
    """Education information."""
    degree: str
    institution: str
    year: Optional[str] = None
    gpa: Optional[str] = None
    relevant_courses: Optional[List[str]] = None

@dataclass
class Experience:
    """Work experience information."""
    title: str
    company: str
    duration: str
    description: List[str]
    technologies: List[str]
    achievements: List[str]

@dataclass
class Project:
    """Project information."""
    name: str
    description: str
    technologies: List[str]
    url: Optional[str] = None
    highlights: Optional[List[str]] = None

@dataclass
class Certification:
    """Certification information."""
    name: str
    issuer: str
    year: Optional[str] = None
    expiry: Optional[str] = None

@dataclass
class ParsedResume:
    """Complete parsed resume data."""
    contact_info: ContactInfo
    skills: Dict[str, List[str]]
    experience: List[Experience]
    education: List[Education]
    projects: List[Project]
    certifications: List[Certification]
    languages: List[str]
    raw_text: str
    parsed_sections: Dict[str, str]
    summary: Optional[str] = None

class AdvancedResumeParser:
    """Advanced resume parser with sophisticated parsing techniques."""
    
    def __init__(self):
        self.section_patterns = {
            'contact': r'(?i)(contact|personal|info|details)',
            'summary': r'(?i)(summary|objective|profile|about)',
            'experience': r'(?i)(experience|work|employment|career|professional)',
            'education': r'(?i)(education|academic|qualification|degree)',
            'skills': r'(?i)(skills|technologies|tools|languages|competencies)',
            'projects': r'(?i)(projects|portfolio|works|applications)',
            'certifications': r'(?i)(certifications|certificates|credentials)',
            'languages': r'(?i)(languages|spoken|fluent)',
            'achievements': r'(?i)(achievements|awards|recognition)'
        }
        
        self.skill_categories = {
            'programming_languages': [
                'python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift',
                'kotlin', 'scala', 'r', 'matlab', 'perl', 'bash', 'powershell', 'typescript'
            ],
            'frameworks': [
                'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring',
                'laravel', 'asp.net', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sql server', 'sqlite',
                'cassandra', 'dynamodb', 'elasticsearch', 'neo4j'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'gcp', 'heroku', 'digitalocean', 'vercel', 'netlify', 'firebase'
            ],
            'devops_tools': [
                'docker', 'kubernetes', 'jenkins', 'gitlab', 'github actions', 'terraform',
                'ansible', 'chef', 'puppet', 'vagrant'
            ],
            'security_tools': [
                'wireshark', 'nmap', 'metasploit', 'burp suite', 'nessus', 'kali linux',
                'splunk', 'elk stack', 'qradar', 'fireeye'
            ],
            'testing_tools': [
                'selenium', 'cypress', 'jest', 'mocha', 'junit', 'pytest', 'postman', 'soapui'
            ]
        }
    
    def parse_resume(self, text: str) -> ParsedResume:
        """Parse resume text and extract structured information."""
        text = self._preprocess_text(text)
        
        # Extract sections
        sections = self._extract_sections(text)
        
        # Parse each section
        contact_info = self._parse_contact_info(sections.get('contact', ''))
        summary = self._parse_summary(sections.get('summary', ''))
        skills = self._parse_skills(sections.get('skills', ''), text)
        experience = self._parse_experience(sections.get('experience', ''))
        education = self._parse_education(sections.get('education', ''))
        projects = self._parse_projects(sections.get('projects', ''))
        certifications = self._parse_certifications(sections.get('certifications', ''))
        languages = self._parse_languages(sections.get('languages', ''))
        
        return ParsedResume(
            contact_info=contact_info,
            summary=summary,
            skills=skills,
            experience=experience,
            education=education,
            projects=projects,
            certifications=certifications,
            languages=languages,
            raw_text=text,
            parsed_sections=sections
        )
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess resume text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\-\.\,\;\:\!\?\(\)\[\]\{\}\@\#\$\%\&\*\+\=\|\/\\]', '', text)
        return text.strip()
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract different sections from resume text."""
        sections = {}
        lines = text.split('\n')
        current_section = 'general'
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a section header
            section_found = False
            for section_name, pattern in self.section_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    if current_section != 'general':
                        sections[current_section] = '\n'.join(current_content)
                    current_section = section_name
                    current_content = []
                    section_found = True
                    break
            
            if not section_found:
                current_content.append(line)
        
        # Add the last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _parse_contact_info(self, text: str) -> ContactInfo:
        """Parse contact information."""
        contact = ContactInfo()
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact.email = email_match.group()
        
        # Extract phone
        phone_pattern = r'(\+?[\d\s\-\(\)]{10,})'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            contact.phone = phone_match.group().strip()
        
        # Extract LinkedIn
        linkedin_pattern = r'(?:linkedin\.com|linkedin)[\s\:]*([^\s\n]+)'
        linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin_match:
            contact.linkedin = linkedin_match.group(1)
        
        # Extract GitHub
        github_pattern = r'(?:github\.com|github)[\s\:]*([^\s\n]+)'
        github_match = re.search(github_pattern, text, re.IGNORECASE)
        if github_match:
            contact.github = github_match.group(1)
        
        # Extract location
        location_patterns = [
            r'(?:location|address|city|state)[\s\:]*([^\n]+)',
            r'([A-Z][a-z]+(?:[\s,]+[A-Z][a-z]+)*,\s*[A-Z]{2})',
            r'([A-Z][a-z]+(?:[\s,]+[A-Z][a-z]+)*,\s*[A-Z][a-z]+)'
        ]
        
        for pattern in location_patterns:
            location_match = re.search(pattern, text, re.IGNORECASE)
            if location_match:
                contact.location = location_match.group(1).strip()
                break
        
        return contact
    
    def _parse_summary(self, text: str) -> Optional[str]:
        """Parse summary/objective section."""
        if not text:
            return None
        
        # Extract first few sentences as summary
        sentences = text.split('.')
        if sentences:
            return sentences[0] if len(sentences[0]) > 20 else '. '.join(sentences[:2])
        return None
    
    def _parse_skills(self, skills_text: str, full_text: str) -> Dict[str, List[str]]:
        """Parse skills section with categorization."""
        skills = {category: [] for category in self.skill_categories.keys()}
        skills['other'] = []
        
        # Combine skills text with full text for better extraction
        search_text = f"{skills_text} {full_text}"
        search_text_lower = search_text.lower()
        
        # Extract skills by category
        for category, skill_list in self.skill_categories.items():
            for skill in skill_list:
                if skill.lower() in search_text_lower:
                    skills[category].append(skill)
        
        # Extract additional skills using regex patterns
        additional_skills = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', search_text)
        for skill in additional_skills:
            if len(skill) > 2 and skill.lower() not in [s.lower() for skills_list in skills.values() for s in skills_list]:
                skills['other'].append(skill)
        
        # Remove empty categories
        skills = {k: v for k, v in skills.items() if v}
        
        return skills
    
    def _parse_experience(self, text: str) -> List[Experience]:
        """Parse work experience section."""
        experiences = []
        
        if not text:
            return experiences
        
        # Split by potential job entries
        job_entries = re.split(r'(?=^[A-Z][^:]*\s*[-–—]\s*[A-Z])', text, flags=re.MULTILINE)
        
        for entry in job_entries:
            if not entry.strip():
                continue
            
            # Extract job title and company
            title_company_pattern = r'^([^:]+?)\s*[-–—]\s*([^\n]+)'
            match = re.search(title_company_pattern, entry)
            
            if match:
                title = match.group(1).strip()
                company = match.group(2).strip()
                
                # Extract duration
                duration_pattern = r'(\d{4}\s*[-–—]\s*(?:present|\d{4}|\w+))'
                duration_match = re.search(duration_pattern, entry)
                duration = duration_match.group(1) if duration_match else "Duration not specified"
                
                # Extract description
                description_lines = []
                lines = entry.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and not re.match(title_company_pattern, line) and not re.match(duration_pattern, line):
                        if line.startswith('•') or line.startswith('-'):
                            description_lines.append(line[1:].strip())
                        else:
                            description_lines.append(line)
                
                # Extract technologies
                technologies = []
                for line in description_lines:
                    for category, tech_list in self.skill_categories.items():
                        for tech in tech_list:
                            if tech.lower() in line.lower():
                                technologies.append(tech)
                
                # Extract achievements
                achievements = [line for line in description_lines if any(word in line.lower() for word in ['achieved', 'improved', 'increased', 'reduced', 'developed', 'implemented'])]
                
                experiences.append(Experience(
                    title=title,
                    company=company,
                    duration=duration,
                    description=description_lines,
                    technologies=list(set(technologies)),
                    achievements=achievements
                ))
        
        return experiences
    
    def _parse_education(self, text: str) -> List[Education]:
        """Parse education section."""
        education_list = []
        
        if not text:
            return education_list
        
        # Split by potential education entries
        edu_entries = re.split(r'(?=^[A-Z][^:]*\s*[-–—]\s*[A-Z])', text, flags=re.MULTILINE)
        
        for entry in edu_entries:
            if not entry.strip():
                continue
            
            # Extract degree and institution
            degree_institution_pattern = r'^([^:]+?)\s*[-–—]\s*([^\n]+)'
            match = re.search(degree_institution_pattern, entry)
            
            if match:
                degree = match.group(1).strip()
                institution = match.group(2).strip()
                
                # Extract year
                year_pattern = r'(\d{4})'
                year_match = re.search(year_pattern, entry)
                year = year_match.group(1) if year_match else None
                
                # Extract GPA
                gpa_pattern = r'GPA[:\s]*([\d\.]+)'
                gpa_match = re.search(gpa_pattern, entry, re.IGNORECASE)
                gpa = gpa_match.group(1) if gpa_match else None
                
                # Extract relevant courses
                courses_pattern = r'(?:courses?|subjects?)[:\s]*(.+)'
                courses_match = re.search(courses_pattern, entry, re.IGNORECASE)
                courses = []
                if courses_match:
                    courses_text = courses_match.group(1)
                    courses = [course.strip() for course in re.split(r'[,;]', courses_text)]
                
                education_list.append(Education(
                    degree=degree,
                    institution=institution,
                    year=year,
                    gpa=gpa,
                    relevant_courses=courses
                ))
        
        return education_list
    
    def _parse_projects(self, text: str) -> List[Project]:
        """Parse projects section."""
        projects = []
        
        if not text:
            return projects
        
        # Split by potential project entries
        project_entries = re.split(r'(?=^[A-Z][^:]*\s*[-–—]?\s*[A-Z])', text, flags=re.MULTILINE)
        
        for entry in project_entries:
            if not entry.strip():
                continue
            
            # Extract project name and description
            name_desc_pattern = r'^([^:]+?)\s*[-–—]?\s*([^\n]+)'
            match = re.search(name_desc_pattern, entry)
            
            if match:
                name = match.group(1).strip()
                description = match.group(2).strip()
                
                # Extract technologies
                technologies = []
                for category, tech_list in self.skill_categories.items():
                    for tech in tech_list:
                        if tech.lower() in entry.lower():
                            technologies.append(tech)
                
                # Extract URL
                url_pattern = r'(https?://[^\s]+)'
                url_match = re.search(url_pattern, entry)
                url = url_match.group(1) if url_match else None
                
                # Extract highlights
                highlights = []
                lines = entry.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and (line.startswith('•') or line.startswith('-')) and len(line) > 10:
                        highlights.append(line[1:].strip())
                
                projects.append(Project(
                    name=name,
                    description=description,
                    technologies=list(set(technologies)),
                    url=url,
                    highlights=highlights
                ))
        
        return projects
    
    def _parse_certifications(self, text: str) -> List[Certification]:
        """Parse certifications section."""
        certifications = []
        
        if not text:
            return certifications
        
        # Split by lines and look for certification patterns
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for certification patterns
            cert_patterns = [
                r'^([^:]+?)\s*[-–—]\s*([^\n]+)',
                r'([A-Z][A-Z\s]+(?:Certified|Certification|Certificate))\s*[-–—]?\s*([^\n]+)',
                r'([A-Z][A-Z\s]+)\s*[-–—]?\s*([^\n]+)'
            ]
            
            for pattern in cert_patterns:
                match = re.search(pattern, line)
                if match:
                    name = match.group(1).strip()
                    issuer = match.group(2).strip()
                    
                    # Extract year
                    year_pattern = r'(\d{4})'
                    year_match = re.search(year_pattern, line)
                    year = year_match.group(1) if year_match else None
                    
                    certifications.append(Certification(
                        name=name,
                        issuer=issuer,
                        year=year
                    ))
                    break
        
        return certifications
    
    def _parse_languages(self, text: str) -> List[str]:
        """Parse languages section."""
        languages = []
        
        if not text:
            return languages
        
        # Common programming and spoken languages
        language_patterns = [
            r'(?:fluent|proficient|intermediate|basic)\s+in\s+([^,\n]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*[-–—]\s*(?:fluent|proficient|intermediate|basic)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*[-–—]\s*[A-Z][a-z]+'
        ]
        
        for pattern in language_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    languages.extend([lang.strip() for lang in match if lang.strip()])
                else:
                    languages.append(match.strip())
        
        return list(set(languages))
    
    def get_parsed_summary(self, parsed_resume: ParsedResume) -> Dict[str, Any]:
        """Get a comprehensive summary of the parsed resume."""
        summary = {
            'contact_info': {
                'name': parsed_resume.contact_info.name,
                'email': parsed_resume.contact_info.email,
                'phone': parsed_resume.contact_info.phone,
                'location': parsed_resume.contact_info.location,
                'linkedin': parsed_resume.contact_info.linkedin,
                'github': parsed_resume.contact_info.github
            },
            'summary': parsed_resume.summary,
            'total_experience_years': self._calculate_experience_years(parsed_resume.experience),
            'skills_summary': {
                category: len(skills) for category, skills in parsed_resume.skills.items()
            },
            'top_skills': self._get_top_skills(parsed_resume.skills),
            'experience_count': len(parsed_resume.experience),
            'project_count': len(parsed_resume.projects),
            'certification_count': len(parsed_resume.certifications),
            'education_count': len(parsed_resume.education),
            'languages': parsed_resume.languages
        }
        
        return summary
    
    def _calculate_experience_years(self, experiences: List[Experience]) -> int:
        """Calculate total years of experience."""
        total_years = 0
        for exp in experiences:
            # Simple calculation - can be enhanced with more sophisticated parsing
            if 'present' in exp.duration.lower():
                total_years += 2  # Assume current role is at least 2 years
            else:
                # Extract years from duration
                years = re.findall(r'\d{4}', exp.duration)
                if len(years) >= 2:
                    total_years += int(years[1]) - int(years[0])
        
        return total_years
    
    def _get_top_skills(self, skills: Dict[str, List[str]]) -> List[str]:
        """Get top skills across all categories."""
        all_skills = []
        for skill_list in skills.values():
            all_skills.extend(skill_list)
        
        # Count frequency and return top skills
        skill_counts = {}
        for skill in all_skills:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        # Return top 10 skills by frequency
        sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)
        return [skill for skill, count in sorted_skills[:10]]

def print_parsed_resume(parsed_resume: ParsedResume):
    """Print a formatted version of the parsed resume."""
    print("=" * 80)
    print("📄 ADVANCED RESUME PARSING RESULTS")
    print("=" * 80)
    
    # Contact Information
    print("\n👤 CONTACT INFORMATION:")
    print("-" * 40)
    contact = parsed_resume.contact_info
    if contact.name:
        print(f"Name: {contact.name}")
    if contact.email:
        print(f"Email: {contact.email}")
    if contact.phone:
        print(f"Phone: {contact.phone}")
    if contact.location:
        print(f"Location: {contact.location}")
    if contact.linkedin:
        print(f"LinkedIn: {contact.linkedin}")
    if contact.github:
        print(f"GitHub: {contact.github}")
    
    # Summary
    if parsed_resume.summary:
        print(f"\n📝 SUMMARY:")
        print("-" * 40)
        print(parsed_resume.summary)
    
    # Skills
    print(f"\n🛠️  SKILLS ANALYSIS:")
    print("-" * 40)
    for category, skills in parsed_resume.skills.items():
        if skills:
            category_name = category.replace('_', ' ').title()
            print(f"{category_name}: {', '.join(skills)}")
    
    # Experience
    if parsed_resume.experience:
        print(f"\n💼 WORK EXPERIENCE:")
        print("-" * 40)
        for i, exp in enumerate(parsed_resume.experience, 1):
            print(f"{i}. {exp.title} at {exp.company}")
            print(f"   Duration: {exp.duration}")
            print(f"   Technologies: {', '.join(exp.technologies) if exp.technologies else 'Not specified'}")
            if exp.achievements:
                print(f"   Key Achievements: {len(exp.achievements)} identified")
            print()
    
    # Education
    if parsed_resume.education:
        print(f"\n🎓 EDUCATION:")
        print("-" * 40)
        for edu in parsed_resume.education:
            print(f"• {edu.degree} from {edu.institution}")
            if edu.year:
                print(f"  Year: {edu.year}")
            if edu.gpa:
                print(f"  GPA: {edu.gpa}")
            if edu.relevant_courses:
                print(f"  Relevant Courses: {', '.join(edu.relevant_courses)}")
            print()
    
    # Projects
    if parsed_resume.projects:
        print(f"\n🚀 PROJECTS:")
        print("-" * 40)
        for i, project in enumerate(parsed_resume.projects, 1):
            print(f"{i}. {project.name}")
            print(f"   Description: {project.description}")
            print(f"   Technologies: {', '.join(project.technologies) if project.technologies else 'Not specified'}")
            if project.url:
                print(f"   URL: {project.url}")
            if project.highlights:
                print(f"   Highlights: {len(project.highlights)} identified")
            print()
    
    # Certifications
    if parsed_resume.certifications:
        print(f"\n🏆 CERTIFICATIONS:")
        print("-" * 40)
        for cert in parsed_resume.certifications:
            print(f"• {cert.name} from {cert.issuer}")
            if cert.year:
                print(f"  Year: {cert.year}")
            print()
    
    # Languages
    if parsed_resume.languages:
        print(f"\n🌍 LANGUAGES:")
        print("-" * 40)
        print(f"Spoken/Programming Languages: {', '.join(parsed_resume.languages)}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    # Test the parser
    parser = AdvancedResumeParser()
    
    # Sample resume for testing
    sample_resume = """
    John Doe
    Software Engineer
    john.doe@email.com | +1-555-123-4567
    San Francisco, CA
    linkedin.com/in/johndoe | github.com/johndoe
    
    SUMMARY
    Experienced full-stack developer with 5 years of expertise in modern web technologies.
    
    EXPERIENCE
    Senior Software Engineer - TechCorp Inc.
    2020 - Present
    • Developed scalable web applications using React and Node.js
    • Implemented microservices architecture with Docker and Kubernetes
    • Led team of 5 developers in agile environment
    • Technologies: React, Node.js, Python, AWS, Docker, Kubernetes
    
    Software Developer - StartupXYZ
    2018 - 2020
    • Built RESTful APIs using Express.js and MongoDB
    • Created responsive frontend with React and TypeScript
    • Technologies: JavaScript, React, Express, MongoDB, Git
    
    EDUCATION
    Bachelor of Science in Computer Science - University of California
    2014 - 2018
    GPA: 3.8/4.0
    Relevant Courses: Data Structures, Algorithms, Web Development, Database Systems
    
    SKILLS
    Programming Languages: JavaScript, Python, Java, TypeScript
    Frameworks: React, Angular, Node.js, Express, Django
    Databases: MongoDB, PostgreSQL, MySQL, Redis
    Cloud Platforms: AWS, Azure, Google Cloud
    DevOps: Docker, Kubernetes, Jenkins, Git
    
    PROJECTS
    E-commerce Platform - React/Node.js
    • Full-stack e-commerce application with payment integration
    • Technologies: React, Node.js, MongoDB, Stripe API
    • URL: github.com/johndoe/ecommerce
    
    Real-time Chat App - Socket.io
    • Real-time messaging application with user authentication
    • Technologies: Node.js, Socket.io, MongoDB, JWT
    
    CERTIFICATIONS
    AWS Certified Solutions Architect - Amazon Web Services
    2021
    MongoDB Certified Developer - MongoDB Inc.
    2020
    
    LANGUAGES
    English - Fluent
    Spanish - Intermediate
    """
    
    print("Testing Advanced Resume Parser...")
    parsed = parser.parse_resume(sample_resume)
    print_parsed_resume(parsed)
    
    # Get summary
    summary = parser.get_parsed_summary(parsed)
    print("\n📊 PARSING SUMMARY:")
    print("-" * 40)
    print(f"Total Experience: {summary['total_experience_years']} years")
    print(f"Skills Categories: {len(summary['skills_summary'])}")
    print(f"Top Skills: {', '.join(summary['top_skills'])}")
    print(f"Experience Count: {summary['experience_count']}")
    print(f"Project Count: {summary['project_count']}")
    print(f"Certification Count: {summary['certification_count']}")
    print(f"Education Count: {summary['education_count']}")
