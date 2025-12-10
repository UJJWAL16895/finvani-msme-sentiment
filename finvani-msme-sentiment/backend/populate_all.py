import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.abspath("."))

from src.ingestion.rss_google_news import GoogleNewsIngester, LANGUAGES

def run():
    print("Starting full ingestion for 22 languages...")
    
    # Define queries
    queries = [
        "MSME",
        "SME India", 
        "Business Loan",
        "Economy India",
        "Finance Ministry",
        "RBI"
    ]
    
    # Ensure data dir is correct (project root)
    base_path = Path("../data/raw").resolve()
    print(f"Saving data to: {base_path}")
    
    ingester = GoogleNewsIngester(str(base_path))
    ingester.run_ingestion(queries, LANGUAGES)
    print("Full ingestion complete.")

if __name__ == "__main__":
    run()
