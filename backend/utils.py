import re
import string

def preprocess_text(text):
    """
    Preprocess text for emotion analysis
    
    Args:
        text (str): Raw input text
        
    Returns:
        str: Cleaned and preprocessed text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Keep basic punctuation for sentiment analysis
    # (exclamation marks and question marks are important for emotion detection)
    
    return text

def clean_text_advanced(text):
    """
    Advanced text cleaning (optional - for future use)
    
    Args:
        text (str): Raw input text
        
    Returns:
        str: Deeply cleaned text
    """
    # Remove special characters but keep important punctuation
    text = re.sub(r'[^\w\s!?.,]', '', text)
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove extra spaces
    text = ' '.join(text.split())
    
    return text

def extract_features(text):
    """
    Extract additional features from text
    
    Args:
        text (str): Input text
        
    Returns:
        dict: Extracted features
    """
    features = {}
    
    # Count exclamation marks
    features['exclamation_marks'] = text.count('!')
    
    # Count question marks
    features['question_marks'] = text.count('?')
    
    # Count capitalized words
    words = text.split()
    features['capitalized_words'] = sum(1 for word in words if word.isupper() and len(word) > 1)
    
    # Text length
    features['text_length'] = len(text)
    
    # Word count
    features['word_count'] = len(words)
    
    return features