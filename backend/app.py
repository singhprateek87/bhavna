from flask import Flask, request, jsonify
from flask_cors import CORS
from model import EmotionAnalyzer
import logging

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize emotion analyzer
analyzer = EmotionAnalyzer()

# ===========================
# API ROUTES
# ===========================

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'message': 'BHAVNA Emotion Analysis API',
        'version': '1.0.0'
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_emotion():
    """
    Analyze emotion from text
    Expected JSON: { "text": "Your text here" }
    Returns: { "emotion": "happy", "confidence": 0.85, "scores": {...} }
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        # Validate input
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing text field in request'
            }), 400
        
        text = data['text']
        
        # Check if text is empty
        if not text or len(text.strip()) == 0:
            return jsonify({
                'error': 'Text cannot be empty'
            }), 400
        
        # Check text length
        if len(text) > 5000:
            return jsonify({
                'error': 'Text too long. Maximum 5000 characters.'
            }), 400
        
        # Analyze emotion
        logger.info(f"Analyzing text: {text[:50]}...")
        result = analyzer.analyze(text)
        
        # Return result
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

# ===========================
# ERROR HANDLERS
# ===========================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ===========================
# RUN APPLICATION
# ===========================

if __name__ == '__main__':
    logger.info("Starting BHAVNA Emotion Analysis API...")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )