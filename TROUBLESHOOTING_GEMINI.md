# 🔧 Troubleshooting Gemini API

## Error: "Model Gemini tidak ditemukan"

Jika Anda mendapat error ini, kemungkinan penyebabnya:

### 1. API Key Tidak Valid atau Tidak Dikonfigurasi

**Cek file `.env`:**
```env
GEMINI_API_KEY=your_actual_api_key_here
```

**Pastikan:**
- ✅ Tidak ada spasi di awal/akhir API key
- ✅ Tidak ada tanda kutip (`"` atau `'`)
- ✅ API key benar-benar dari Google AI Studio

**Cara dapatkan API key:**
1. Buka: https://makersuite.google.com/app/apikey
2. Login dengan akun Google
3. Klik "Create API Key"
4. Copy API key
5. Paste ke file `backend/.env`

### 2. API Key Tidak Memiliki Akses ke Gemini API

**Solusi:**
1. Pastikan API key dibuat di Google AI Studio (bukan Google Cloud Console)
2. Pastikan Gemini API sudah diaktifkan untuk project Anda

### 3. Quota API Habis

**Cek:**
- Buka Google AI Studio: https://makersuite.google.com/app/apikey
- Lihat quota/usage Anda
- Jika habis, tunggu reset atau upgrade plan

### 4. API Key Expired atau Disabled

**Solusi:**
1. Buat API key baru di Google AI Studio
2. Update file `.env` dengan API key baru

## ✅ Langkah Troubleshooting

### Step 1: Verifikasi API Key di File .env

```powershell
cd backend
notepad .env
```

Pastikan format benar:
```env
GEMINI_API_KEY=AIzaSy...  # Tanpa tanda kutip, tanpa spasi
```

### Step 2: Test API Key

Buat file test sederhana:

```python
# test_gemini.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key: {api_key[:10]}..." if api_key else "API Key tidak ditemukan!")

if api_key:
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        print(f"✅ API Key valid! Models tersedia: {len(list(models))}")
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name}")
    except Exception as e:
        print(f"❌ Error: {e}")
```

Jalankan:
```powershell
python test_gemini.py
```

### Step 3: Restart Server

Setelah memperbaiki `.env`:
1. Stop server (Ctrl+C)
2. Restart: `python app.py`

## 🔍 Cek Log di Terminal

Saat analisis review, lihat log di terminal backend. Anda akan melihat:

**Jika berhasil:**
```
🔍 Mencari model Gemini yang tersedia...
✅ Model yang tersedia: ['models/gemini-pro', ...]
✅ Menggunakan model: gemini-pro
```

**Jika gagal:**
```
❌ Error ekstraksi poin penting: ...
```

## 🆘 Masalah Umum

### "API key tidak dikonfigurasi"
- **Solusi:** Tambahkan `GEMINI_API_KEY` ke file `.env`

### "403 Permission denied"
- **Solusi:** API key tidak memiliki izin. Buat API key baru.

### "429 Quota exceeded"
- **Solusi:** Quota habis. Tunggu atau upgrade plan.

### "404 Model not found"
- **Solusi:** API key mungkin tidak memiliki akses. Buat API key baru.

## 📝 Contoh File .env yang Benar

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/review_analyzer
GEMINI_API_KEY=AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz1234567
```

**PENTING:** 
- Jangan ada spasi sebelum/sesudah `=`
- Jangan pakai tanda kutip
- Jangan commit file `.env` ke git (sudah ada di .gitignore)

## ✅ Next Steps

Setelah memperbaiki:
1. Restart server
2. Coba analisis review lagi
3. Cek terminal untuk log error (jika masih ada masalah)

Good luck! 🚀

