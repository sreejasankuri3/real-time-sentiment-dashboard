from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import random

print("🚀 Starting Sentiment Analysis API...")
print("✅ API Ready!")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store data
analysis_data = []

class TextData(BaseModel):
    text: str

def simple_sentiment_analysis(text):
    """Simple rule-based sentiment analysis"""
    positive_words = ['love', 'good', 'great', 'excellent', 'amazing', 'fantastic', 'wonderful', 'happy', 'awesome', 'perfect']
    negative_words = ['hate', 'bad', 'terrible', 'awful', 'horrible', 'sad', 'angry', 'disappointing', 'worst', 'hate']
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return 'POSITIVE', 0.8 + random.random() * 0.2
    elif negative_count > positive_count:
        return 'NEGATIVE', 0.8 + random.random() * 0.2
    else:
        return 'NEUTRAL', 0.5 + random.random() * 0.3

@app.get("/")
def home():
    return {"message": "Sentiment Analysis API is running!", "status": "OK"}

@app.post("/analyze")
def analyze_text(data: TextData):
    print(f"📊 Analyzing: {data.text[:50]}...")
    
    # Use our simple sentiment analysis
    sentiment, confidence = simple_sentiment_analysis(data.text)
    
    response_data = {
        "text": data.text,
        "sentiment": sentiment,
        "confidence": round(confidence, 4),
        "timestamp": datetime.now().isoformat()
    }
    
    analysis_data.append(response_data)
    if len(analysis_data) > 50:
        analysis_data.pop(0)
    
    print(f"✅ {sentiment} ({(confidence*100):.1f}% confidence)")
    return response_data

@app.get("/stats")
def get_stats():
    if not analysis_data:
        return {"data": [], "stats": {"positive": 0, "negative": 0, "neutral": 0, "total": 0}}
    
    positive = sum(1 for item in analysis_data if item['sentiment'] == 'POSITIVE')
    negative = sum(1 for item in analysis_data if item['sentiment'] == 'NEGATIVE')
    neutral = sum(1 for item in analysis_data if item['sentiment'] == 'NEUTRAL')
    
    return {
        "data": analysis_data[-10:],
        "stats": {
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "total": len(analysis_data)
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy", "records": len(analysis_data)}

if __name__ == "__main__":
    import uvicorn
    print("🌐 Server starting at: http://localhost:8000")
    print("📊 Check stats at: http://localhost:8000/stats")
    print("❤️  Health check: http://localhost:8000/health")
    print("\n🎯 Try analyzing text by sending POST requests to http://localhost:8000/analyze")
    uvicorn.run(app, host="0.0.0.0", port=8000)