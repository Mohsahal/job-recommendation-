#!/usr/bin/env python3
"""
Setup script to configure your SerpApi API key.
Run this script to set up your API key for the job recommendation system.
"""

import os
import sys

def setup_api_key():
    """Interactive setup for the API key."""
    
    print("🔑 SerpApi API Key Setup")
    print("=" * 50)
    print("This script will help you set up your SerpApi API key.")
    print("Get your free API key from: https://serpapi.com")
    print()
    
    # Check if config.py exists
    if not os.path.exists("config.py"):
        print("❌ config.py not found. Please make sure it exists in the current directory.")
        return False
    
    # Get API key from user
    api_key = input("Enter your SerpApi API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided.")
        return False
    
    if len(api_key) < 20:
        print("⚠️  Warning: API key seems too short. Please double-check.")
        confirm = input("Continue anyway? (y/N): ").strip().lower()
        if confirm != 'y':
            return False
    
    # Update config.py
    try:
        with open("config.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace the placeholder API key
        if "your_api_key_here" in content:
            content = content.replace("your_api_key_here", api_key)
        else:
            # If no placeholder, update the SERPAPI_API_KEY line
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith("SERPAPI_API_KEY = "):
                    lines[i] = f'SERPAPI_API_KEY = "{api_key}"'
                    break
            content = '\n'.join(lines)
        
        with open("config.py", "w", encoding="utf-8") as f:
            f.write(content)
        
        print("✅ API key saved to config.py successfully!")
        print("🔑 You can now run the job recommendation system:")
        print("   python job_recommender.py --resume resume.txt")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving API key: {e}")
        return False

def check_current_config():
    """Check the current configuration."""
    print("📋 Current Configuration")
    print("=" * 50)
    
    try:
        from config import SERPAPI_API_KEY, DEFAULT_LOCATION, DEFAULT_TOP_RESULTS
        
        if SERPAPI_API_KEY and SERPAPI_API_KEY != "your_api_key_here":
            print(f"✅ API Key: {SERPAPI_API_KEY[:8]}...{SERPAPI_API_KEY[-4:]}")
        else:
            print("❌ API Key: Not configured")
        
        print(f"📍 Default Location: {DEFAULT_LOCATION}")
        print(f"📊 Default Top Results: {DEFAULT_TOP_RESULTS}")
        
    except ImportError:
        print("❌ config.py not found or has errors")
        return False
    
    return True

def main():
    """Main setup function."""
    print("🚀 Job Recommendation System - API Key Setup")
    print("=" * 60)
    
    # Check current config
    check_current_config()
    print()
    
    # Ask what user wants to do
    print("What would you like to do?")
    print("1. Set up new API key")
    print("2. Check current configuration")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        setup_api_key()
    elif choice == "2":
        check_current_config()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()
