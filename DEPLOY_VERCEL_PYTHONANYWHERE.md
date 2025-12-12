# Deployment Guide: Vercel (Frontend) + PythonAnywhere (Backend)

Panduan lengkap untuk deploy ReviewInsight dengan frontend di Vercel dan backend di PythonAnywhere.

## Prerequisites

- Akun Vercel (gratis): https://vercel.com
- Akun PythonAnywhere (gratis): https://www.pythonanywhere.com
- GitHub repository (untuk Vercel auto-deploy)

## Part 1: Deploy Backend ke PythonAnywhere

### 1.1 Persiapan

1. **Daftar di PythonAnywhere**
   - Kunjungi https://www.pythonanywhere.com
   - Buat akun gratis (Beginner plan cukup untuk testing)

2. **Siapkan Database**
   - **Recommended**: Gunakan Neon (Serverless PostgreSQL) - Gratis & mudah
     - Setup: https://neon.tech (lihat [SETUP_NEON_DATABASE.md](SETUP_NEON_DATABASE.md))
     - Dapatkan connection string dari Neon dashboard
   - **Alternative**: PythonAnywhere MySQL (gratis) atau PostgreSQL eksternal

### 1.2 Upload Files ke PythonAnywhere

**Opsi A: Via Web Interface**
1. Login ke PythonAnywhere
2. Buka **Files** tab
3. Upload semua file dari folder `backend/` ke home directory
4. Pastikan struktur seperti ini:
   ```
   /home/yourusername/
   ├── app.py
   ├── sentiment_analyzer.py
   ├── key_points_extractor.py
   ├── requirements.txt
   ├── wsgi.py
   └── .env
   ```

**Opsi B: Via Git (Recommended)**
```bash
# Di PythonAnywhere Bash console
cd ~
git clone https://github.com/yourusername/your-repo.git
cd your-repo/backend
```

### 1.3 Setup Environment

1. **Buat file .env:**
   ```bash
   nano .env
   ```

2. **Isi dengan konfigurasi:**
   ```env
   # Database - Recommended: Neon (see SETUP_NEON_DATABASE.md)
   DATABASE_URL=postgresql://username:password@ep-xxx-xxx-pooler.region.aws.neon.tech/dbname?sslmode=require
   
   # AI API Keys
   GEMINI_API_KEY=your_gemini_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   HUGGINGFACE_API_KEY=your_huggingface_api_key_here
   
   # Settings
   FLASK_ENV=production
   USE_GEMINI=true
   USE_GROQ_KEY_POINTS=true
   USE_HUGGINGFACE_KEY_POINTS=true
   ```
   
   **Note**: Untuk Neon setup, lihat [SETUP_NEON_DATABASE.md](SETUP_NEON_DATABASE.md)

### 1.4 Install Dependencies

Di PythonAnywhere Bash console:

```bash
cd ~/your-repo/backend  # atau direktori backend Anda

# Install dependencies
pip3.10 install --user -r requirements.txt

# Jika ada error dengan torch (terlalu besar), install tanpa torch dulu:
pip3.10 install --user flask flask-cors flask-sqlalchemy psycopg2-binary transformers google-generativeai python-dotenv werkzeug requests gunicorn

# Install torch separately jika diperlukan (opsional, untuk sentiment analysis)
pip3.10 install --user torch --index-url https://download.pytorch.org/whl/cpu
```

### 1.5 Setup Database

**Recommended: Neon (Serverless PostgreSQL)**

1. **Daftar di Neon**: https://neon.tech
2. **Buat project baru** di Neon dashboard
3. **Copy connection string** (gunakan pooled connection untuk production)
4. **Paste ke .env file**:
   ```env
   DATABASE_URL=postgresql://user:pass@ep-xxx-xxx-pooler.region.aws.neon.tech/dbname?sslmode=require
   ```
5. **Setup lengkap**: Lihat [SETUP_NEON_DATABASE.md](SETUP_NEON_DATABASE.md)

**Alternative: MySQL (PythonAnywhere default)**

1. Buka **Databases** tab di PythonAnywhere
2. Buat database baru
3. Update `requirements.txt` untuk MySQL:
   ```
   # Ganti psycopg2-binary dengan:
   pymysql==1.1.0
   ```
4. Update DATABASE_URL di .env:
   ```env
   DATABASE_URL=mysql+pymysql://username:password@hostname/database_name
   ```

### 1.6 Configure Web App

1. Buka **Web** tab di PythonAnywhere
2. Klik **Add a new web app**
3. Pilih **Flask**
4. Pilih Python version (3.10 recommended)
5. Set **Source code** ke direktori backend Anda
6. Set **Working directory** ke direktori backend Anda

7. **Edit WSGI configuration file:**
   - Klik link WSGI configuration file
   - Ganti isinya dengan:
   ```python
   import sys
   path = '/home/yourusername/your-repo/backend'  # Ganti dengan path Anda
   if path not in sys.path:
       sys.path.insert(0, path)
   
   from wsgi import application
   ```

8. **Reload web app**

