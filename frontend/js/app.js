// ===========================
// DOM ELEMENTS
// ===========================
const textInput = document.getElementById('textInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const clearBtn = document.getElementById('clearBtn');
const charCounter = document.getElementById('charCounter');
const loader = document.getElementById('loader');
const errorMsg = document.getElementById('errorMsg');
const errorText = document.getElementById('errorText');
const resultsSection = document.getElementById('resultsSection');
const emotionEmoji = document.getElementById('emotionEmoji');
const emotionLabel = document.getElementById('emotionLabel');
const confidenceBar = document.getElementById('confidenceBar');
const confidenceScore = document.getElementById('confidenceScore');

// ===========================
// CONFIGURATION
// ===========================
const API_URL = 'http://localhost:5000/api/analyze'; // Change this for production

// Emotion to Emoji Mapping
const EMOTION_EMOJIS = {
    'happy': '😊',
    'sad': '😔',
    'angry': '😡',
    'neutral': '😐',
    'surprise': '😲',
    'fear': '😨',
    'disgust': '🤢'
};

// Chart instance
let emotionChart = null;

// ===========================
// EVENT LISTENERS
// ===========================
textInput.addEventListener('input', updateCharCounter);
analyzeBtn.addEventListener('click', analyzeEmotion);
clearBtn.addEventListener('click', clearInput);

// Allow Enter key to submit (with Shift+Enter for new line)
textInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        analyzeEmotion();
    }
});

// ===========================
// FUNCTIONS
// ===========================

// Update character counter
function updateCharCounter() {
    const length = textInput.value.length;
    charCounter.textContent = `${length} / 1000`;
    
    if (length > 900) {
        charCounter.style.color = '#ff0050';
    } else {
        charCounter.style.color = '#b0b0b0';
    }
}

// Clear input and results
function clearInput() {
    textInput.value = '';
    updateCharCounter();
    hideResults();
    hideError();
}

// Validate input
function validateInput(text) {
    if (!text || text.trim().length === 0) {
        showError('Please enter some text to analyze.');
        return false;
    }
    
    if (text.trim().length < 3) {
        showError('Please enter at least 3 characters.');
        return false;
    }
    
    return true;
}

// Show error message
function showError(message) {
    errorText.textContent = message;
    errorMsg.classList.remove('hidden');
    setTimeout(() => {
        hideError();
    }, 5000);
}

// Hide error message
function hideError() {
    errorMsg.classList.add('hidden');
}

// Show loader
function showLoader() {
    loader.classList.remove('hidden');
    analyzeBtn.disabled = true;
}

// Hide loader
function hideLoader() {
    loader.classList.add('hidden');
    analyzeBtn.disabled = false;
}

// Hide results
function hideResults() {
    resultsSection.classList.add('hidden');
}

// Analyze emotion (main function)
async function analyzeEmotion() {
    const text = textInput.value;
    
    // Validate input
    if (!validateInput(text)) {
        return;
    }
    
    // Hide previous results and errors
    hideResults();
    hideError();
    
    // Show loader
    showLoader();
    
    try {
        // Make API request
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to connect to the server. Please make sure the backend is running on http://localhost:5000');
    } finally {
        hideLoader();
    }
}

// Display results
function displayResults(data) {
    const { emotion, confidence, scores } = data;
    
    // Set emoji
    emotionEmoji.textContent = EMOTION_EMOJIS[emotion.toLowerCase()] || '🤔';
    
    // Set emotion label
    emotionLabel.textContent = emotion.charAt(0).toUpperCase() + emotion.slice(1);
    
    // Set confidence bar
    const confidencePercent = Math.round(confidence * 100);
    confidenceBar.style.width = `${confidencePercent}%`;
    confidenceScore.textContent = `${confidencePercent}%`;
    
    // Create or update chart
    createEmotionChart(scores);
    
    // Show results with animation
    resultsSection.classList.remove('hidden');
    
    // Scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

// Create emotion chart
function createEmotionChart(scores) {
    const ctx = document.getElementById('emotionChart').getContext('2d');
    
    // Destroy previous chart if exists
    if (emotionChart) {
        emotionChart.destroy();
    }
    
    // Prepare data
    const labels = Object.keys(scores).map(key => 
        key.charAt(0).toUpperCase() + key.slice(1)
    );
    const values = Object.values(scores).map(val => Math.round(val * 100));
    
    // Color gradient
    const colors = [
        'rgba(0, 245, 255, 0.8)',    // Happy - Cyan
        'rgba(131, 56, 236, 0.8)',   // Sad - Purple
        'rgba(255, 0, 110, 0.8)',    // Angry - Pink
        'rgba(6, 255, 165, 0.8)',    // Neutral - Green
        'rgba(255, 195, 0, 0.8)'     // Surprise - Yellow
    ];
    
    // Create chart
    emotionChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Emotion Score (%)',
                data: values,
                backgroundColor: colors,
                borderColor: colors.map(color => color.replace('0.8', '1')),
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#00f5ff',
                    bodyColor: '#ffffff',
                    borderColor: '#00f5ff',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return `${context.parsed.y}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        color: '#b0b0b0',
                        callback: function(value) {
                            return value + '%';
                        }
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        color: '#b0b0b0'
                    },
                    grid: {
                        display: false
                    }
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeInOutQuart'
            }
        }
    });
}

// ===========================
// INITIALIZATION
// ===========================
document.addEventListener('DOMContentLoaded', () => {
    console.log('BHAVNA - Emotion Analysis App Loaded');
    updateCharCounter();
});