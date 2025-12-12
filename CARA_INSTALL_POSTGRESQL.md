# 🚀 Cara Install PostgreSQL - Panduan Cepat

## Error yang Anda Alami

```
psql : The term 'psql' is not recognized
```

**Ini berarti PostgreSQL BELUM TERINSTALL!**

## ✅ Solusi: Install PostgreSQL

### Langkah 1: Download PostgreSQL

1. **Buka browser** dan kunjungi:
   ```
   https://www.postgresql.org/download/windows/
   ```

2. **Klik tombol "Download the installer"** yang besar di tengah halaman

3. **Pilih versi:**
   - **PostgreSQL 16** (recommended - versi terbaru)
   - Atau PostgreSQL 15/14 (juga OK)

4. **Download installer:**
   - File biasanya: `postgresql-16-x64.exe` atau similar
   - Ukuran sekitar 200-300 MB

### Langkah 2: Install PostgreSQL

1. **Jalankan installer** yang sudah didownload
   - Double-click file `.exe`
   - Jika muncul UAC prompt, klik "Yes"

2. **Welcome Screen** → Klik "**Next**"

3. **Installation Directory** → Biarkan default, klik "**Next**"
   - Default: `C:\Program Files\PostgreSQL\16`

4. **Select Components** → Centang semua, klik "**Next**"
   - ✅ PostgreSQL Server (WAJIB)
   - ✅ pgAdmin 4 (recommended - GUI tool)
   - ✅ Stack Builder (opsional)
   - ✅ Command Line Tools (WAJIB - ini yang membuat `psql` command)

5. **Data Directory** → Biarkan default, klik "**Next**"
   - Default: `C:\Program Files\PostgreSQL\16\data`

6. **Password** ⚠️ **PENTING!**
   - Masukkan password untuk user `postgres`
   - **CATAT PASSWORD INI!** Anda akan membutuhkannya nanti
   - Contoh: `postgres` (mudah diingat untuk development)
   - Atau password yang lebih kuat
   - Klik "**Next**"

7. **Port** → Biarkan default `5432`, klik "**Next**"
   - Kecuali ada aplikasi lain yang sudah pakai port ini

8. **Advanced Options** → Biarkan default, klik "**Next**"

9. **Pre Installation Summary** → Klik "**Next**"

10. **Ready to Install** → Klik "**Next**"
    - Installasi akan berjalan (beberapa menit)
    - Tunggu sampai selesai

11. **Completing the PostgreSQL Setup Wizard**
    - **JANGAN** centang "Launch Stack Builder" (opsional)
    - Centang "Launch pgAdmin 4?" jika ingin (opsional)
    - Klik "**Finish**"

### Langkah 3: Verifikasi Installasi

1. **Buka PowerShell atau Command Prompt BARU**
   - Tutup terminal yang lama
   - Buka terminal baru (supaya PATH ter-update)

2. **Test command:**
   ```powershell
   psql --version
   ```
   
   Jika berhasil, akan muncul:
   ```
   psql (PostgreSQL) 16.x
   ```

3. **Test koneksi:**
   ```powershell
   psql -U postgres
   ```
   
   Masukkan password yang Anda set tadi.

4. **Jika berhasil**, Anda akan melihat:
   ```
   postgres=#
   ```

5. **Keluar dari psql:**
   ```
   \q
   ```

### Langkah 4: Buat Database untuk Aplikasi

Setelah PostgreSQL terinstall dan running, buat database:

**Cara Paling Mudah:**
```powershell
create_database.bat
```

**Atau manual:**
```powershell
psql -U postgres
CREATE DATABASE review_analyzer;
\q
```

### Langkah 5: Setup Aplikasi

1. **Buat file `.env` di folder `backend`:**
   ```powershell
   cd backend
   copy env_example.txt .env
   ```

2. **Edit file `.env`** dengan notepad atau text editor:
   ```env
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/review_analyzer
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   **Ganti `YOUR_PASSWORD`** dengan password yang Anda set saat install PostgreSQL.

3. **Test aplikasi:**
   ```powershell
   cd backend
   venv\Scripts\activate
   python app.py
   ```

## ✅ Checklist

Setelah install, pastikan:

- [ ] `psql --version` berhasil
- [ ] `psql -U postgres` bisa connect
- [ ] Database `review_analyzer` sudah dibuat
- [ ] File `.env` sudah dikonfigurasi
- [ ] Aplikasi bisa connect ke database

## 🆘 Masalah Setelah Install?

### Masalah: `psql` masih tidak dikenali

**Solusi:**
1. **Tutup semua terminal/PowerShell**
2. **Buka terminal baru**
3. **Test lagi:**
   ```powershell
   psql --version
   ```

Jika masih tidak bekerja, tambahkan ke PATH manual:
1. Buka File Explorer
2. Navigate ke: `C:\Program Files\PostgreSQL\16\bin`
3. Copy path tersebut
4. Win + R → `sysdm.cpl` → Tab "Advanced"
5. Klik "Environment Variables"
6. Di "System variables", pilih "Path" → "Edit"
7. "New" → Paste path
8. OK semua
9. Restart terminal

### Masalah: "Connection refused" saat test

**Solusi:**
1. Buka Services (Win+R → `services.msc`)
2. Cari service `postgresql-x64-16`
3. Klik kanan → "Start"

### Masalah: Password salah

**Solusi:**
- Pastikan Anda menggunakan password yang Anda set saat install
- Jika lupa, reset password (lihat SETUP_DATABASE.md bagian Troubleshooting)

## 📚 Informasi Lebih Lanjut

Untuk troubleshooting lengkap, lihat: **SETUP_DATABASE.md**

## 🎉 Next Steps

Setelah PostgreSQL terinstall dan database dibuat:

1. ✅ Setup `.env` file
2. ✅ Install dependencies: `pip install -r requirements.txt`
3. ✅ Run aplikasi: `python app.py`

Good luck! 🚀

