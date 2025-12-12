# 🚀 Cara Setup AI Gratis untuk Key Points Extraction

## ⚡ Opsi 1: Groq (RECOMMENDED - Paling Cepat & Limit Besar)

**Limit:** 14,400 requests/hari (GRATIS)

### Langkah Setup:

1. **Daftar di Groq:**
   - Buka: https://console.groq.com/
   - Sign up dengan email atau Google account
   - Gratis, tidak perlu kartu kredit

2. **Buat API Key:**
   - Setelah login, klik "API Keys" di sidebar
   - Klik "Create API Key"
   - Copy API key yang diberikan

3. **Tambahkan ke `.env`:**
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   USE_GROQ_KEY_POINTS=true
   ```

4. **Restart server:**
   ```powershell
   python app.py
   ```

**Selesai!** Aplikasi akan otomatis menggunakan Groq untuk key points extraction.

---

## 🤗 Opsi 2: Hugging Face (30,000 requests/bulan)

**Limit:** 30,000 requests/bulan (GRATIS)

### Langkah Setup:

1. **Daftar di Hugging Face:**
   - Buka: https://huggingface.co/join
   - Sign up dengan email atau Google account
   - Gratis, tidak perlu kartu kredit

2. **Buat Access Token:**
   - Setelah login, buka: https://huggingface.co/settings/tokens
   - Klik "New token"
   - Pilih "Read" permission
   - Copy token yang diberikan

3. **Tambahkan ke `.env`:**
   ```env
   HUGGINGFACE_API_KEY=your_huggingface_token_here
   USE_HUGGINGFACE_KEY_POINTS=true
   ```

4. **Restart server:**
   ```powershell
   python app.py
   ```

**Selesai!** Aplikasi akan otomatis menggunakan Hugging Face untuk key points extraction.

---

## 🎯 Prioritas Penggunaan

Aplikasi akan mencoba AI provider dalam urutan ini:

1. **Groq** (jika dikonfigurasi) - 14,400/hari
2. **Hugging Face** (jika dikonfigurasi) - 30,000/bulan
3. **Gemini** (jika dikonfigurasi) - 20/hari
4. **Ekstraksi Cerdas** (selalu tersedia) - Unlimited

Jika provider pertama gagal (quota habis, error, dll), akan otomatis mencoba provider berikutnya.

---

## 💡 Rekomendasi

**Untuk Development/Testing:**
- ✅ **Gunakan Ekstraksi Cerdas** - Tidak perlu setup, unlimited
- ✅ Atau **Groq** - Limit besar, cepat

**Untuk Production:**
- ✅ **Groq** - Sangat cepat, limit besar
- ✅ **Hugging Face** - Stabil, limit cukup

---

## 🔧 Nonaktifkan Provider Tertentu

Jika tidak ingin menggunakan provider tertentu, edit `.env`:

```env
# Nonaktifkan Groq
USE_GROQ_KEY_POINTS=false

# Nonaktifkan Hugging Face
USE_HUGGINGFACE_KEY_POINTS=false

# Nonaktifkan Gemini
USE_GEMINI=false
```

---

## ✅ Test Setup

Setelah setup, test dengan menjalankan aplikasi dan analisis review. Cek terminal untuk melihat provider mana yang digunakan:

```
🔄 Menggunakan Groq API...
✅ Groq API berhasil
```

atau

```
🔄 Menggunakan Hugging Face API...
✅ Hugging Face API berhasil
```

---

## 🆘 Troubleshooting

### Error: "API key tidak valid"
- Pastikan API key sudah di-copy dengan benar (tidak ada spasi)
- Pastikan API key masih aktif (tidak expired)

### Error: "Quota habis"
- Groq: 14,400/hari - tunggu reset (24 jam)
- Hugging Face: 30,000/bulan - tunggu reset (bulanan)
- Aplikasi akan otomatis fallback ke provider lain atau ekstraksi cerdas

### Error: "Connection timeout"
- Cek koneksi internet
- Coba lagi dalam beberapa detik

---

## 📝 Contoh `.env` Lengkap

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/review_analyzer

# Groq (Recommended)
GROQ_API_KEY=gsk_your_key_here
USE_GROQ_KEY_POINTS=true

# Hugging Face (Alternative)
HUGGINGFACE_API_KEY=hf_your_token_here
USE_HUGGINGFACE_KEY_POINTS=true

# Gemini (Optional - quota kecil)
GEMINI_API_KEY=your_gemini_key_here
USE_GEMINI=false
```

---

**Selamat!** Sekarang aplikasi Anda memiliki multiple AI provider dengan fallback otomatis! 🎉

