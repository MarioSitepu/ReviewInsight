# Product Review Analyzer

Aplikasi web full-stack yang menganalisis review produk dengan mengekstrak sentiment (positif/negatif/netral) menggunakan Hugging Face dan key points menggunakan AI (Google Gemini atau Groq). Hasil disimpan dalam database PostgreSQL dan ditampilkan di frontend React yang modern.

## Fitur

- 📝 **Input Review**: Pengguna dapat memasukkan review produk melalui form teks
- 🎯 **Analisis Sentiment**: Secara otomatis menganalisis sentiment (positif/negatif/netral) menggunakan model transformer Hugging Face
- 💡 **Ekstraksi Key Points**: Mengekstrak poin-poin penting dari review menggunakan AI (Google Gemini atau Groq)
- 💾 **Penyimpanan Database**: Menyimpan semua hasil analisis ke database PostgreSQL
- 📊 **Tampilan Hasil**: UI React yang indah menampilkan hasil analisis dan riwayat review
- ⚡ **Penanganan Error**: Penanganan error yang komprehensif dan loading states
- 🌓 **Dark/Light Mode**: Dukungan mode terang dan gelap untuk kenyamanan pengguna
- 📱 **Responsive Design**: Tampilan yang responsif untuk desktop dan mobile

## Screenshots

### Tampilan Utama

![Tampilan Home](ScreenshootReviewAnalyzer/tampilan-home.png)
**Tampilan Home** - Halaman utama aplikasi dengan form input review

![Tampilan Desktop Light Mode](ScreenshootReviewAnalyzer/tampilan-desktop-lightmode.png)
**Tampilan Desktop Light Mode** - Tampilan aplikasi pada desktop dengan mode terang

![Tampilan Desktop Dark Mode](ScreenshootReviewAnalyzer/tampilan-desktop-dark-mode.png)
**Tampilan Desktop Dark Mode** - Tampilan aplikasi pada desktop dengan mode gelap

![Tampilan Mobile](ScreenshootReviewAnalyzer/tampilan-hp.png)
**Tampilan Mobile** - Tampilan aplikasi yang responsif pada perangkat mobile

### Fitur Aplikasi

![Box Menulis Review](ScreenshootReviewAnalyzer/box-menulis-review.png)
**Box Menulis Review** - Form untuk menulis dan mengirim review produk

![Box Hasil Review](ScreenshootReviewAnalyzer/box-hasil-review.png)
**Box Hasil Review** - Tampilan hasil analisis review yang menampilkan sentiment dan key points

![Review Terbaru](ScreenshootReviewAnalyzer/review-terbaru.png)
**Review Terbaru** - Daftar review terbaru yang telah dianalisis

![History Review](ScreenshootReviewAnalyzer/history-review.png)
**History Review** - Riwayat semua review yang telah dianalisis sebelumnya

> **Catatan**: Link website yang tersedia hanya untuk tampilan front-end saja. Backend API harus dijalankan secara terpisah untuk fungsi analisis review berjalan dengan baik.

## Tech Stack

### Backend
- **Flask**: Framework web Python
- **SQLAlchemy**: ORM untuk operasi database
- **PostgreSQL**: Database relasional
- **Hugging Face Transformers**: Analisis sentiment
- **Google Gemini API** atau **Groq API**: Ekstraksi key points (dapat dipilih)

### Frontend
- **React**: Framework UI
- **Vite**: Build tool dan development server
- **Axios**: HTTP client
- **Tailwind CSS**: Framework CSS utility-first
- **CSS3**: Styling modern dengan gradients dan animasi

## Struktur Project

