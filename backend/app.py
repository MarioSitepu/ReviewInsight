from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime
import os
import sys
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Import AI modules with error handling
try:
    from sentiment_analyzer import analyze_sentiment
    print("[INFO] Sentiment analyzer loaded successfully")
except Exception as e:
    print(f"[ERROR] Failed to load sentiment_analyzer: {e}")
    sys.exit(1)

try:
    from key_points_extractor import extract_key_points
    print("[INFO] Key points extractor loaded successfully")
except Exception as e:
    print(f"[ERROR] Failed to load key_points_extractor: {e}")
    sys.exit(1)

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
# Check multiple environment variables to detect production
is_production = (
    os.getenv('FLASK_ENV') == 'production' or 
    os.getenv('ENVIRONMENT') == 'production' or
    os.getenv('RENDER') == 'true' or  # Render sets this automatically
    os.getenv('FLASK_DEBUG') == '0' or
    (not os.getenv('FLASK_ENV') and not os.getenv('FLASK_DEBUG'))  # Default to production if not explicitly set to dev
)

# Debug: Print environment variables for troubleshooting
print(f"[DEBUG] FLASK_ENV: {os.getenv('FLASK_ENV')}")
print(f"[DEBUG] ENVIRONMENT: {os.getenv('ENVIRONMENT')}")
print(f"[DEBUG] RENDER: {os.getenv('RENDER')}")
print(f"[DEBUG] FLASK_DEBUG: {os.getenv('FLASK_DEBUG')}")
print(f"[DEBUG] is_production: {is_production}")

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

# Handle CORS manually for better control and reliability
# We'll handle all CORS headers manually instead of using Flask-CORS to avoid conflicts

@app.before_request
def handle_preflight():
    """Handle CORS preflight (OPTIONS) requests"""
    if request.method == "OPTIONS":
        response = jsonify({})
        origin = request.headers.get("Origin", "*")
        
        # Set CORS headers
        if cors_origins == "*":
            response.headers["Access-Control-Allow-Origin"] = "*"
        elif isinstance(cors_origins, list) and origin in cors_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
        elif isinstance(cors_origins, list) and cors_origins:
            response.headers["Access-Control-Allow-Origin"] = cors_origins[0]
        else:
            response.headers["Access-Control-Allow-Origin"] = "*"
        
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
        response.headers["Access-Control-Max-Age"] = "3600"
        return response

@app.after_request
def after_request(response):
    """Add CORS headers to all responses"""
    origin = request.headers.get("Origin", "*")
    
    # Set CORS headers (always override to ensure they're present)
    if cors_origins == "*":
        response.headers["Access-Control-Allow-Origin"] = "*"
    elif isinstance(cors_origins, list) and origin in cors_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
    elif isinstance(cors_origins, list) and cors_origins:
        response.headers["Access-Control-Allow-Origin"] = cors_origins[0]
    else:
        response.headers["Access-Control-Allow-Origin"] = "*"
    
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Credentials"] = "false"
    
    return response

# Database configuration
database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/review_analyzer')

# For Neon (and other cloud PostgreSQL), ensure SSL is properly configured
# Neon requires SSL connections, so add sslmode=require if not present
if database_url.startswith('postgresql://') and 'sslmode' not in database_url:
    # Add sslmode=require for secure connections (Neon requires this)
    separator = '&' if '?' in database_url else '?'
    database_url = f"{database_url}{separator}sslmode=require"

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Connection pooling configuration for better reliability
# These settings help with connection timeouts and SSL issues
# Note: connect_args for sslmode should be in the URL, not here
# But we can still configure pool settings
try:
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,  # Verify connections before using them
        'pool_recycle': 300,    # Recycle connections after 5 minutes
        'pool_size': 5,         # Number of connections to maintain
        'max_overflow': 10,     # Additional connections beyond pool_size
    }
    print("[INFO] Database engine options configured")
except Exception as e:
    print(f"[WARNING] Could not set engine options: {e}")

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


# Create tables - wrap in try-except to prevent crash
try:
    with app.app_context():
        # Test database connection first
        try:
            db.session.execute(text('SELECT 1'))
            print("[INFO] Database connection test successful")
        except Exception as conn_error:
            print(f"[WARNING] Database connection test failed: {conn_error}")
            print("[INFO] Will retry when first request comes in")
        
        # Create tables
        try:
            db.create_all()
            print("[INFO] Database tables initialized")
        except Exception as table_error:
            print(f"[WARNING] Could not create tables: {table_error}")
            print("[INFO] Tables may already exist")
except Exception as e:
    print(f"[WARNING] Database initialization error: {e}")
    print("[INFO] App will continue, but database operations may fail")


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
        # Test database connection first
        try:
            db.session.execute(text('SELECT 1'))
            print("[INFO] Database connection OK")
        except Exception as conn_error:
            print(f"[WARNING] Database connection test failed: {conn_error}")
            # Try to reconnect
            db.session.remove()
            db.session.execute(text('SELECT 1'))
            print("[INFO] Database reconnected")
        
        reviews = Review.query.order_by(Review.created_at.desc()).all()
        print(f"[SUCCESS] Found {len(reviews)} reviews")
        return jsonify([review.to_dict() for review in reviews]), 200
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"[ERROR] Gagal memuat reviews: {str(e)}")
        print(f"[ERROR] Traceback: {error_trace}")
        
        # Try to rollback and close connection on error
        try:
            db.session.rollback()
            db.session.remove()
        except:
            pass
        
        # Return error with CORS headers (handled by after_request)
        error_message = str(e)
        # Don't expose full traceback to client, just error message
        return jsonify({'error': 'Gagal memuat review dari database', 'details': error_message[:200]}), 500


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


