import torch
import torch.nn.functional as F
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from typing import Dict, Any
import logging
import os

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """
    Inference class for FinVani Sentiment Model.
    """
    # Mapping for cardiffnlp/twitter-xlm-roberta-base-sentiment
    # 0 -> Negative, 1 -> Neutral, 2 -> Positive
    ID2LABEL = {
        0: "NEGATIVE",
        1: "NEUTRAL",
        2: "POSITIVE"
    }

    def __init__(self, model_path: str = "model_output"):
        """
        Args:
            model_path: HuggingFace model ID or local path.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Check if local path exists, if not fallback to default smaller model to avoid OOM on free tier
        if not os.path.exists(model_path):
            logger.warning(f"Local model path '{model_path}' not found. Downloading lightweight English model (DistilBERT) to save memory...")
            self.model_path = "distilbert-base-uncased-finetuned-sst-2-english"
        else:
            self.model_path = model_path
        
        logger.info(f"Loading multilingual model {self.model_path} on {self.device}...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
            self.model.to(self.device)
            self.model.eval()
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model from {self.model_path}: {e}")
            raise e

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Predict sentiment for a given text.
        Returns: {'label': str, 'score': float}
        """
        inputs = self.tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True, 
            max_length=512,
            padding=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = F.softmax(outputs.logits, dim=1)
        
        # Get the highest probability label
        top_prob, top_idx = torch.max(probabilities, dim=1)
        label_id = top_idx.item()
        
        return {
            "label": self.ID2LABEL.get(label_id, "UNKNOWN"),
            "score": round(top_prob.item(), 4) # Return 4 decimal places
        }

if __name__ == "__main__":
    # Test with dummy data
    try:
        # Assuming running from root: python backend/src/models/infer.py
        # Model output expected at ./model_output/
        analyzer = SentimentAnalyzer(model_path="model_output")
        
        test_headlines = [
            "RBI increases repo rate by 50 bps, hitting MSME loans.",
            "Government announces subsidy for small exporters.",
            "Sensex stays flat ahead of budget announcement."
        ]
        
        print("\n--- Inference Test ---")
        for headline in test_headlines:
            result = analyzer.predict(headline)
            print(f"Text: {headline}")
            print(f"Prediction: {result}\n")
            
    except Exception as e:
        logger.error(f"Usage Error: {e}")
