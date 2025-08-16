#!/usr/bin/env python3
"""
Configuration file for the Job Recommendation System.
Set your API keys and preferences here.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# API Configuration
SERPAPI_API_KEY = "75a0c460c0c121a971d74635c7d92497ca22ba10a33ab43e8557dfcf9a058e83"

# Default Settings
DEFAULT_LOCATION = os.getenv("DEFAULT_LOCATION", "Bangalore")
DEFAULT_TOP_RESULTS = int(os.getenv("DEFAULT_TOP_RESULTS", "10"))
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "all-MiniLM-L6-v2")

# Check if API key is configured
def check_api_key():
    """Check if the API key is properly configured."""
    if not SERPAPI_API_KEY or SERPAPI_API_KEY == "75a0c460c0c121a971d74635c7d92497ca22ba10a33ab43e8557dfcf9a058e83":
        print("⚠️  WARNING: SerpApi API key not configured!")
        print("   Please set your API key in one of these ways:")
        print("   1. Edit config.py and set SERPAPI_API_KEY")
        print("   2. Set environment variable: $env:SERPAPI_API_KEY='your_key'")
        print("   3. Use command line: --api-key 'your_key'")
        print("   4. Get free API key from: https://serpapi.com")
        return False
    return True

if __name__ == "__main__":
    check_api_key()
