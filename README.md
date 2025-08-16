# 🎯 Smart Job Recommendation System

An intelligent resume-to-job matching system that automatically detects your resume type and recommends the most relevant positions.

## ✨ Features

- **🔍 Automatic Resume Type Detection**: Automatically identifies if your resume is focused on:
  - Cybersecurity
  - Software Development
  - Data Science
  - DevOps
  - Cloud Engineering

- **🚀 Smart Query Generation**: Creates optimized job search queries based on your detected skills
- **📊 Domain-Aware Ranking**: Jobs are ranked using domain-specific scoring for better matches
- **💼 Multiple Job Sources**: Fetches jobs from Google Jobs via SerpApi
- **📈 Detailed Analysis**: Shows resume analysis, domain scores, and matching insights
- **💾 CSV Export**: Saves results with detailed matching information

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Your SerpApi Key

```bash
# Option 1: Environment variable
export SERPAPI_API_KEY="your_api_key_here"

# Option 2: Command line argument
python job_recommender.py --resume your_resume.pdf --api-key "your_api_key_here"
```

### 3. Run the System

```bash
python job_recommender.py --resume your_resume.pdf
```

## 📋 Usage Examples

### Basic Usage
```bash
python job_recommender.py --resume resume.pdf
```

### With Custom Location
```bash
python job_recommender.py --resume resume.pdf --location "Mumbai"
```

### LinkedIn Jobs Only
```bash
python job_recommender.py --resume resume.pdf --linkedin-only
```

### Custom Number of Results
```bash
python job_recommender.py --resume resume.pdf --top 20
```

### Custom Output File
```bash
python job_recommender.py --resume resume.pdf --out "my_jobs.csv"
```

## 🔧 How It Works

### 1. Resume Analysis
The system analyzes your resume and detects the primary domain:
- **Cybersecurity**: Security tools, certifications, threat analysis
- **Software Development**: Programming languages, frameworks, web technologies
- **Data Science**: ML/AI, statistics, data visualization tools
- **DevOps**: CI/CD, containers, cloud platforms, monitoring
- **Cloud Engineering**: Cloud services, infrastructure, serverless

### 2. Smart Query Generation
Based on detected skills, it generates optimized job search queries:
- **Cybersecurity**: "Cybersecurity Wireshark Nmap Bangalore jobs"
- **Software Dev**: "Software Developer Python React Bangalore jobs"
- **Data Science**: "Data Scientist Machine Learning Python Bangalore jobs"

### 3. Domain-Aware Ranking
Jobs are scored using:
- **Base Similarity**: Semantic matching between resume and job description
- **Domain Boost**: Extra points for domain-relevant keywords
- **Final Score**: Combined score for optimal ranking

## 📊 Output Format

### Console Output
```
🎯 Top Cybersecurity Job Recommendations:

1. Cybersecurity Engineer - TechCorp
   📍 Bangalore, India | Source: LinkedIn
   📊 Match: 85.2% (Base: 65.2% + Domain: +20.0%)
   🚀 Cybersecurity Boost Applied | 🎯 Cybersecurity Role
   🔗 Apply: [Job Link]
```

### CSV Output
The CSV includes columns for:
- Title, Company, Location, Source
- Primary Domain
- Base Match %, Domain Boost %, Final Match %
- Apply Link

## 🧪 Testing

Test the resume analysis system:

```bash
python test_resume_analysis.py
```

This will show how the system detects different resume types and generates appropriate queries.

## 📁 Supported Resume Formats

- **PDF**: Using PyPDF2
- **DOCX**: Using docx2txt
- **TXT**: Plain text files

## 🔑 API Requirements

- **SerpApi**: For fetching Google Jobs data
- Get your API key from [serpapi.com](https://serpapi.com)

## 🎯 Resume Optimization Tips

### For Better Cybersecurity Matches:
- Include security tools: Wireshark, Nmap, Metasploit, Burp Suite
- Mention certifications: CompTIA Security+, CEH, CISSP
- Use security keywords: penetration testing, vulnerability assessment, incident response

### For Better Software Development Matches:
- List programming languages: Python, Java, JavaScript, C++
- Include frameworks: React, Angular, Django, Spring
- Mention technologies: REST APIs, databases, cloud platforms

### For Better Data Science Matches:
- Include ML/AI keywords: machine learning, deep learning, AI
- List tools: Python, R, SQL, Pandas, TensorFlow
- Mention domains: NLP, computer vision, predictive modeling

## 🚨 Troubleshooting

### Common Issues:

1. **API Key Error**: Make sure your SerpApi key is valid and has credits
2. **No Jobs Found**: Try changing the location or check if the query is too specific
3. **Poor Matches**: Ensure your resume has relevant keywords for your target domain

### Performance Tips:

1. **Resume Length**: Keep resumes focused and relevant (1-2 pages)
2. **Keyword Density**: Include domain-specific keywords naturally
3. **Skill Organization**: Group related skills together for better detection

## 🤝 Contributing

Feel free to contribute by:
- Adding new domain detection patterns
- Improving the ranking algorithms
- Adding support for more resume formats
- Enhancing the query generation logic

## 📄 License

This project is open source and available under the MIT License.
