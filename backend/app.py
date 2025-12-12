from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
from sentiment_analyzer import analyze_sentiment
from key_points_extractor import extract_key_points

load_dotenv()

app = Flask(__name__)

# CORS configuration - allow Vercel, Render, and local development
allowed_origins_env = os.getenv('ALLOWED_ORIGINS', '')
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(',') if origin.strip()] if allowed_origins_env else []

# Default origins for development
default_origins = [
    'http://localhost:5173',
    'http://localhost:3000',
    'http://localhost:5174',
]

# Determine if we're in production
is_production = os.getenv('FLASK_ENV') == 'production' or os.getenv('ENVIRONMENT') == 'production'

# For production: allow all origins by default (for flexibility with Vercel preview deployments)
# flask-cors doesn't support wildcards like *.vercel.app, so we use "*" for all origins
if is_production:
    if allowed_origins:
        # Use specific origins if provided
        cors_origins = allowed_origins
        print(f"[CORS] Production mode: Using specific origins: {cors_origins}")
    else:
        # Allow all origins in production if not specified (for flexibility)
        # This allows Vercel preview deployments and Render deployments
        cors_origins = "*"
        print("[CORS] Production mode: Allowing all origins (*)")
else:
    # In development, use default localhost origins
    cors_origins = default_origins
    print(f"[CORS] Development mode: Using localhost origins: {cors_origins}")

# Configure CORS with explicit options
CORS(app, resources={
    r"/api/*": {
        "origins": cors_origins,
        "methods": ["GET", "POST", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": False,
        "expose_headers": ["Content-Type"],
        "max_age": 3600
    }
})

# Add manual CORS headers for OPTIONS requests (preflight) to ensure they work
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({})
        origin = request.headers.get("Origin", "*")
        if cors_origins == "*":
            response.headers.add("Access-Control-Allow-Origin", "*")
        elif origin in cors_origins:
            response.headers.add("Access-Control-Allow-Origin", origin)
        else:
            response.headers.add("Access-Control-Allow-Origin", cors_origins[0] if cors_origins else "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        response.headers.add("Access-Control-Max-Age", "3600")
        return response

# Add CORS headers to all responses (including errors)
@app.after_request
def after_request(response):
    # Add CORS headers to all responses
    origin = request.headers.get("Origin", "*")
    if cors_origins == "*":
        response.headers.add("Access-Control-Allow-Origin", "*")
    elif isinstance(cors_origins, list) and origin in cors_origins:
        response.headers.add("Access-Control-Allow-Origin", origin)
    elif isinstance(cors_origins, list) and cors_origins:
        response.headers.add("Access-Control-Allow-Origin", cors_origins[0])
    else:
        response.headers.add("Access-Control-Allow-Origin", "*")
    
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
    response.headers.add("Access-Control-Allow-Credentials", "false")
    return response

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/review_analyzer'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Database Model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(20), nullable=False)
    sentiment_score = db.Column(db.Float, nullable=True)
    key_points = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'review_text': self.review_text,
            'sentiment': self.sentiment,
            'sentiment_score': self.sentiment_score,
            'key_points': self.key_points,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# Create tables
with app.app_context():
    db.create_all()


@app.route('/api/analyze-review', methods=['POST'])
def analyze_review():
    try:
        data = request.get_json()
        
        if not data or 'review_text' not in data:
            return jsonify({'error': 'review_text is required'}), 400
        
        review_text = data['review_text'].strip()
        
        if not review_text:
            return jsonify({'error': 'review_text cannot be empty'}), 400
        
        # Analyze sentiment using Hugging Face
        print(f"[INFO] Menganalisis sentimen untuk review: {review_text[:50]}...")
        sentiment_result = analyze_sentiment(review_text)
        print(f"[SUCCESS] Sentimen: {sentiment_result['label']} (score: {sentiment_result.get('score', 0):.2f})")
        
        # Extract key points using AI (Groq/Hugging Face/Gemini) or smart extraction
        print("[INFO] Mengekstrak poin penting...")
        key_points = extract_key_points(review_text)
        print("[SUCCESS] Poin penting berhasil diekstrak")
        
        # Save to database
        review = Review(
            review_text=review_text,
            sentiment=sentiment_result['label'],
            sentiment_score=sentiment_result.get('score', 0.0),
            key_points=key_points
        )
        
        db.session.add(review)
        db.session.commit()
        
        return jsonify({
            'id': review.id,
            'review_text': review.review_text,
            'sentiment': review.sentiment,
            'sentiment_score': review.sentiment_score,
            'key_points': review.key_points,
            'created_at': review.created_at.isoformat() if review.created_at else None
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    try:
        print("[INFO] Fetching reviews from database...")
        reviews = Review.query.order_by(Review.created_at.desc()).all()
        print(f"[SUCCESS] Found {len(reviews)} reviews")
        return jsonify([review.to_dict() for review in reviews]), 200
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"[ERROR] Gagal memuat reviews: {str(e)}")
        print(f"[ERROR] Traceback: {error_trace}")
        # Return error with CORS headers (handled by after_request)
        return jsonify({'error': str(e), 'details': error_trace[:500]}), 500


@app.route('/api/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    try:
        review = Review.query.get(review_id)
        
        if not review:
            return jsonify({'error': 'Review tidak ditemukan'}), 404
        
        db.session.delete(review)
        db.session.commit()
        
        print(f"[SUCCESS] Review ID {review_id} berhasil dihapus")
        return jsonify({'message': 'Review berhasil dihapus', 'id': review_id}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Gagal menghapus review: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    # Development mode
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))


