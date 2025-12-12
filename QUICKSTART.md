# Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:

- ✅ Python 3.8+ installed (`python --version`)
- ✅ Node.js 14+ installed (`node --version`)
- ✅ PostgreSQL installed and running
- ✅ Google Gemini API key (Get from [Google AI Studio](https://makersuite.google.com/app/apikey))

## Step-by-Step Setup

### 1. Database Setup (5 minutes)

**Option A: Using Python Script (Recommended - Works on all platforms)**

```bash
# Windows - Double click or run:
create_database.bat

# Linux/Mac - Run:
chmod +x create_database.sh
./create_database.sh
```

**Option B: Using psql command**

```bash
# Connect to PostgreSQL
psql -U postgres

# Then run:
CREATE DATABASE review_analyzer;
\q
```

**Option C: Using createdb command (if available in PATH)**

```bash
createdb review_analyzer
```

**Note:** If `createdb` command is not found, use Option A or B above.

**⚠️ Having issues?** See `SETUP_DATABASE.md` for complete troubleshooting guide including:
- How to install PostgreSQL
- How to start PostgreSQL service
- How to fix connection errors
- All common problems and solutions

### 2. Backend Setup (10 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
copy env_example.txt .env  # Windows
# OR
cp env_example.txt .env    # Linux/Mac

# Edit .env file with your credentials:
# DATABASE_URL=postgresql://username:password@localhost:5432/review_analyzer
# GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Frontend Setup (5 minutes)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Linux/Mac

python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

Browser should automatically open at `http://localhost:3000`

## Testing the Application

1. **Enter a Review**: Type a product review in the text area
   Example: "This product is amazing! Great quality and fast shipping. Highly recommended!"

2. **Analyze**: Click "Analyze Review" button

3. **View Results**: 
   - See sentiment (positive/negative/neutral) with confidence score
   - See extracted key points

4. **View History**: Scroll down to see all previous reviews

## Troubleshooting

### Backend won't start

- **Check PostgreSQL**: Make sure PostgreSQL is running
  ```bash
  # Windows - check services
  # Linux/Mac
  sudo systemctl status postgresql
  ```

- **Check Database URL**: Verify `.env` file has correct database credentials

- **Check Port**: Make sure port 5000 is not in use

### Frontend can't connect to backend

- **Check Backend**: Make sure backend is running on port 5000
- **Check CORS**: Backend has CORS enabled, should work automatically
- **Check API URL**: Verify `REACT_APP_API_URL` in frontend `.env` if you created one

### Sentiment Analysis takes too long

- First run downloads the model (~500MB), be patient
- Subsequent runs are much faster

### Gemini API errors

- Verify API key is correct in backend `.env`
- Check internet connection
- Verify API key has quota remaining

## Next Steps

- Try different types of reviews (positive, negative, neutral)
- Check the database to see stored reviews:
  ```bash
  psql -U postgres -d review_analyzer
  SELECT * FROM review;
  ```

## Need Help?

Check the main README.md for detailed documentation and API reference.

