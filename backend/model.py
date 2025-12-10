import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from utils import preprocess_text
import logging

logger = logging.getLogger(__name__)

class EmotionAnalyzer:
    """
    Emotion analysis engine using TextBlob and VADER sentiment analysis
    """
    
    def __init__(self):
        """Initialize sentiment analyzers"""
        self.vader = SentimentIntensityAnalyzer()
        logger.info("EmotionAnalyzer initialized successfully")
    
    def analyze(self, text):
        """
        Main analysis function
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            dict: Analysis results with emotion, confidence, and scores
        """
        # Preprocess text
        processed_text = preprocess_text(text)
        
        # Get sentiment scores
        vader_scores = self.vader.polarity_scores(processed_text)
        blob = TextBlob(processed_text)
        
        # Calculate emotion scores
        emotion_scores = self._calculate_emotion_scores(vader_scores, blob)
        
        # Determine primary emotion
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        
        # Calculate confidence
        confidence = self._calculate_confidence(emotion_scores)
        
        # Prepare result
        result = {
            'emotion': primary_emotion,
            'confidence': round(confidence, 2),
            'scores': {k: round(v, 2) for k, v in emotion_scores.items()}
        }
        
        logger.info(f"Analysis result: {result['emotion']} ({result['confidence']})")
        return result
    
    def _calculate_emotion_scores(self, vader_scores, blob):
        """
        Calculate scores for each emotion category
        
        Args:
            vader_scores (dict): VADER sentiment scores
            blob (TextBlob): TextBlob object for polarity/subjectivity
            
        Returns:
            dict: Emotion scores (0-1) for each category
        """
        # Extract VADER scores
        compound = vader_scores['compound']
        pos = vader_scores['pos']
        neg = vader_scores['neg']
        neu = vader_scores['neu']
        
        # Extract TextBlob scores
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Initialize emotion scores
        scores = {
            'happy': 0.0,
            'sad': 0.0,
            'angry': 0.0,
            'neutral': 0.0,
            'surprise': 0.0
        }
        
        # Calculate Happy score
        if compound > 0.05:
            scores['happy'] = min(1.0, pos * 0.7 + (polarity + 1) / 2 * 0.3)
        
        # Calculate Sad score
        if compound < -0.05:
            scores['sad'] = min(1.0, neg * 0.6 + (1 - (polarity + 1) / 2) * 0.4)
        
        # Calculate Angry score
        if compound < -0.3:
            scores['angry'] = min(1.0, neg * 0.8 + subjectivity * 0.2)
        
        # Calculate Neutral score
        scores['neutral'] = min(1.0, neu * 0.7 + (1 - subjectivity) * 0.3)
        
        # Calculate Surprise score (based on subjectivity)
        scores['surprise'] = min(1.0, subjectivity * 0.5)
        
        # Normalize scores to sum to 1.0
        total = sum(scores.values())
        if total > 0:
            scores = {k: v / total for k, v in scores.items()}
        else:
            # If all zeros, set neutral to 1.0
            scores['neutral'] = 1.0
        
        return scores
    
    def _calculate_confidence(self, emotion_scores):
        """
        Calculate confidence score based on emotion score distribution
        
        Args:
            emotion_scores (dict): Emotion scores
            
        Returns:
            float: Confidence score (0-1)
        """
        # Get max score
        max_score = max(emotion_scores.values())
        
        # Get second highest score
        sorted_scores = sorted(emotion_scores.values(), reverse=True)
        second_max = sorted_scores[1] if len(sorted_scores) > 1 else 0
        
        # Calculate confidence based on difference between top two scores
        confidence = max_score - second_max
        
        # Boost confidence if max score is very high
        if max_score > 0.7:
            confidence = min(1.0, confidence + 0.2)
        
        return confidence