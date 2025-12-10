import random
import json
import time
import logging
from typing import List, Dict
try:
    from googletrans import Translator
except ImportError:
    Translator = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SyntheticHeadlineGenerator:
    """
    Generates synthetic financial headlines using:
    1. Template filling (robust)
    2. Back-translation (experimental, requires internet/googletrans)
    """

    TEMPLATES = [
        "{entity} announces new {product} for {target}.",
        "{entity} reports {sentiment} Q3 results amid {condition}.",
        "Government introduces {policy} to boost {target} sector.",
        "{target} owners face {challenge} due to rising {factor}.",
        "RBI {action} interest rates, impacting {target} loans.",
        "Exports from {target} sector {verb} by {percentage} this month.",
        "{entity} partners with {partner} to empower {target}.",
        "Budget 2024: New schemes for {target} expected to {impact} growth."
    ]

    SLOTS = {
        "entity": ["SBI", "HDFC Bank", "Lendingkart", "SIDBI", "Reliance", "Tata Motors"],
        "product": ["loan scheme", "credit line", "digital platform", "insurance cover"],
        "target": ["MSME", "SME", "small business", "textile units", "startups"],
        "sentiment": ["strong", "weak", "record", "disappointing"],
        "condition": ["global slowdown", "festive demand", "inflation", "supply chain issues"],
        "policy": ["PLI scheme", "tax relief", "subsidy", "credit guarantee"],
        "challenge": ["cash crunch", "labor shortage", "high input costs", "regulatory hurdles"],
        "factor": ["fuel prices", "raw material costs", "GST rates", "compliance burden"],
        "action": ["hikes", "cuts", "maintains"],
        "verb": ["surge", "decline", "fall", "jump"],
        "percentage": ["10%", "5%", "20%", "15%"],
        "partner": ["Flipkart", "Amazon", "fintechs", "local trade bodies"],
        "impact": ["accelerate", "hinder", "stall", "revive"]
    }

    def __init__(self):
        self.translator = Translator() if Translator else None
        if not self.translator:
            logger.warning("googletrans not installed or failed to import. Back-translation disabled.")

    def generate_by_template(self, num_samples: int = 10) -> List[str]:
        """Generates headlines by filling random slots in templates."""
        headlines = []
        for _ in range(num_samples):
            template = random.choice(self.TEMPLATES)
            
            # Simple slot filling
            generated = template
            for key, values in self.SLOTS.items():
                placeholder = "{" + key + "}"
                if placeholder in generated:
                    generated = generated.replace(placeholder, random.choice(values))
            
            headlines.append(generated)
        return headlines

    def back_translate(self, texts: List[str], intermediate_lang: str = 'hi') -> List[str]:
        """
        Augments text by translating English -> Intermediate (e.g., Hindi) -> English.
        Adds variation to phrasing.
        """
        if not self.translator:
            logger.error("Translator not available.")
            return []

        augmented = []
        for text in texts:
            try:
                # En -> Hi
                translated = self.translator.translate(text, src='en', dest=intermediate_lang).text
                # Hi -> En
                back_translated = self.translator.translate(translated, src=intermediate_lang, dest='en').text
                
                if back_translated.lower() != text.lower():
                    augmented.append(back_translated)
                
                # Rate limit courtesy
                time.sleep(0.5)
            except Exception as e:
                logger.error(f"Translation failed for '{text}': {e}")
        
        return augmented

def save_synthetic_data(headlines: List[str], output_path: str = "synthetic_headlines.json"):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(headlines, f, indent=2)
    logger.info(f"Saved {len(headlines)} headlines to {output_path}")

if __name__ == "__main__":
    generator = SyntheticHeadlineGenerator()
    
    print("--- Generating Template Definitions ---")
    template_headlines = generator.generate_by_template(num_samples=20)
    for h in template_headlines:
        print(f"Template: {h}")

    # Optional: Test Back-translation if available (commented out by default to avoid hanging if network issues)
    # print("\n--- Testing Back-Translation (En->Hi->En) ---")
    # seeds = ["Small businesses are struggling with high interest rates.", "Government announces new subsidies for exporters."]
    # augmented = generator.back_translate(seeds)
    # for orig, aug in zip(seeds, augmented):
    #     print(f"Original: {orig}")
    #     print(f"Augmented: {aug}")
        
    # Save output
    # save_synthetic_data(template_headlines, "../../../data/processed/synthetic_headlines.json")
