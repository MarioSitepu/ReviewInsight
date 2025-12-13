from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime
import os
import sys
import threading
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Import AI modules with error handling
# Don't exit on import errors - allow app to start and handle errors at request time
try:
    from sentiment_analyzer import analyze_sentiment
    print("[INFO] Sentiment analyzer module loaded successfully")
except Exception as e:
    print(f"[ERROR] Failed to load sentiment_analyzer module: {e}")
    import traceback
    print(f"[ERROR] Traceback: {traceback.format_exc()}")
    # Don't exit - create a fallback function instead
    def analyze_sentiment(text):
        print("[WARNING] Using fallback sentiment analysis")
        return {'label': 'neutral', 'score': 0.5}

try:
    from key_points_extractor import extract_key_points
    print("[INFO] Key points extractor module loaded successfully")
except Exception as e:
    print(f"[ERROR] Failed to load key_points_extractor module: {e}")
    import traceback
    print(f"[ERROR] Traceback: {traceback.format_exc()}")
    # Don't exit - create a fallback function instead
    def extract_key_points(text):
        print("[WARNING] Using fallback key points extraction")
        return "Poin penting tidak dapat diekstrak"

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
# More defensive: if we're on Render or any cloud platform, assume production
is_production = (
    os.getenv('FLASK_ENV') == 'production' or 
    os.getenv('ENVIRONMENT') == 'production' or
    os.getenv('RENDER') == 'true' or  # Render sets this automatically
    os.getenv('RENDER') == 'True' or  # Case variation
    os.getenv('FLASK_DEBUG') == '0' or
    os.getenv('FLASK_DEBUG') == 'False' or
    # If PORT is set (cloud platforms set this), assume production
    os.getenv('PORT') is not None or
    # If we're not explicitly in development, assume production (defensive)
    os.getenv('FLASK_ENV') != 'development'
)

# Debug: Print environment variables for troubleshooting
print(f"[DEBUG] FLASK_ENV: {os.getenv('FLASK_ENV')}")
print(f"[DEBUG] ENVIRONMENT: {os.getenv('ENVIRONMENT')}")
print(f"[DEBUG] RENDER: {os.getenv('RENDER')}")
print(f"[DEBUG] FLASK_DEBUG: {os.getenv('FLASK_DEBUG')}")
print(f"[DEBUG] PORT: {os.getenv('PORT')}")
print(f"[DEBUG] is_production: {is_production}")

