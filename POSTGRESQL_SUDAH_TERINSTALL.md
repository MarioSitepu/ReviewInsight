# ✅ PostgreSQL Sudah Terinstall - Langkah Selanjutnya

## Situasi Anda

Installer mendeteksi PostgreSQL sudah terinstall di:
```
C:\Program Files\PostgreSQL\18
```

Ini berarti PostgreSQL **sudah ada**, tapi kemungkinan:
1. Command-line tools (`psql`) tidak ada di PATH
2. Service tidak running
3. Perlu upgrade

## ✅ Solusi: Lanjutkan dengan Upgrade

### Opsi 1: Lanjutkan Upgrade (Recommended)

1. **Klik "Next" atau "Continue"** di installer
2. **Biarkan installer melakukan upgrade**
3. **Pastikan "Command Line Tools" tercentang** saat install
4. **Selesai install**

5. **Tutup semua terminal/PowerShell**
6. **Buka PowerShell BARU**

7. **Test command:**
   ```powershell
   psql --version
   ```

### Opsi 2: Jika Upgrade Selesai tapi `psql` Masih Tidak Dikenali

Jika setelah upgrade `psql` masih tidak dikenali:

#### Langkah 1: Tambahkan PostgreSQL ke PATH

1. **Buka File Explorer**
2. **Navigate ke:**
   ```
   C:\Program Files\PostgreSQL\18\bin
   ```
3. **Copy path tersebut** (Ctrl+C)

4. **Tambahkan ke System PATH:**
   - Tekan `Win + R`
   - Ketik: `sysdm.cpl` → Enter
   - Tab "**Advanced**"
   - Klik "**Environment Variables**"
   - Di bagian "**System variables**", cari dan pilih "**Path**"
   - Klik "**Edit**"
   - Klik "**New**"
   - Paste path: `C:\Program Files\PostgreSQL\18\bin`
   - Klik "**OK**" di semua dialog

5. **Tutup semua terminal/PowerShell**
6. **Buka PowerShell BARU**
7. **Test:**
   ```powershell
   psql --version
   ```

#### Langkah 2: Cek Apakah Service Running

1. **Tekan `Win + R`**
2. **Ketik: `services.msc`** → Enter
3. **Cari service:** `postgresql-x64-18` (atau `postgresql-x64-16` tergantung versi)
4. **Cek status:**
   - Jika "Running" = ✅ OK
   - Jika "Stopped" = ❌ Klik kanan → "Start"

#### Langkah 3: Test Koneksi

```powershell
psql -U postgres
```

Jika diminta password, masukkan password yang Anda set saat install PostgreSQL.

## ✅ Setelah psql Berfungsi

### 1. Buat Database

**Cara Termudah:**
```powershell
create_database.bat
```

**Atau Manual:**
```powershell
psql -U postgres
CREATE DATABASE review_analyzer;
\q
```

### 2. Setup .env File

1. **Buat file `.env` di folder `backend`:**
   ```powershell
   cd backend
   copy env_example.txt .env
   ```

2. **Edit file `.env`** dengan Notepad:
   ```env
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/review_analyzer
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   **Ganti `YOUR_PASSWORD`** dengan password PostgreSQL Anda.

### 3. Test Aplikasi

```powershell
cd backend
venv\Scripts\activate
python app.py
```

## 🔍 Verifikasi Instalasi

Jalankan script diagnostic:
```powershell
check_postgresql.bat
```

Script ini akan memberitahu:
- ✅ Apakah PostgreSQL terinstall
- ✅ Apakah service running
- ✅ Apakah port 5432 tersedia

## ⚠️ Jika Masih Bermasalah

### Masalah: "psql is not recognized" setelah upgrade

**Solusi:**
1. Pastikan "Command Line Tools" tercentang saat install
2. Tambahkan ke PATH manual (lihat Langkah 1 di atas)
3. Restart komputer (terkadang diperlukan)

### Masalah: Lupa Password PostgreSQL

**Solusi:**
1. Coba password umum: `postgres`
2. Atau reset password (lihat SETUP_DATABASE.md)

### Masalah: Service tidak running

**Solusi:**
1. Buka Services (Win+R → `services.msc`)
2. Cari service PostgreSQL
3. Start service
4. Set "Startup type" menjadi "Automatic"

## 📚 File Bantuan

- `SETUP_DATABASE.md` - Panduan lengkap troubleshooting
- `check_postgresql.bat` - Script diagnostic

## ✅ Checklist

Setelah upgrade dan setup:

- [ ] `psql --version` berhasil
- [ ] PostgreSQL service running (Services.msc)
- [ ] `psql -U postgres` bisa connect
- [ ] Database `review_analyzer` dibuat
- [ ] File `.env` dikonfigurasi
- [ ] Aplikasi bisa connect

Good luck! 🚀

