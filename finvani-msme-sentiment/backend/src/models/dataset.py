import torch
from torch.utils.data import Dataset
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class SentimentDataset(Dataset):
    """
    Custom Dataset for Financial News Sentiment.
    Maps labels: POS -> 0, NEU -> 1, NEG -> 2
    """
    LABEL_MAP = {
        "POS": 0,
        "NEU": 1,
        "NEG": 2
    }

    def __init__(self, data: List[Dict], tokenizer, max_len: int = 128):
        """
        Args:
            data: List of dicts, each containing 'headline' (or 'text') and 'sentiment'.
            tokenizer: HuggingFace tokenizer instance.
            max_len: Maximum sequence length.
        """
        self.data = data
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        item = self.data[index]
        
        # Flexibly handle 'headline' or 'text' keys
        text = item.get("headline") or item.get("text") or ""
        label_str = item.get("sentiment")
        
        # Default to NEU (1) if label is missing or invalid in training data
        label = self.LABEL_MAP.get(label_str, 1)

        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        return {
            'text': text,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }
