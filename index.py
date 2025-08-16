from serpapi import GoogleSearch
import csv
import schedule
import time

# 🔑 Your SerpApi Key
API_KEY = "75a0c460c0c121a971d74635c7d92497ca22ba10a33ab43e8557dfcf9a058e83"

# 🔍 Define your search query
params = {
    "engine": "google_jobs",
    "q": "Software Engineer ",  # change to your job query
    "hl": "en",
    "api_key": API_KEY
}


def fetch_linkedin_jobs():
    """Fetch LinkedIn jobs from SerpApi Google Jobs API and save to CSV."""
    search = GoogleSearch(params)
    results = search.get_dict()
    jobs = results.get("jobs_results", [])

    # Filter only LinkedIn jobs
    linkedin_jobs = [
        job for job in jobs
        if "linkedin" in str(job.get("via", "")).lower()
    ]

    if not linkedin_jobs:
        print("⚠️ No LinkedIn jobs found for this query.")
        return

    print(f"✅ Found {len(linkedin_jobs)} LinkedIn jobs")

    # Print jobs
    for job in linkedin_jobs:
        print("Title:", job.get("title"))
        print("Company:", job.get("company_name"))
        print("Location:", job.get("location"))
        print("Source:", job.get("via"))
        print("Link:", job.get("apply_options", [{}])[0].get("link"))
        print("-" * 60)

    # Save to CSV
    with open("linkedin_jobs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Company", "Location", "Source", "Link"])

        for job in linkedin_jobs:
            writer.writerow([
                job.get("title"),
                job.get("company_name"),
                job.get("location"),
                job.get("via"),
                job.get("apply_options", [{}])[0].get("link")
            ])

    print("💾 LinkedIn jobs saved to linkedin_jobs.csv")


# 🔄 Run immediately once
fetch_linkedin_jobs()

# ⏰ Schedule to run daily at 9:00 AM
schedule.every().day.at("09:00").do(fetch_linkedin_jobs)

# 🕒 Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)
