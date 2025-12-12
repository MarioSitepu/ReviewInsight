from transformers import pipeline
import os

# Initialize sentiment analysis pipeline
sentiment_pipeline = None


def get_sentiment_pipeline():
    global sentiment_pipeline
    if sentiment_pipeline is None:
        print("[INFO] Mengunduh model sentiment analysis... (pertama kali bisa memakan waktu 5-10 menit)")
        print("       Model: cardiffnlp/twitter-roberta-base-sentiment-latest (~500MB)")
        # Using a pre-trained model for sentiment analysis
        # Use device_map="cpu" to force CPU usage and reduce memory
        try:
            sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                return_all_scores=True,
                device=-1  # Use CPU (-1) instead of GPU to reduce memory usage
            )
        except Exception as e:
            # Fallback without device specification
            print(f"[WARNING] Error setting device, using default: {e}")
            sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                return_all_scores=True
            )
        print("[SUCCESS] Model berhasil dimuat!")
    return sentiment_pipeline


def analyze_sentiment(text):
    """
    Analyze sentiment of the review text.
    Returns: {'label': 'positive'/'negative'/'neutral', 'score': float}
    """
    try:
        pipeline = get_sentiment_pipeline()
        results = pipeline(text)[0]
        
        # Find the highest score
        best_result = max(results, key=lambda x: x['score'])
        label = best_result['label'].lower()
        score = best_result['score']
        
        # Normalize labels to our expected format
        # Handle different label formats from the model
        label_lower = label.lower()
        
        if 'positive' in label_lower or 'pos' in label_lower or 'label_2' in label_lower:
            normalized_label = 'positive'
        elif 'negative' in label_lower or 'neg' in label_lower or 'label_0' in label_lower:
            normalized_label = 'negative'
        elif 'neutral' in label_lower or 'label_1' in label_lower:
            normalized_label = 'neutral'
        else:
            # Default to neutral if label doesn't match
            normalized_label = 'neutral'
        
        # Additional check for negative keywords (especially for Indonesian)
        # More aggressive detection for Indonesian language
        text_lower = text.lower()
        
        # Strong positive indicators (especially Indonesian)
        strong_positive_indicators = [
            'menarik', 'ketagihan', 'suka', 'sangat suka', 'love', 'loved',
            'bagus', 'baik', 'excellent', 'sempurna', 'perfect', 'menakjubkan', 'amazing',
            'recommended', 'rekomendasi', 'puas', 'satisfied', 'senang', 'happy',
            'worth', 'layak', 'value', 'nilai', 'mantap', 'top', 'terbaik', 'best',
            'cepat', 'fast', 'efisien', 'efficient', 'mudah', 'easy', 'simple',
            'enak', 'lezat', 'tasty', 'delicious', 'wow', 'keren', 'cool', 'great'
        ]
        
        # Strong negative indicators (especially Indonesian)
        strong_negative_indicators = [
            'tidak sesuai', 'tidak memuaskan', 'tidak layak', 'tidak recommended',
            'tidak bagus', 'tidak baik', 'tidak puas', 'tidak worth',
            'tidak sesuai ekspektasi', 'tidak sesuai harapan', 'tidak sesuai dengan',
            'kecewa', 'buruk', 'jelek', 'rusak', 'masalah', 'cacat', 'menyesal',
            'mahal', 'overpriced', 'waste', 'disappointed', 'terrible', 'awful',
            'not worth', 'poor quality', 'bad quality', 'does not meet', 'doesn\'t meet',
            'kurang', 'lemah', 'gagal', 'gajelas', 'gaje', 'gak jelas', 'tidak jelas',
            'aneh', 'weird', 'strange', 'tidak enak', 'tidak nyaman', 'tidak nyaman',
            'bau', 'busuk', 'tidak fresh', 'tidak segar', 'tidak layak konsumsi'
        ]
        
        # Indonesian slang/colloquial negative words (kata-kata kasar/frustrasi)
        negative_slang = [
            'gajelas', 'gaje', 'gak jelas', 'gak jelas', 'gak jelas',
            'apalah', 'apaan', 'apa ini', 'apa sih', 'gimana sih',
            'woi', 'weh', 'waduh', 'astaga', 'ya ampun',
            'sampah', 'rubbish', 'trash', 'junk', 'garbage',
            'ngaco', 'ngawur', 'sembarangan', 'asal-asalan'
        ]
        
        # Check for negative slang/colloquial expressions
        has_negative_slang = any(slang in text_lower for slang in negative_slang)
        
        # Check for frustration patterns (short reviews with exclamations/interjections)
        is_short_frustrated = len(text.strip()) < 50 and any(word in text_lower for word in [
            'woi', 'weh', 'apalah', 'apaan', 'gajelas', 'gaje', 'gimana', 'kenapa'
        ])
        
        # Check for positive and negative patterns
        has_positive = any(indicator in text_lower for indicator in strong_positive_indicators)
        has_negative = any(indicator in text_lower for indicator in strong_negative_indicators)
        
        # Get all scores
        negative_score = next((r['score'] for r in results if 'neg' in r['label'].lower() or 'label_0' in r['label'].lower()), 0)
        positive_score = next((r['score'] for r in results if 'pos' in r['label'].lower() or 'label_2' in r['label'].lower()), 0)
        neutral_score = next((r['score'] for r in results if 'neutral' in r['label'].lower() or 'label_1' in r['label'].lower()), 0)
        
        # Priority 0: Check for strong positive indicators
        if has_positive:
            # Check for very strong positive words
            very_positive_words = ['menarik', 'ketagihan', 'suka', 'love', 'bagus', 'baik', 'excellent', 'sempurna', 'mantap', 'terbaik']
            has_very_positive = any(word in text_lower for word in very_positive_words)
            
            if has_very_positive and (normalized_label == 'neutral' or normalized_label == 'negative'):
                normalized_label = 'positive'
                score = max(positive_score, 0.7)  # High confidence for very positive words
                print(f"[WARNING] Override: Detected very positive keywords, changing to positive (score: {score:.2f})")
            elif normalized_label == 'neutral' and positive_score > 0.2:
                normalized_label = 'positive'
                score = max(positive_score, 0.65)
                print(f"[WARNING] Override: Detected positive keywords, changing from neutral to positive (score: {score:.2f})")
        
        # Priority 1: Check for negative slang/frustration (very strong indicator)
        elif has_negative_slang or is_short_frustrated:
            if normalized_label != 'negative':
                normalized_label = 'negative'
                score = max(negative_score, 0.7)  # High confidence for slang/frustration
                print(f"[WARNING] Override: Detected negative slang/frustration, changing to negative (score: {score:.2f})")
        
        # Priority 2: More aggressive override for Indonesian negative patterns
        elif has_negative:
            # Check for specific strong negative patterns
            very_negative_patterns = [
                'tidak sesuai', 'tidak memuaskan', 'tidak layak', 'kecewa',
                'buruk', 'jelek', 'rusak', 'masalah', 'cacat', 'gajelas', 'gaje',
                'tidak enak', 'bau', 'busuk', 'aneh', 'weird'
            ]
            has_very_negative = any(pattern in text_lower for pattern in very_negative_patterns)
            
            # If model says neutral/positive but text has very negative words, override
            if (normalized_label == 'neutral' or normalized_label == 'positive') and has_very_negative:
                normalized_label = 'negative'
                score = max(negative_score, 0.65)  # Set minimum score to 0.65
                print(f"[WARNING] Override: Detected very negative keywords, changing from {normalized_label} to negative (score: {score:.2f})")
            # If model says neutral but has any negative indicator
            elif normalized_label == 'neutral' and has_negative:
                # More aggressive: override even if negative_score is low
                normalized_label = 'negative'
                score = max(negative_score, 0.6)
                print(f"[WARNING] Override: Detected negative keywords, changing from neutral to negative (score: {score:.2f})")
        
        # Priority 3: For short reviews with negative tone, be more aggressive
        elif len(text.strip()) < 30:
            # Check if it's likely negative based on tone
            negative_tone_words = ['woi', 'apalah', 'gajelas', 'gaje', 'jelek', 'buruk', 'aneh']
            if any(word in text_lower for word in negative_tone_words):
                if normalized_label == 'neutral' and negative_score > 0.15:  # Lower threshold for short reviews
                    normalized_label = 'negative'
                    score = max(negative_score, 0.65)
                    print(f"[WARNING] Override: Short review with negative tone, changing to negative (score: {score:.2f})")
        
        return {
            'label': normalized_label,
            'score': float(score)
        }
    except Exception as e:
        # Fallback to neutral if analysis fails
        print(f"Sentiment analysis error: {str(e)}")
        return {
            'label': 'neutral',
            'score': 0.5
        }