### 1.7 Update CORS untuk Vercel

Edit `app.py` untuk allow Vercel domain:

```python
from flask_cors import CORS

# Allow Vercel domains
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://your-app.vercel.app",
            "https://*.vercel.app",  # Allow all Vercel preview deployments
            "http://localhost:5173"  # For local testing
        ],
        "methods": ["GET", "POST", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### 1.8 Test Backend

1. Buka URL web app Anda: `https://yourusername.pythonanywhere.com`
2. Test health endpoint: `https://yourusername.pythonanywhere.com/api/health`
3. Seharusnya return: `{"status": "healthy"}`

## Part 2: Deploy Frontend ke Vercel

### 2.1 Persiapan

1. **Push code ke GitHub** (jika belum)
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Install Vercel CLI** (opsional, untuk local testing):
   ```bash
   npm i -g vercel
   ```

### 2.2 Deploy via Vercel Dashboard

1. **Login ke Vercel**
   - Kunjungi https://vercel.com
   - Login dengan GitHub

2. **Import Project**
   - Klik **Add New** → **Project**
   - Pilih repository GitHub Anda
   - Vercel akan auto-detect Vite config

3. **Configure Project**
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build` (atau `vite build`)
   - **Output Directory**: `dist`

4. **Environment Variables**
   Tambahkan:
   ```
   VITE_API_URL=https://yourusername.pythonanywhere.com/api
   ```
   **Penting**: Pastikan menggunakan `VITE_` prefix untuk Vite env vars!

5. **Deploy**
   - Klik **Deploy**
   - Tunggu build selesai

### 2.3 Deploy via CLI (Alternative)

```bash
cd frontend
vercel login
vercel

# Set environment variable
vercel env add VITE_API_URL
# Enter: https://yourusername.pythonanywhere.com/api

# Deploy to production
vercel --prod
```

### 2.4 Update Frontend Code

Pastikan `App.jsx` menggunakan environment variable dengan benar:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.DEV ? '/api' : 'https://yourusername.pythonanywhere.com/api');
```

## Part 3: Testing & Verification

### 3.1 Test Frontend
1. Buka URL Vercel: `https://your-app.vercel.app`
2. Test analisis review
3. Check browser console untuk errors

### 3.2 Test Backend
1. Test API endpoints:
   ```bash
   curl https://yourusername.pythonanywhere.com/api/health
   curl -X POST https://yourusername.pythonanywhere.com/api/analyze-review \
     -H "Content-Type: application/json" \
     -d '{"review_text": "Produk bagus!"}'
   ```

### 3.3 Common Issues

**CORS Error:**
- Pastikan backend CORS allow Vercel domain
- Check browser console untuk exact error

**API Connection Error:**
- Verify `VITE_API_URL` di Vercel environment variables
- Pastikan backend URL benar dan accessible

**Database Error:**
- Check DATABASE_URL di PythonAnywhere .env
- Verify database connection di PythonAnywhere console

## Part 4: Production Optimizations

### 4.1 PythonAnywhere

1. **Upgrade ke Hacker plan** (jika perlu) untuk:
   - Custom domains
   - HTTPS
   - More resources

2. **Setup Custom Domain** (Hacker plan):
   - Add domain di Web tab
   - Setup SSL certificate

3. **Monitor Logs:**
   - Check error logs di Web tab
   - Monitor server logs

### 4.2 Vercel

1. **Custom Domain:**
   - Add domain di Project Settings
   - Update DNS records

2. **Environment Variables per Environment:**
   - Production: `VITE_API_URL=https://yourusername.pythonanywhere.com/api`
   - Preview: Bisa berbeda untuk testing

3. **Analytics:**
   - Enable Vercel Analytics untuk monitoring

## Troubleshooting

### Backend Issues

**Import Error:**
```bash
# Check Python path
python3.10 -c "import sys; print(sys.path)"
# Add path if needed in wsgi.py
```

**Module Not Found:**
```bash
# Install missing packages
pip3.10 install --user package_name
```

**Database Connection:**
- Verify DATABASE_URL format
- Test connection di PythonAnywhere console

### Frontend Issues

**Build Fails:**
- Check build logs di Vercel
- Verify all dependencies di package.json

**API Calls Fail:**
- Check CORS settings
- Verify VITE_API_URL environment variable
- Check network tab di browser DevTools

## Cost Estimate

- **Vercel**: Free tier cukup untuk personal projects
- **PythonAnywhere**: Free tier (Beginner) cukup untuk testing
  - Upgrade ke Hacker ($5/month) untuk custom domain & HTTPS

## Next Steps

1. ✅ Backend deployed di PythonAnywhere
2. ✅ Frontend deployed di Vercel
3. ✅ Test semua fitur
4. ✅ Setup custom domains (optional)
5. ✅ Monitor logs dan errors
6. ✅ Setup backups untuk database

## Support

- PythonAnywhere Docs: https://help.pythonanywhere.com
- Vercel Docs: https://vercel.com/docs
- Project Issues: Check GitHub issues

