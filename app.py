from flask import Flask, render_template, request, jsonify, session, send_file
import os
import tempfile
from werkzeug.utils import secure_filename
import PyPDF2
import docx2txt
import requests
from sentence_transformers import SentenceTransformer, util
import traceback
import json

# Import job recommender functions
from job_recommender import (
    analyze_resume_type, 
    generate_smart_query, 
    fetch_jobs_from_serpapi,
    rank_jobs_domain_aware,
    save_to_csv
)

# Import configuration
try:
    from config import SERPAPI_API_KEY, DEFAULT_LOCATION, DEFAULT_TOP_RESULTS, DEFAULT_MODEL
except ImportError:
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "")
    DEFAULT_LOCATION = "Bangalore"
    DEFAULT_TOP_RESULTS = 10
    DEFAULT_MODEL = "all-MiniLM-L6-v2"

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_resume_text(file_path: str, file_extension: str) -> str:
    """Extract text from resume file based on its extension."""
    try:
        if file_extension == 'pdf':
            text = ""
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text() or ""
                    text += page_text + "\n"
            return text.strip()

        elif file_extension == 'docx':
            return docx2txt.process(file_path)

        elif file_extension == 'txt':
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()

        else:
            raise ValueError("Unsupported resume format. Use PDF, DOCX, or TXT.")
    except Exception as e:
        raise Exception(f"Error extracting text from {file_extension} file: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    try:
        # Check if file was uploaded
        if 'resume' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PDF, DOCX, or TXT files only.'}), 400
        
        # Get location preference
        location = request.form.get('location', DEFAULT_LOCATION)
        
        # Check API key
        if not SERPAPI_API_KEY:
            return jsonify({'error': 'SerpApi API key not configured. Please check your configuration.'}), 500
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.rsplit('.', 1)[1].lower()}") as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name
        
        try:
            # Extract text from resume
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            resume_text = extract_resume_text(temp_file_path, file_extension)
            
            if not resume_text.strip():
                return jsonify({'error': 'Could not extract text from resume. Please ensure the file contains readable text.'}), 400
            
            # Debug: Print resume text preview
            print(f"📄 Resume text preview (first 500 chars): {resume_text[:500]}...")
            print(f"📏 Total resume length: {len(resume_text)} characters")
            
            # Analyze resume type
            print("🔍 Analyzing resume for domain focus...")
            resume_analysis = analyze_resume_type(resume_text)
            
            # Debug: Print detailed resume analysis results
            print(f"🎯 Resume Analysis Results:")
            print(f"   Primary Domain: {resume_analysis['primary_domain']}")
            print(f"   Subdomain: {resume_analysis.get('subdomain', 'N/A')}")
            print(f"   Primary Score: {resume_analysis['primary_score']}%")
            print(f"   Top Domains: {resume_analysis['top_domains']}")
            
            # Print detailed domain breakdown
            print(f"\n📊 Detailed Domain Analysis:")
            for domain, data in resume_analysis['all_domains'].items():
                domain_name = domain.replace('_', ' ').title()
                print(f"   {domain_name}: {data['score']}%")
                if data['keyword_matches']:
                    print(f"     Keywords: {', '.join(data['keyword_matches'][:5])}")
                if data['framework_matches']:
                    print(f"     Frameworks: {', '.join(data['framework_matches'][:3])}")
                if data['tool_matches']:
                    print(f"     Tools: {', '.join(data['tool_matches'][:3])}")
                print()
            
            # Generate smart query
            print("🔍 Generating optimized job query...")
            auto_query = generate_smart_query(resume_analysis, location=location)
            print(f"🔍 Generated Query: {auto_query}")
            
            # Fetch jobs from SerpApi
            print("🔍 Fetching jobs from SerpApi...")
            jobs = fetch_jobs_from_serpapi(auto_query, SERPAPI_API_KEY)
            print(f"📊 Fetched {len(jobs)} jobs from SerpApi")
            
            if not jobs:
                return jsonify({
                    'success': True,
                    'message': 'Resume analyzed successfully, but no jobs found for the current query.',
                    'resume_analysis': {
                        'primary_domain': resume_analysis['primary_domain'].replace('_', ' ').title(),
                        'subdomain': resume_analysis.get('subdomain', 'N/A').replace('_', ' ').title(),
                        'primary_score': resume_analysis['primary_score'],
                        'top_domains': [
                            {
                                'domain': domain.replace('_', ' ').title(),
                                'score': data['score']
                            } for domain, data in resume_analysis['top_domains']
                        ],
                        'detailed_analysis': {
                            domain.replace('_', ' ').title(): {
                                'score': data['score'],
                                'keyword_matches': data['keyword_matches'],
                                'framework_matches': data['framework_matches'],
                                'tool_matches': data['tool_matches']
                            } for domain, data in resume_analysis['all_domains'].items()
                        }
                    },
                    'query': auto_query,
                    'jobs_count': 0
                })
            
            # Debug: Print first few jobs
            print(f"📋 Sample jobs fetched:")
            for i, job in enumerate(jobs[:3]):
                print(f"   {i+1}. {job.get('title', 'N/A')} - {job.get('company_name', 'N/A')}")
                print(f"      Description preview: {job.get('description', 'N/A')[:100]}...")
            
            # Rank jobs by similarity
            print("📊 Ranking jobs by similarity...")
            try:
                ranked_jobs = rank_jobs_domain_aware(resume_text, jobs, resume_analysis, model_name=DEFAULT_MODEL)
                print(f"✅ Job ranking completed successfully")
                
                # Debug: Print ranking results
                print(f"📊 Ranking Results (top 3):")
                for i, job in enumerate(ranked_jobs[:3]):
                    print(f"   {i+1}. {job.get('title', 'N/A')}")
                    print(f"      Similarity: {round(job.get('similarity', 0.0) * 100, 2)}%")
                    print(f"      Base: {round(job.get('base_similarity', 0.0) * 100, 2)}%")
                    print(f"      Domain Boost: {round(job.get('domain_boost', 0.0) * 100, 2)}%")
                
            except Exception as ranking_error:
                print(f"❌ Error in job ranking: {str(ranking_error)}")
                print(traceback.format_exc())
                # Fallback: use original jobs without ranking
                ranked_jobs = jobs
                for job in ranked_jobs:
                    job["similarity"] = 0.5  # Default similarity
                    job["base_similarity"] = 0.5
                    job["domain_boost"] = 0.0
                    job["primary_domain"] = resume_analysis["primary_domain"]
                    job["subdomain"] = resume_analysis.get("subdomain", "")
            
            # Get top results
            top_jobs = ranked_jobs[:DEFAULT_TOP_RESULTS]
            
            # Save to CSV
            csv_filename = f"job_recommendations_{secure_filename(file.filename)}.csv"
            csv_path = os.path.join(os.getcwd(), csv_filename)
            save_to_csv(top_jobs, csv_path)
            
            # Prepare response data with detailed analysis
            response_data = {
                'success': True,
                'message': 'Resume analyzed and jobs fetched successfully!',
                'resume_analysis': {
                    'primary_domain': resume_analysis['primary_domain'].replace('_', ' ').title(),
                    'subdomain': resume_analysis.get('subdomain', 'N/A').replace('_', ' ').title(),
                    'primary_score': resume_analysis['primary_score'],
                    'top_domains': [
                        {
                            'domain': domain.replace('_', ' ').title(),
                            'score': data['score']
                        } for domain, data in resume_analysis['top_domains']
                    ],
                    'detailed_analysis': {
                        domain.replace('_', ' ').title(): {
                            'score': data['score'],
                            'keyword_matches': data['keyword_matches'],
                            'framework_matches': data['framework_matches'],
                            'tool_matches': data['tool_matches']
                        } for domain, data in resume_analysis['all_domains'].items()
                    }
                },
                'query': auto_query,
                'location': location,
                'jobs_count': len(top_jobs),
                'extracted_text': resume_text[:1000] + '...' if len(resume_text) > 1000 else resume_text,
                'top_jobs': [
                    {
                        'title': job.get('title', ''),
                        'company': job.get('company_name', ''),
                        'location': job.get('location', ''),
                        'source': job.get('via', ''),
                        'similarity': round(job.get('similarity', 0.0) * 100, 2),
                        'base_similarity': round(job.get('base_similarity', 0.0) * 100, 2),
                        'domain_boost': round(job.get('domain_boost', 0.0) * 100, 2),
                        'apply_link': job.get('share_link') or job.get('link') or '',
                        'description': job.get('description', '')[:200] + '...' if job.get('description') else ''
                    } for job in top_jobs
                ],
                'csv_download': csv_filename
            }
            
            return jsonify(response_data)
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        print(f"Error processing resume: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'An error occurred while processing your resume: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_csv(filename):
    """Download the generated CSV file."""
    try:
        file_path = os.path.join(os.getcwd(), filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    