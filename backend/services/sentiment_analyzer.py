"""
Sentiment Analysis Service
Uses Hugging Face transformers for emotion detection
"""

import os
from typing import Dict
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import re

class SentimentAnalyzer:
    """Analyzes sentiment and emotion from text using Hugging Face models"""
    
    def __init__(self):
        self.model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        self.tokenizer = None
        self.model = None
        self.pipeline = None
        self._load_model()
    
    def _load_model(self):
        """Load the sentiment analysis model"""
        try:
            print(f"Loading sentiment model: {self.model_name}")
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                tokenizer=self.model_name,
                device=-1  # Use CPU (-1) or GPU (0) if available
            )
            print("✅ Sentiment model loaded successfully")
        except Exception as e:
            print(f"⚠️ Error loading model: {e}")
            print("Using fallback sentiment analysis")
            self.pipeline = None
    
    def is_ready(self) -> bool:
        """Check if the model is loaded and ready"""
        return self.pipeline is not None
    
    def _clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?]', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text.strip()
    
    def _score_to_label(self, label: str, score: float) -> tuple:
        """
        Convert model output to our label format
        Returns: (label, normalized_score)
        """
        # Map model labels to our emotion labels
        label_map = {
            "positive": "joyful",
            "negative": "anxious",
            "neutral": "neutral",
            "LABEL_0": "negative",  # Some models use LABEL_0, LABEL_1, etc.
            "LABEL_1": "neutral",
            "LABEL_2": "positive"
        }
        
        # Normalize label
        normalized_label = label_map.get(label.lower(), "neutral")
        
        # Normalize score to -1 to 1 range
        # Positive -> 0 to 1, Negative -> -1 to 0, Neutral -> around 0
        if normalized_label == "joyful":
            normalized_score = score  # 0 to 1
        elif normalized_label == "anxious":
            normalized_score = -score  # -1 to 0
        else:
            normalized_score = (score - 0.5) * 0.2  # Small range around 0
        
        return normalized_label, normalized_score
    
    def analyze(self, text: str) -> Dict[str, any]:
        """
        Analyze sentiment of text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with 'label' and 'score'
        """
        if not text or len(text.strip()) == 0:
            return {
                "label": "neutral",
                "score": 0.0
            }
        
        # Clean text
        cleaned_text = self._clean_text(text)
        
        if len(cleaned_text) < 3:
            return {
                "label": "neutral",
                "score": 0.0
            }
        
        # Use model if available
        if self.pipeline:
            try:
                # Truncate to model's max length (usually 512 tokens)
                max_length = 512
                if len(cleaned_text) > max_length:
                    cleaned_text = cleaned_text[:max_length]
                
                result = self.pipeline(cleaned_text)[0]
                label, score = self._score_to_label(
                    result["label"],
                    result["score"]
                )
                
                return {
                    "label": label,
                    "score": round(score, 3)
                }
            except Exception as e:
                print(f"Error in sentiment analysis: {e}")
                # Fall through to fallback
        
        # Fallback: Simple rule-based sentiment
        return self._fallback_analyze(cleaned_text)
    
    def _fallback_analyze(self, text: str) -> Dict[str, any]:
        """Simple fallback sentiment analysis using keyword matching"""
        text_lower = text.lower()
        
        # Positive keywords
        positive_words = ["happy", "joy", "excited", "love", "great", "amazing", "wonderful", "good", "best", "awesome"]
        # Negative keywords
        negative_words = ["sad", "angry", "hate", "terrible", "awful", "bad", "worst", "anxious", "stress", "worried"]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return {"label": "joyful", "score": min(0.7, positive_count * 0.2)}
        elif negative_count > positive_count:
            return {"label": "anxious", "score": max(-0.7, -negative_count * 0.2)}
        else:
            return {"label": "neutral", "score": 0.0}