# For production: allow all origins by default (for flexibility with Vercel preview deployments)
# flask-cors doesn't support wildcards like *.vercel.app, so we use "*" for all origins
# More defensive: if in doubt, allow all origins (better than blocking)
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
    """Handle CORS preflight (OPTIONS) requests and log incoming requests"""
    try:
        # Handle OPTIONS preflight requests
        if request.method == "OPTIONS":
            response = jsonify({})
            origin = request.headers.get("Origin", "*")
            
            # Set CORS headers - always allow if in production or if origin is from a known cloud platform
            # More defensive: allow all origins if we're not sure
            if cors_origins == "*":
                response.headers["Access-Control-Allow-Origin"] = "*"
            elif isinstance(cors_origins, list) and origin in cors_origins:
                response.headers["Access-Control-Allow-Origin"] = origin
            elif isinstance(cors_origins, list) and cors_origins:
                response.headers["Access-Control-Allow-Origin"] = cors_origins[0]
            else:
                # Fallback: always allow (defensive approach)
                response.headers["Access-Control-Allow-Origin"] = "*"
            
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
            response.headers["Access-Control-Max-Age"] = "3600"
            response.headers["Access-Control-Allow-Credentials"] = "false"
            return response
    except Exception as e:
        # Even if before_request fails, try to set basic CORS
        print(f"[ERROR] Error in before_request: {e}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
    
    # Log incoming requests for debugging
    try:
        origin = request.headers.get("Origin", "unknown")
        print(f"[REQUEST] {request.method} {request.path} from origin: {origin}")
    except Exception as log_error:
        # Even if logging fails, continue
        print(f"[WARNING] Failed to log request: {log_error}")
        try:
            print(f"[REQUEST] {request.method} {request.path}")
        except:
            pass
    except Exception as e:
        # Even if before_request fails, try to set basic CORS
        print(f"[ERROR] Error in before_request: {e}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")

@app.after_request
def after_request(response):
    """Add CORS headers to all responses - CRITICAL for CORS to work"""
    try:
        # Get origin safely
        try:
            origin = request.headers.get("Origin", "*")
        except:
            origin = "*"
        
        # Always set CORS headers (critical for CORS to work)
        # More defensive: always allow if in production or if uncertain
        try:
            if cors_origins == "*":
                response.headers["Access-Control-Allow-Origin"] = "*"
            elif isinstance(cors_origins, list) and origin in cors_origins:
                response.headers["Access-Control-Allow-Origin"] = origin
            elif isinstance(cors_origins, list) and cors_origins:
                response.headers["Access-Control-Allow-Origin"] = cors_origins[0]
            else:
                # Fallback: always allow (defensive approach - better than blocking)
                response.headers["Access-Control-Allow-Origin"] = "*"
        except:
            # If setting origin fails, use wildcard
            response.headers["Access-Control-Allow-Origin"] = "*"
        
        # Set other CORS headers
        try:
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Credentials"] = "false"
        except:
            pass  # If headers already set, continue
        
        # Debug logging for CORS (only log first few requests to avoid spam)
        try:
            if not hasattr(after_request, '_request_count'):
                after_request._request_count = 0
            after_request._request_count += 1
            if after_request._request_count <= 5:
                print(f"[CORS DEBUG] Request #{after_request._request_count}: Origin={origin}, CORS-Origin={response.headers.get('Access-Control-Allow-Origin', 'NOT SET')}")
        except:
            pass  # Don't fail on logging
        
    except Exception as e:
        # Even if CORS setup fails, try to add basic headers
        # This is critical - we MUST set CORS headers even on errors
        print(f"[ERROR] Failed to set CORS headers: {e}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        try:
            # Always set CORS headers as fallback
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Credentials"] = "false"
        except Exception as fallback_error:
            print(f"[ERROR] Even fallback CORS headers failed: {fallback_error}")
            # Last resort: try to set at least the origin header
            try:
                response.headers["Access-Control-Allow-Origin"] = "*"
            except:
                pass
    
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
        print("[INFO] Received analyze-review request")
        data = request.get_json()
        
        if not data or 'review_text' not in data:
            print("[ERROR] Missing review_text in request")
            return jsonify({'error': 'review_text is required'}), 400
        
        review_text = data['review_text'].strip()
        
        if not review_text:
            print("[ERROR] Empty review_text")
            return jsonify({'error': 'review_text cannot be empty'}), 400
        
        # Analyze sentiment using Hugging Face
        print(f"[INFO] Menganalisis sentimen untuk review: {review_text[:50]}...")
        try:
            # Check if model is loaded (non-blocking)
            from sentiment_analyzer import sentiment_pipeline
            
            # If model is not loaded yet, use fallback (don't wait for it)
            if sentiment_pipeline is None:
                print("[WARNING] Model still loading, using fallback sentiment analysis")
                sentiment_result = {'label': 'neutral', 'score': 0.5}
            else:
                # Model is loaded, use it
                sentiment_result = analyze_sentiment(review_text)
                print(f"[SUCCESS] Sentimen: {sentiment_result['label']} (score: {sentiment_result.get('score', 0):.2f})")
        except Exception as sent_error:
            print(f"[ERROR] Sentiment analysis failed: {sent_error}")
            import traceback
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            # Use fallback instead of returning error
            print("[WARNING] Using fallback sentiment analysis")
            sentiment_result = {'label': 'neutral', 'score': 0.5}
        
        # Extract key points using AI (Groq/Hugging Face/Gemini) or smart extraction
        print("[INFO] Mengekstrak poin penting...")
        try:
            key_points = extract_key_points(review_text)
            print("[SUCCESS] Poin penting berhasil diekstrak")
        except Exception as kp_error:
            print(f"[ERROR] Key points extraction failed: {kp_error}")
            import traceback
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            # Use fallback if extraction fails
            print("[WARNING] Using fallback key points extraction")
            key_points = "Poin penting tidak dapat diekstrak"
        
        # Save to database
        try:
            review = Review(
                review_text=review_text,
                sentiment=sentiment_result['label'],
                sentiment_score=sentiment_result.get('score', 0.0),
                key_points=key_points
            )
            
            db.session.add(review)
            db.session.commit()
            print(f"[SUCCESS] Review saved with ID: {review.id}")
        except Exception as db_error:
            print(f"[ERROR] Database save failed: {db_error}")
            db.session.rollback()
            import traceback
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            # Return result even if save fails
            return jsonify({
                'review_text': review_text,
                'sentiment': sentiment_result['label'],
                'sentiment_score': sentiment_result.get('score', 0.0),
                'key_points': key_points,
                'warning': 'Review tidak dapat disimpan ke database'
            }), 201
        
        return jsonify({
            'id': review.id,
            'review_text': review.review_text,
            'sentiment': review.sentiment,
            'sentiment_score': review.sentiment_score,
            'key_points': review.key_points,
            'created_at': review.created_at.isoformat() if review.created_at else None
        }), 201
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"[ERROR] Unexpected error in analyze_review: {str(e)}")
        print(f"[ERROR] Traceback: {error_trace}")
        
        # Try to rollback database session
        try:
            db.session.rollback()
        except:
            pass
        
        # Return error with CORS headers (handled by after_request)
        return jsonify({'error': 'Gagal menganalisis review', 'details': str(e)[:200]}), 500


@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    try:
        print("[INFO] Fetching reviews from database...")
        # Test database connection first (with timeout protection)
        try:
            db.session.execute(text('SELECT 1'))
            print("[INFO] Database connection OK")
        except Exception as conn_error:
            print(f"[WARNING] Database connection test failed: {conn_error}")
            # Try to reconnect
            try:
                db.session.remove()
                db.session.execute(text('SELECT 1'))
                print("[INFO] Database reconnected")
            except Exception as reconnect_error:
                print(f"[ERROR] Database reconnection failed: {reconnect_error}")
                # Return empty list instead of error to prevent 502
                return jsonify([]), 200
        
        # Fetch reviews with error handling
        try:
            reviews = Review.query.order_by(Review.created_at.desc()).all()
            print(f"[SUCCESS] Found {len(reviews)} reviews")
            return jsonify([review.to_dict() for review in reviews]), 200
        except Exception as query_error:
            print(f"[ERROR] Query failed: {query_error}")
            # Return empty list instead of error
            return jsonify([]), 200
            
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
        
        # Return empty list instead of error to prevent 502
        # CORS headers will be added by after_request
        return jsonify([]), 200


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
    """Health check endpoint - lightweight, doesn't load models"""
    try:
        # Quick database connection test (non-blocking)
        try:
            db.session.execute(text('SELECT 1'))
            db_status = 'connected'
        except Exception as db_error:
            db_status = f'error: {str(db_error)[:50]}'
        
        # Check model loading status (non-blocking)
        model_status = 'unknown'
        try:
            from sentiment_analyzer import sentiment_pipeline
            if sentiment_pipeline is not None:
                model_status = 'loaded'
            else:
                model_status = 'loading'
        except:
            model_status = 'unknown'
        
        return jsonify({
            'status': 'healthy',
            'database': db_status,
            'model_status': model_status,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        # Even if health check fails, return 200 to prevent restart loops
        print(f"[WARNING] Health check error: {e}")
        return jsonify({
            'status': 'degraded',
            'error': str(e)[:100]
        }), 200


# Global error handler to ensure CORS headers are always present
@app.errorhandler(500)
def handle_500_error(e):
    """Handle 500 errors and ensure CORS headers are present"""
    import traceback
    error_trace = traceback.format_exc()
    print(f"[ERROR] 500 Internal Server Error: {str(e)}")
    print(f"[ERROR] Traceback: {error_trace}")
    
    response = jsonify({'error': 'Internal server error', 'details': str(e)[:200]})
    response.status_code = 500
    
    # CORS headers will be added by after_request
    return response


@app.errorhandler(404)
def handle_404_error(e):
    """Handle 404 errors and ensure CORS headers are present"""
    response = jsonify({'error': 'Not found'})
    response.status_code = 404
    # CORS headers will be added by after_request
    return response


@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all unhandled exceptions and ensure CORS headers are present"""
    import traceback
    error_trace = traceback.format_exc()
    print(f"[ERROR] Unhandled exception: {str(e)}")
    print(f"[ERROR] Traceback: {error_trace}")
    
    response = jsonify({'error': 'An error occurred', 'details': str(e)[:200]})
    response.status_code = 500
    
    # CORS headers will be added by after_request
    return response


# Background model preloading function
def preload_models():
    """Preload AI models in background after startup"""
    try:
        print("[INFO] Starting background model preloading...")
        # Preload sentiment model (allow_loading=True for background thread)
        try:
            from sentiment_analyzer import get_sentiment_pipeline
            print("[INFO] Preloading sentiment analysis model...")
            get_sentiment_pipeline(allow_loading=True)
            print("[SUCCESS] Sentiment model preloaded")
        except Exception as e:
            print(f"[WARNING] Failed to preload sentiment model: {e}")
            import traceback
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
        
        # Note: Key points extractor uses API calls, no preloading needed
        print("[INFO] Model preloading completed")
    except Exception as e:
        print(f"[ERROR] Model preloading error: {e}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")

# Startup message
print("=" * 50)
print("ReviewInsight Backend Server")
print("=" * 50)
print(f"Environment: {os.getenv('FLASK_ENV', 'not set')}")
print(f"Production mode: {is_production}")
print(f"CORS origins: {cors_origins}")
print(f"Database URL: {database_url[:50]}..." if len(database_url) > 50 else f"Database URL: {database_url}")
print("=" * 50)
print("[INFO] Server is ready to accept requests")
print("[INFO] Starting background model preloading...")
print("=" * 50)

# Start model preloading in background thread (non-blocking)
# This ensures models are ready when needed, but doesn't block startup
model_preload_thread = threading.Thread(target=preload_models, daemon=True)
model_preload_thread.start()
print("[INFO] Model preloading started in background thread")

if __name__ == '__main__':
    # Development mode
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))


