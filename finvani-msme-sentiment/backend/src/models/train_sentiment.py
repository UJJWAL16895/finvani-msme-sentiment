import os
import torch
import logging
import json
import numpy as np
from torch.utils.data import DataLoader
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from torch.optim import AdamW
from sklearn.metrics import accuracy_score, f1_score
from typing import List, Dict

# Adjust import based on where this script is run from
try:
    from src.models.dataset import SentimentDataset
except ImportError:
    # Fallback for running directly as script
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    from src.models.dataset import SentimentDataset

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SentimentTrainer:
    def __init__(self, model_name: str = "distilbert-base-uncased", num_labels: int = 3, learning_rate: float = 2e-5):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = model_name
        
        logger.info(f"Loading tokenizer and model: {model_name}")
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_name)
        self.model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
        self.model.to(self.device)
        
        self.optimizer = AdamW(self.model.parameters(), lr=learning_rate)
        self.loss_fn = torch.nn.CrossEntropyLoss()

    def train(self, train_loader: DataLoader, epochs: int = 3):
        self.model.train()
        for epoch in range(epochs):
            total_loss = 0
            logger.info(f"Epoch {epoch + 1}/{epochs} started.")
            
            for batch in train_loader:
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['labels'].to(self.device)

                self.optimizer.zero_grad()

                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )
                
                loss = outputs.loss
                total_loss += loss.item()

                loss.backward()
                self.optimizer.step()

            avg_loss = total_loss / len(train_loader)
            logger.info(f"Epoch {epoch + 1} completed. Average Loss: {avg_loss:.4f}")

    def evaluate(self, val_loader: DataLoader) -> Dict[str, float]:
        self.model.eval()
        predictions, true_labels = [], []

        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['labels'].to(self.device)

                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask
                )
                
                _, preds = torch.max(outputs.logits, dim=1)
                
                predictions.extend(preds.cpu().tolist())
                true_labels.extend(labels.cpu().tolist())

        acc = accuracy_score(true_labels, predictions)
        f1 = f1_score(true_labels, predictions, average='weighted')
        
        return {"accuracy": acc, "f1_score": f1}

    def save_model(self, output_dir: str = "model_output"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        logger.info(f"Saving model to {output_dir}")
        
        # Save model state dict
        model_path = os.path.join(output_dir, "model_state.bin")
        torch.save(self.model.state_dict(), model_path)
        
        # Save tokenizer
        self.tokenizer.save_pretrained(output_dir)
        
        # Save config (optional, but good for loading)
        self.model.config.save_pretrained(output_dir)
        logger.info("Model saved successfully.")

def main():
    # Dummy Data for Testing
    dummy_data = [
        {"headline": "Profits soar for MSME sector", "sentiment": "POS"},
        {"headline": "Severe losses reported due to inflation", "sentiment": "NEG"},
        {"headline": "Market remains stable today", "sentiment": "NEU"},
        {"headline": "Government announces new loan scheme", "sentiment": "POS"},
        {"headline": "Restrictions imposed on exports", "sentiment": "NEG"},
    ] * 10  # Duplicate to simulate batch

    logger.info("Initializing Trainer...")
    trainer = SentimentTrainer()
    
    logger.info("Preparing Dataset...")
    dataset = SentimentDataset(dummy_data, trainer.tokenizer)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)
    
    logger.info("Starting Training...")
    trainer.train(dataloader, epochs=1)
    
    logger.info("Evaluating...")
    metrics = trainer.evaluate(dataloader)
    logger.info(f"Validation Metrics: {metrics}")
    
    logger.info("Saving Model...")
    trainer.save_model("model_output")

if __name__ == "__main__":
    main()
