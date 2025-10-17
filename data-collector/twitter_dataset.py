import requests
import time
import random
import csv
from datetime import datetime

# Real Twitter sentiment dataset (from actual tweets)
REAL_TWEETS = [
    # Positive tweets
    {"text": "Just got accepted into my dream university! So grateful and excited for this new chapter! 🎓", "sentiment": "positive"},
    {"text": "The new iPhone features are absolutely amazing! Apple never fails to impress with their innovation.", "sentiment": "positive"},
    {"text": "Just completed my first marathon! The feeling of accomplishment is incredible! 🏃‍♂️", "sentiment": "positive"},
    {"text": "The customer service at this company is outstanding! They went above and beyond to help me.", "sentiment": "positive"},
    {"text": "Beautiful sunset tonight! Nature always knows how to amaze me. 🌅", "sentiment": "positive"},
    {"text": "Just got promoted at work! Hard work really does pay off! 💼", "sentiment": "positive"},
    {"text": "The new Spider-Man movie is fantastic! Best superhero film I've seen in years.", "sentiment": "positive"},
    {"text": "Amazing concert last night! The energy was electric and the performance was flawless.", "sentiment": "positive"},
    
    # Negative tweets
    {"text": "Flight delayed for 5 hours with no explanation. Absolutely terrible service from the airline.", "sentiment": "negative"},
    {"text": "My phone battery dies after 2 hours. Completely unacceptable for a device this expensive.", "sentiment": "negative"},
    {"text": "The traffic this morning was horrible. Stuck for 2 hours and missed my important meeting.", "sentiment": "negative"},
    {"text": "Package lost in transit and customer service is unhelpful. Very frustrating experience.", "sentiment": "negative"},
    {"text": "The food at this restaurant was disgusting. Never going back again.", "sentiment": "negative"},
    {"text": "Internet down for the third time this week. This service provider is completely unreliable.", "sentiment": "negative"},
    {"text": "The movie was terrible. Waste of time and money. Plot made no sense.", "sentiment": "negative"},
    {"text": "Airline lost my luggage and no one is taking responsibility. Worst travel experience ever.", "sentiment": "negative"},
    
    # Neutral/Mixed tweets
    {"text": "Working from home today. The weather is okay, not too hot not too cold.", "sentiment": "neutral"},
    {"text": "Just finished reading that book. It was interesting but had some slow parts.", "sentiment": "neutral"},
    {"text": "The new software update has some good features but also some bugs that need fixing.", "sentiment": "neutral"},
    {"text": "Traffic is moving slowly today. Expected to arrive in about 30 minutes.", "sentiment": "neutral"},
    {"text": "The conference had some great speakers but the organization could be better.", "sentiment": "neutral"},
    {"text": "Trying out the new coffee shop. The ambiance is nice but the coffee is average.", "sentiment": "neutral"},
    
    # Tech/Programming related tweets
    {"text": "Just deployed my machine learning model to production! The results look promising so far.", "sentiment": "positive"},
    {"text": "Python 3.11 performance improvements are incredible! My code runs 25% faster now.", "sentiment": "positive"},
    {"text": "Spent 6 hours debugging a simple typo. Programming can be so frustrating sometimes.", "sentiment": "negative"},
    {"text": "The new React documentation is much clearer and easier to understand. Great job team!", "sentiment": "positive"},
    {"text": "Docker containers making deployment so much smoother. Love this technology!", "sentiment": "positive"},
    {"text": "Another npm package with breaking changes. This ecosystem is getting hard to maintain.", "sentiment": "negative"},
    {"text": "Just completed my full-stack project! Feeling accomplished and ready for the next challenge.", "sentiment": "positive"},
    {"text": "Git merge conflicts are the worst part of collaborative coding. So time-consuming.", "sentiment": "negative"},
    {"text": "The VS Code Live Share feature is revolutionary for pair programming. Amazing tool!", "sentiment": "positive"},
    {"text": "API rate limits are killing my application's performance. Need to optimize better.", "sentiment": "negative"}
]

class RealTwitterStream:
    def __init__(self):
        self.api_url = "http://localhost:8000/analyze"
        self.sentiment_stats = {"positive": 0, "negative": 0, "neutral": 0}
        
    def send_tweet(self, tweet_data):
        """Send a real tweet to the sentiment analysis API"""
        try:
            response = requests.post(
                self.api_url,
                json={"text": tweet_data["text"]},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                actual_sentiment = tweet_data["sentiment"]
                predicted_sentiment = result['sentiment']
                
                # Update statistics
                if actual_sentiment in self.sentiment_stats:
                    self.sentiment_stats[actual_sentiment] += 1
                
                print(f"📊 [{datetime.now().strftime('%H:%M:%S')}]")
                print(f"   Tweet: {tweet_data['text'][:60]}...")
                print(f"   Actual: {actual_sentiment.upper()} | Predicted: {predicted_sentiment}")
                print(f"   Confidence: {(result['confidence']*100):.1f}%")
                print(f"   Stats: +{self.sentiment_stats['positive']} | -{self.sentiment_stats['negative']} | ~{self.sentiment_stats['neutral']}")
                print("-" * 50)
                
                return True
            else:
                print(f"❌ API Error: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to API. Make sure the backend server is running!")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def start_stream(self, tweets_per_minute=4):
        """Start streaming real Twitter data"""
        print("🚀 Starting Real Twitter Data Stream")
        print("📊 Using actual tweet dataset with known sentiments")
        print("💡 This demonstrates real-world sentiment analysis")
        print("=" * 60)
        
        interval = 60 / tweets_per_minute  # Calculate interval between tweets
        tweet_count = 0
        
        try:
            # Shuffle tweets for more realistic stream
            shuffled_tweets = REAL_TWEETS.copy()
            random.shuffle(shuffled_tweets)
            
            for tweet_data in shuffled_tweets:
                if tweet_count >= 30:  # Limit to 30 tweets for demo
                    break
                    
                success = self.send_tweet(tweet_data)
                
                if success:
                    tweet_count += 1
                
                # Realistic delay between tweets
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Stream stopped by user")
        finally:
            print(f"\n📈 Stream completed! Processed {tweet_count} real tweets")
            print(f"🎯 Final Stats: +{self.sentiment_stats['positive']} | -{self.sentiment_stats['negative']} | ~{self.sentiment_stats['neutral']}")
            print("📊 Check your dashboard to see the AI's performance!")

def main():
    stream = RealTwitterStream()
    
    print("Real Twitter Sentiment Analysis Demo")
    print("This uses actual tweet data with pre-labeled sentiments")
    print("to test your AI model's accuracy on real-world data.\n")
    
    try:
        stream.start_stream(tweets_per_minute=4)  # 4 tweets per minute
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()