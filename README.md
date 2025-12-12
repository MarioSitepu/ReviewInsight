# Product Review Analyzer

A full-stack web application that analyzes product reviews by extracting sentiment (positive/negative/neutral) using Hugging Face and key points using Google Gemini AI. Results are stored in a PostgreSQL database and displayed in a modern React frontend.

## Features

- 📝 **Review Input**: Users can input product reviews via a text form
- 🎯 **Sentiment Analysis**: Automatically analyzes sentiment (positive/negative/neutral) using Hugging Face's transformer models
- 💡 **Key Points Extraction**: Extracts key points from reviews using Google Gemini AI
- 💾 **Database Storage**: Saves all analysis results to PostgreSQL database
- 📊 **Results Display**: Beautiful React UI showing analysis results and review history
- ⚡ **Error Handling**: Comprehensive error handling and loading states

## Tech Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Relational database
- **Hugging Face Transformers**: Sentiment analysis
- **Google Gemini API**: Key points extraction

### Frontend
- **React**: UI framework
- **Axios**: HTTP client
- **CSS3**: Modern styling with gradients and animations

## Project Structure

```
TugasPemWeb3/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── sentiment_analyzer.py  # Sentiment analysis using Hugging Face
│   ├── key_points_extractor.py # Key points extraction using Gemini
│   ├── requirements.txt       # Python dependencies
│   └── .env.example          # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Component styles
│   │   ├── index.js          # React entry point
│   │   └── index.css         # Global styles
│   ├── public/
│   │   └── index.html        # HTML template
│   └── package.json          # Node.js dependencies
└── README.md                 # This file
```

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **Node.js 14+** and npm
- **PostgreSQL 12+**
- **Google Gemini API Key** (Get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

## Setup Instructions

### 1. Database Setup

**Option A: Using Python Script (Recommended - Works on all platforms)**

The easiest way is to use our helper script:

```bash
# Windows
create_database.bat

# Linux/Mac
chmod +x create_database.sh
./create_database.sh
```

This script will automatically:
- Check if the database exists
- Create it if it doesn't
- Handle connection errors gracefully

**Option B: Using psql**

Connect to PostgreSQL and create the database:

```sql
psql -U postgres
CREATE DATABASE review_analyzer;
\q
```

**Option C: Using createdb command (if available in PATH)**

```bash
createdb review_analyzer
```

**Note:** If `createdb` command is not found (common on Windows), use Option A or B above.

**📖 Need help with database setup?** See `SETUP_DATABASE.md` for comprehensive guide including installation, troubleshooting, and all common issues.

### 2. Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create a virtual environment (recommended):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the backend directory:

```bash
cp .env.example .env
```

5. Edit `.env` file with your configuration:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/review_analyzer
GEMINI_API_KEY=your_gemini_api_key_here
```

**Note**: Replace `username` and `password` with your PostgreSQL credentials.

### 3. Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install Node.js dependencies:

```bash
npm install
```

3. Create a `.env` file in the frontend directory (optional):

```env
REACT_APP_API_URL=http://localhost:5000/api
```

If not set, it defaults to `http://localhost:5000/api`.

## Running the Application

### Start Backend Server

1. Activate your virtual environment (if not already activated):

```bash
cd backend
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. Run the Flask application:

```bash
python app.py
```

The backend server will start on `http://localhost:5000`

### Start Frontend Development Server

1. In a new terminal, navigate to the frontend directory:

```bash
cd frontend
```

2. Start the React development server:

```bash
npm start
```

The frontend will automatically open in your browser at `http://localhost:3000`

## API Endpoints

### POST /api/analyze-review

Analyze a new product review.

**Request Body:**
```json
{
  "review_text": "This product is amazing! Great quality and fast shipping."
}
```

**Response:**
```json
{
  "id": 1,
  "review_text": "This product is amazing! Great quality and fast shipping.",
  "sentiment": "positive",
  "sentiment_score": 0.98,
  "key_points": "• Product quality is excellent\n• Shipping is fast\n• Overall positive experience",
  "created_at": "2024-01-15T10:30:00"
}
```

### GET /api/reviews

Get all analyzed reviews.

**Response:**
```json
[
  {
    "id": 1,
    "review_text": "...",
    "sentiment": "positive",
    "sentiment_score": 0.98,
    "key_points": "...",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

### GET /api/health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Usage

1. **Analyze a Review**: 
   - Enter your product review in the text area
   - Click "Analyze Review" button
   - Wait for the analysis to complete (this may take a few seconds)

2. **View Results**:
   - Sentiment analysis result (positive/negative/neutral) with confidence score
   - Extracted key points from the review

3. **View All Reviews**:
   - Scroll down to see all previously analyzed reviews
   - Click "Refresh" to reload the list
   - Expand "Key Points" to see detailed analysis

## Error Handling

The application includes comprehensive error handling:

- **Empty Review Text**: Shows error if review text is empty
- **API Errors**: Displays user-friendly error messages
- **Database Errors**: Handles database connection issues gracefully
- **Loading States**: Shows loading indicators during API calls

## Troubleshooting

### Backend Issues

1. **Database Connection Error**:
   - Verify PostgreSQL is running
   - Check DATABASE_URL in `.env` file
   - Ensure database exists

2. **Gemini API Error**:
   - Verify GEMINI_API_KEY is set correctly in `.env`
   - Check API key is valid and has quota

3. **Sentiment Analysis Slow**:
   - First run may take time to download the model
   - Subsequent runs will be faster

### Frontend Issues

1. **Cannot Connect to Backend**:
   - Verify backend server is running on port 5000
   - Check REACT_APP_API_URL in frontend `.env`

2. **CORS Errors**:
   - Backend has CORS enabled for localhost
   - Check flask-cors is installed

## Development Notes

- The sentiment analysis model (`cardiffnlp/twitter-roberta-base-sentiment-latest`) will be downloaded on first use (~500MB)
- Gemini API requires internet connection and valid API key
- Database tables are created automatically on first run

## Deployment

### Option 1: Vercel (Frontend) + PythonAnywhere (Backend) ⭐ Recommended

**Best for:** Free hosting, easy setup, great for personal projects

1. **Deploy Backend to PythonAnywhere:**
   - Follow guide: [DEPLOY_VERCEL_PYTHONANYWHERE.md](DEPLOY_VERCEL_PYTHONANYWHERE.md#part-1-deploy-backend-ke-pythonanywhere)

2. **Deploy Frontend to Vercel:**
   - Follow guide: [DEPLOY_VERCEL_PYTHONANYWHERE.md](DEPLOY_VERCEL_PYTHONANYWHERE.md#part-2-deploy-frontend-ke-vercel)

**Benefits:**
- ✅ Free tier available
- ✅ Easy setup
- ✅ Auto-deploy from GitHub (Vercel)
- ✅ Great for learning and small projects

### Option 2: Docker Compose (Full Stack)

1. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and database password
   ```

2. **Deploy:**
   ```bash
   # Linux/Mac
   ./deploy.sh
   
   # Windows
   deploy.bat
   ```

3. **Access:**
   - Frontend: http://localhost:80
   - Backend API: http://localhost:5000

### Option 3: Other Cloud Platforms

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Docker deployment
- Heroku deployment
- AWS/Azure/GCP deployment
- Production configuration
- Monitoring and troubleshooting

## License

This project is created for educational purposes.

## Author

Created for Tugas PemWeb 3