```
TugasPemWeb3/
├── backend/
│   ├── app.py                 # Aplikasi Flask utama
│   ├── sentiment_analyzer.py  # Analisis sentiment menggunakan Hugging Face
│   ├── key_points_extractor.py # Ekstraksi key points menggunakan Gemini/Groq
│   ├── requirements.txt       # Dependencies Python
│   ├── .env.example          # Template environment variables
│   └── Dockerfile            # Konfigurasi Docker untuk backend
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Komponen React utama
│   │   ├── main.jsx          # Entry point React
│   │   ├── index.css         # Global styles
│   │   └── components/       # Komponen-komponen React
│   ├── public/
│   │   └── index.html        # HTML template
│   ├── package.json          # Dependencies Node.js
│   └── Dockerfile            # Konfigurasi Docker untuk frontend
├── ScreenshootReviewAnalyzer/ # Screenshot aplikasi
├── render.yaml               # Konfigurasi deployment Render
├── docker-compose.yml        # Konfigurasi Docker Compose
└── README.md                 # File ini
```

## Persyaratan

Sebelum memulai, pastikan Anda telah menginstall:

- **Python 3.8+**
- **Node.js 14+** dan npm
- **Database**: 
  - **Direkomendasikan**: Neon (Serverless PostgreSQL) - Gratis dan mudah digunakan
  - **Alternatif**: PostgreSQL 12+ (instalasi lokal)
