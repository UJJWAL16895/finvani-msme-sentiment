import feedparser
import json
import hashlib
import logging
import datetime
import os
from dateutil import parser as date_parser
import urllib.parse
from pathlib import Path
from typing import List, Dict, Any, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GoogleNewsIngester:
    BASE_URL = "https://news.google.com/rss/search"
    
    def __init__(self, data_dir: str = "../../../data/raw"):
        self.data_dir = Path(data_dir).resolve()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.seen_hashes: Set[str] = set()

    def _generate_hash(self, article: Dict[str, Any]) -> str:
        """Generate a unique hash for an article based on URL and title."""
        unique_string = f"{article.get('link', '')}{article.get('title', '')}"
        return hashlib.md5(unique_string.encode('utf-8')).hexdigest()

    def _load_existing_hashes(self, filepath: Path):
        """Load existing hashes from today's file to avoid duplicates on re-run."""
        if not filepath.exists():
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        if 'id' in record:
                            self.seen_hashes.add(record['id'])
                    except json.JSONDecodeError:
                        continue
            logger.info(f"Loaded {len(self.seen_hashes)} existing unique hashes.")
        except Exception as e:
            logger.error(f"Error loading existing hashes: {e}")

    def fetch_feed(self, query: str, lang: str = "en") -> List[Dict[str, Any]]:
        """Fetch news entries from Google News RSS feed."""
        # Clean query and construct URL
        # hl: language, gl: country (IN), ceid: country:language
        encoded_query = urllib.parse.quote_plus(query)
        params = f"q={encoded_query}&hl={lang}-IN&gl=IN&ceid=IN:{lang}"
        url = f"{self.BASE_URL}?{params}"
        
        logger.info(f"Fetching feed for query='{query}', lang='{lang}'")
        
        try:
            feed = feedparser.parse(url)
            
            if feed.bozo:
                logger.warning(f"Feed malformed or error: {feed.bozo_exception}")
            
            articles = []
            for entry in feed.entries:
                
                published_dt = None
                if 'published' in entry:
                    try:
                        published_dt = str(date_parser.parse(entry.published))
                    except:
                        published_dt = str(datetime.datetime.now())
                
                article = {
                    "source": "google_news",
                    "query": query,
                    "language": lang,
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "published": published_dt,
                    "summary": entry.get("summary", ""),
                    "fetched_at": str(datetime.datetime.now())
                }
                
                # Generate hash ID
                article_id = self._generate_hash(article)
                article["id"] = article_id
                
                if article_id not in self.seen_hashes:
                    articles.append(article)
                    self.seen_hashes.add(article_id)
                
            logger.info(f"Found {len(articles)} new unique articles.")
            return articles
            
        except Exception as e:
            logger.error(f"Failed to fetch feed: {e}")
            return []

    def save_to_jsonl(self, articles: List[Dict[str, Any]]):
        """Save deduplicated articles to JSONL file."""
        if not articles:
            return

        today = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"{today}.jsonl"
        filepath = self.data_dir / filename
        
        # Load existing hashes if this is the first write/check in this run
        # (Though we effectively did this by keeping self.seen_hashes in memory, 
        # but for robustness across multiple runs of the script, we should load first if not loaded)
        # For this script run, we assume _load_existing_hashes is called at start.
        
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                for article in articles:
                    f.write(json.dumps(article, ensure_ascii=False) + '\n')
            logger.info(f"Saved {len(articles)} articles to {filepath}")
        except Exception as e:
            logger.error(f"Error writing to file: {e}")

    def run_ingestion(self, queries: List[str], languages: List[str]):
        """Run ingestion for all query and language combinations."""
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        filepath = self.data_dir / f"{today}.jsonl"
        self._load_existing_hashes(filepath)
        
        all_articles = []
        for query in queries:
            for lang in languages:
                articles = self.fetch_feed(query, lang)
                all_articles.extend(articles)
        
        self.save_to_jsonl(all_articles)
        logger.info("Ingestion run completed.")

# Official languages (22 Scheduled Languages of India)
# Note: Google News RSS availability varies. Using standard ISO codes.
LANGUAGES = [
    "en", "hi", "bn", "te", "mr", "ta", "ur", "gu", "kn", "ml",
    "or", "pa", "as", "mai", "sat", "ks", "ne", "doi", "gom", "sd",
    "mni", "sa"
]

# Example Usage & Test Snippet
if __name__ == "__main__":
    # Example MSME-focused queries
    QUERIES = [
        "MSME loan scheme India",
        "SME sector growth India",
        "RBI MSME guidelines",
        "small business finance India"
    ]
    
    # Ensure data directory exists relative to script execution or absolute
    # This assumes running from backend/src/ingestion or backend/
    # Adjust path as necessary. We use a relative path that should resolve correctly 
    # if run from monorepo root or backend/
    
    # Fix path for robustness: Assume script is at backend/src/ingestion/rss_google_news.py
    # We want data/ at finvani-msme-sentiment/data/
    
    base_path = Path(__file__).resolve().parent.parent.parent.parent / "data" / "raw"
    print(f"DEBUG: base_path resolve to: {base_path}")
    
    ingester = GoogleNewsIngester(str(base_path))
    ingester.run_ingestion(QUERIES, LANGUAGES)
    
    # Test Snippet Validation
    print("\n--- Verification ---")
    today_file = base_path / f"{datetime.datetime.now().strftime('%Y-%m-%d')}.jsonl"
    if today_file.exists():
        print(f"Success: File created at {today_file}")
        with open(today_file, 'r', encoding='utf-8') as f:
            count = sum(1 for _ in f)
        print(f"Total articles in file: {count}")
    else:
        print("Error: Output file not found.")