- **API Key AI** (pilih salah satu):
  - **Google Gemini API Key** (Dapatkan dari [Google AI Studio](https://makersuite.google.com/app/apikey))
  - **Groq API Key** (Dapatkan dari [Groq Console](https://console.groq.com/))

## Instruksi Setup

### 1. Setup Database

**Opsi A: Neon (Serverless PostgreSQL) ⭐ Direkomendasikan**

Neon adalah serverless PostgreSQL yang gratis dan mudah digunakan:

1. **Daftar di Neon**: https://neon.tech
2. **Buat project baru** di dashboard
3. **Salin connection string** dari Neon dashboard
4. **Tempel ke file `.env`**:
   ```env
   DATABASE_URL=postgresql://user:pass@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
   ```

**📖 Panduan lengkap**: Daftar di https://neon.tech dan ikuti panduan setup database di dashboard

**Opsi B: PostgreSQL Lokal**

Jika ingin menggunakan PostgreSQL lokal:

```bash
# Windows
create_database.bat

# Linux/Mac
chmod +x create_database.sh
./create_database.sh
```

Atau manual:
```sql
psql -U postgres
CREATE DATABASE review_analyzer;
\q
```

### 2. Setup Backend

1. Masuk ke direktori backend:

```bash
cd backend
```

2. Buat virtual environment (disarankan):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies Python:

```bash
pip install -r requirements.txt
```

4. Buat file `.env` di direktori backend:

```bash
# Windows
copy env_example.txt .env

# Linux/Mac
cp env_example.txt .env
```

5. Edit file `.env` dengan konfigurasi Anda:

```env
# Database - Gunakan Neon connection string (direkomendasikan)
DATABASE_URL=postgresql://user:pass@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require

# API Keys AI - Pilih salah satu atau keduanya
# Untuk menggunakan Gemini, isi GEMINI_API_KEY
GEMINI_API_KEY=your_gemini_api_key_here

# Untuk menggunakan Groq, isi GROQ_API_KEY
GROQ_API_KEY=your_groq_api_key_here

# API Key untuk Hugging Face (opsional, untuk akses model premium)
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

**Catatan Penting**: 
- Anda dapat menggunakan **Gemini** atau **Groq** untuk ekstraksi key points
- Jika kedua API key diisi, aplikasi akan menggunakan Gemini sebagai default
- Untuk Neon: Dapatkan connection string dari https://console.neon.tech
- Untuk PostgreSQL lokal: `postgresql://username:password@localhost:5432/review_analyzer`

**Cara Mendapatkan API Key:**

- **Google Gemini API Key**:
  1. Kunjungi https://makersuite.google.com/app/apikey
  2. Login dengan akun Google
  3. Klik "Create API Key"
  4. Salin API key yang dihasilkan

- **Groq API Key**:
  1. Kunjungi https://console.groq.com/
  2. Buat akun atau login
  3. Buka bagian "API Keys"
  4. Klik "Create API Key"
  5. Salin API key yang dihasilkan

### 3. Setup Frontend

1. Masuk ke direktori frontend:

```bash
cd frontend
```

2. Install dependencies Node.js:

```bash
npm install
```

3. Buat file `.env` di direktori frontend (opsional):

```env
VITE_API_URL=http://localhost:5000/api
```

Jika tidak diatur, default ke `http://localhost:5000/api`.

## Menjalankan Aplikasi

### Menjalankan Backend Server

1. Aktifkan virtual environment (jika belum diaktifkan):

```bash
cd backend
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. Jalankan aplikasi Flask:

```bash
python app.py
```

Server backend akan berjalan di `http://localhost:5000`

### Menjalankan Frontend Development Server

1. Di terminal baru, masuk ke direktori frontend:

```bash
cd frontend
```

2. Jalankan development server React:

```bash
npm run dev
```

Frontend akan otomatis terbuka di browser di `http://localhost:5173` (atau port yang tersedia)

## API Endpoints

### POST /api/analyze-review

Menganalisis review produk baru.

**Request Body:**
```json
{
  "review_text": "Produk ini luar biasa! Kualitas bagus dan pengiriman cepat."
}
```

**Response:**
```json
{
  "id": 1,
  "review_text": "Produk ini luar biasa! Kualitas bagus dan pengiriman cepat.",
  "sentiment": "positive",
  "sentiment_score": 0.98,
  "key_points": "• Kualitas produk sangat baik\n• Pengiriman cepat\n• Pengalaman keseluruhan positif",
  "created_at": "2024-01-15T10:30:00"
}
```

### GET /api/reviews

Mendapatkan semua review yang telah dianalisis.

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

Endpoint health check.

**Response:**
```json
{
  "status": "healthy"
}
```

## Cara Penggunaan

1. **Menganalisis Review**: 
   - Masukkan review produk Anda di area teks
   - Klik tombol "Analyze Review"
   - Tunggu hingga analisis selesai (mungkin memakan waktu beberapa detik)

2. **Melihat Hasil**:
   - Hasil analisis sentiment (positif/negatif/netral) dengan confidence score
   - Key points yang diekstrak dari review

3. **Melihat Semua Review**:
   - Scroll ke bawah untuk melihat semua review yang telah dianalisis sebelumnya
   - Klik "Refresh" untuk memuat ulang daftar
   - Buka "Key Points" untuk melihat analisis detail

## Penanganan Error

Aplikasi ini mencakup penanganan error yang komprehensif:

- **Review Text Kosong**: Menampilkan error jika review text kosong
- **Error API**: Menampilkan pesan error yang user-friendly
- **Error Database**: Menangani masalah koneksi database dengan baik
- **Loading States**: Menampilkan indikator loading selama API call

## Troubleshooting

### Masalah Backend

1. **Error Koneksi Database**:
   - Verifikasi PostgreSQL sedang berjalan
   - Periksa DATABASE_URL di file `.env`
   - Pastikan database sudah dibuat

2. **Error API Gemini/Groq**:
   - Verifikasi GEMINI_API_KEY atau GROQ_API_KEY sudah diatur dengan benar di `.env`
   - Periksa API key valid dan memiliki quota
   - Pastikan koneksi internet tersedia

3. **Analisis Sentiment Lambat**:
   - Run pertama mungkin memakan waktu untuk download model
   - Run selanjutnya akan lebih cepat

4. **AI Tidak Berfungsi**:
   - Pastikan minimal satu API key (GEMINI_API_KEY atau GROQ_API_KEY) sudah diisi
   - Periksa log backend untuk melihat error detail
   - Verifikasi API key memiliki quota yang tersedia

### Masalah Frontend

1. **Tidak Bisa Terhubung ke Backend**:
   - Verifikasi server backend berjalan di port 5000
   - Periksa VITE_API_URL di frontend `.env`
   - Pastikan tidak ada firewall yang memblokir koneksi

2. **Error CORS**:
   - Backend sudah memiliki CORS enabled untuk localhost
   - Periksa flask-cors sudah terinstall

## Catatan Pengembangan

- Model analisis sentiment (`cardiffnlp/twitter-roberta-base-sentiment-latest`) akan di-download pada penggunaan pertama (~500MB)
- API Gemini/Groq memerlukan koneksi internet dan API key yang valid
- Tabel database dibuat otomatis pada run pertama
- Aplikasi mendukung penggunaan Gemini atau Groq untuk ekstraksi key points
- Jika kedua API key tersedia, aplikasi akan menggunakan Gemini sebagai default

## Deployment

### Opsi 1: Render dengan Docker ⭐ Direkomendasikan

**Terbaik untuk:** Deployment full-stack, dukungan Docker, auto-deploy, HTTPS gratis

1. **Deploy Backend & Frontend ke Render:**
   - Setup menggunakan `render.yaml` yang tersedia di repository
   - Pastikan semua environment variables sudah diatur di Render dashboard

**Keuntungan:**
- ✅ Free tier tersedia
- ✅ Dukungan Docker
- ✅ Auto-deploy dari GitHub
- ✅ HTTPS otomatis
- ✅ Custom domain gratis
- ✅ Setup mudah dengan render.yaml

### Opsi 2: Vercel (Frontend) + PythonAnywhere (Backend)

**Terbaik untuk:** Hosting gratis, setup mudah, bagus untuk project personal

1. **Deploy Backend ke PythonAnywhere:**
   - Setup backend Flask di PythonAnywhere dengan konfigurasi WSGI
   - Atur environment variables di PythonAnywhere dashboard

2. **Deploy Frontend ke Vercel:**
   - Deploy frontend React ke Vercel dengan konfigurasi environment variables
   - Pastikan VITE_API_URL mengarah ke URL backend yang sudah di-deploy

### Opsi 3: Docker Compose (Full Stack)

1. **Konfigurasi environment:**
   ```bash
   cd backend
   cp env_example.txt .env
   # Edit .env dengan API keys dan database password
   ```

2. **Deploy:**
   ```bash
   # Linux/Mac
   ./deploy.sh
   
   # Windows
   deploy.bat
   ```

3. **Akses:**
   - Frontend: http://localhost:80
   - Backend API: http://localhost:5000

### Opsi 4: Platform Cloud Lainnya

Untuk deployment ke platform cloud lainnya:
- Docker deployment menggunakan Dockerfile yang tersedia
- Heroku deployment dengan konfigurasi Procfile
- AWS/Azure/GCP deployment dengan konfigurasi sesuai platform

**Catatan Deployment:**
- Pastikan semua environment variables sudah diatur di platform deployment
- Untuk production, gunakan database yang reliable (Neon direkomendasikan)
- Pastikan API keys (Gemini atau Groq) sudah diatur dengan benar
- Aktifkan HTTPS untuk keamanan data

## Konfigurasi AI (Gemini atau Groq)

Aplikasi ini mendukung penggunaan dua provider AI untuk ekstraksi key points:

### Menggunakan Google Gemini

1. Dapatkan API key dari [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Tambahkan ke file `.env`:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### Menggunakan Groq

1. Dapatkan API key dari [Groq Console](https://console.groq.com/)
2. Tambahkan ke file `.env`:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Prioritas Penggunaan

- Jika **kedua API key** tersedia, aplikasi akan menggunakan **Gemini** sebagai default
- Jika hanya **satu API key** yang tersedia, aplikasi akan menggunakan yang tersedia
- Pastikan minimal **satu API key** sudah diatur untuk ekstraksi key points berfungsi

**Perbandingan:**

| Fitur | Google Gemini | Groq |
|-------|---------------|------|
| Kecepatan | Sedang | Sangat Cepat |
| Kualitas | Sangat Baik | Baik |
| Gratis | Ya (dengan quota) | Ya (dengan quota) |
| Model | Gemini Pro | Llama 3 |

## Lisensi

Project ini dibuat untuk keperluan edukasi.

## Author

Dibuat untuk Tugas PemWeb 3
