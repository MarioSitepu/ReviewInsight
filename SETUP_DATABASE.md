# 📚 Panduan Lengkap Setup Database PostgreSQL

Panduan komprehensif untuk mengatasi semua masalah database PostgreSQL dan setup aplikasi Product Review Analyzer.

---

## 📋 Daftar Isi

1. [Masalah Umum](#masalah-umum)
2. [Diagnosis Masalah](#diagnosis-masalah)
3. [Install PostgreSQL](#install-postgresql-di-windows)
4. [Start PostgreSQL Service](#start-postgresql-service)
5. [Buat Database](#membuat-database)
6. [Setup Aplikasi](#setup-aplikasi)
7. [Troubleshooting](#troubleshooting)
8. [Quick Reference](#quick-reference)

---

## 🔴 Masalah Umum

### Error: psql command not found

Jika Anda mendapatkan error:
```
psql : The term 'psql' is not recognized as the name of a cmdlet, function, script file, or operable program.
```

**Ini berarti PostgreSQL BELUM TERINSTALL atau command-line tools tidak ada di PATH.**

⚠️ **LANGKAH PERTAMA:** Install PostgreSQL terlebih dahulu! Lihat bagian [Install PostgreSQL](#-install-postgresql-di-windows).

### Error: Connection Refused

Jika Anda mendapatkan error:
```
connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
```

**Ini berarti PostgreSQL tidak berjalan atau belum terinstall.**

### Error: createdb command not found

```
bash: createdb: command not found
```

**Ini berarti PostgreSQL command-line tools tidak ada di PATH atau PostgreSQL belum terinstall.**

---

## 🔍 Diagnosis Masalah

### Langkah 1: Cek Apakah PostgreSQL Terinstall

**Jika Anda mendapatkan error `psql is not recognized`:**
- ❌ PostgreSQL **BELUM TERINSTALL**
- ⚠️ **Anda HARUS install PostgreSQL terlebih dahulu** sebelum bisa lanjut

**Jika `psql` command berhasil:**
```bash
psql --version
```
- ✅ PostgreSQL sudah terinstall
- Lanjut ke Langkah 2

### Langkah 2: Jalankan Script Diagnostic

Setelah PostgreSQL terinstall, jalankan script diagnostic:

```bash
check_postgresql.bat
```

Script ini akan menampilkan:
- ✅ Apakah PostgreSQL terinstall
- ✅ Apakah service PostgreSQL berjalan
- ✅ Apakah port 5432 tersedia
- ✅ Rekomendasi langkah selanjutnya

### Manual Check - Cek Service

**Cek apakah service berjalan:**
1. Tekan `Win + R`
2. Ketik: `services.msc` → Enter
3. Cari service: `postgresql-x64-16` (atau versi Anda)

---

## 💾 Install PostgreSQL di Windows

> ⚠️ **PENTING:** Jika Anda mendapatkan error `psql is not recognized`, ini berarti PostgreSQL belum terinstall. Ikuti langkah-langkah di bawah ini untuk install PostgreSQL.

### Langkah 1: Download PostgreSQL

1. Buka browser dan kunjungi:
   ```
   https://www.postgresql.org/download/windows/
   ```

2. Klik tombol **"Download the installer"**

3. Pilih versi:
   - **PostgreSQL 16** (recommended - versi terbaru)
   - Atau PostgreSQL 15/14 (juga OK)

### Langkah 2: Install PostgreSQL

1. **Jalankan installer** yang sudah didownload
   - File biasanya: `postgresql-16-x64.exe` atau similar

2. **Welcome Screen** → Klik "Next"

3. **Installation Directory** → Biarkan default, klik "Next"
   - Default: `C:\Program Files\PostgreSQL\16`

4. **Select Components** → Centang semua, klik "Next"
   - ✅ PostgreSQL Server
   - ✅ pgAdmin 4
   - ✅ Stack Builder
   - ✅ Command Line Tools

5. **Data Directory** → Biarkan default, klik "Next"
   - Default: `C:\Program Files\PostgreSQL\16\data`

6. **Password** ⚠️ **PENTING!**
   - Masukkan password untuk user `postgres`
   - **CATAT PASSWORD INI!** Anda akan membutuhkannya
   - Contoh: `postgres` atau password kuat lainnya
   - Klik "Next"

7. **Port** → Biarkan default `5432`, klik "Next"
   - Kecuali ada aplikasi lain yang pakai port ini

8. **Advanced Options** → Biarkan default, klik "Next"

9. **Pre Installation Summary** → Klik "Next"

10. **Ready to Install** → Klik "Next"
    - Installasi akan berjalan (beberapa menit)

11. **Completing** → **JANGAN** centang Stack Builder (opsional), klik "Finish"

### Langkah 3: Verifikasi Installasi

1. **Buka Command Prompt** atau PowerShell

2. **Test koneksi:**
   ```bash
   psql -U postgres
   ```
   Masukkan password yang Anda set tadi.

3. **Jika berhasil**, Anda akan melihat:
   ```
   postgres=#
   ```

4. Ketik `\q` untuk keluar.

### Alternative: Install via Chocolatey

Jika Anda punya Chocolatey:

```bash
choco install postgresql16
```

---

## ▶️ Start PostgreSQL Service

Jika PostgreSQL sudah terinstall tapi tidak running:

### Cara 1: Menggunakan Services (GUI)

1. Tekan `Win + R`
2. Ketik: `services.msc` → Enter
3. Cari service dengan nama:
   - `postgresql-x64-16` (atau versi Anda)
   - Atau `PostgreSQL Database Server`
4. **Start Service:**
   - Klik kanan → "Start"
   - Atau double-click → "Start" button
5. **Set Auto-Start (Opsional):**
   - Klik kanan → "Properties"
   - "Startup type" → Pilih "Automatic"
   - OK

### Cara 2: Menggunakan Command Line (Administrator)

```bash
net start postgresql-x64-16
```

Ganti `16` dengan versi PostgreSQL Anda.

---

## 🗄️ Membuat Database

Setelah PostgreSQL running, buat database untuk aplikasi. Ada beberapa cara:

### ✅ Cara 1: Menggunakan Script Python (Paling Mudah - Recommended)

**Windows:**
```bash
create_database.bat
```

**Linux/Mac:**
```bash
chmod +x create_database.sh
./create_database.sh
```

**Manual Python:**
```bash
cd backend
python create_database.py
```

**Keuntungan:**
- ✅ Tidak perlu `createdb` command
- ✅ Bekerja di semua platform
- ✅ Otomatis cek apakah database sudah ada
- ✅ Error message yang jelas

### ✅ Cara 2: Menggunakan psql

```bash
# Connect to PostgreSQL
psql -U postgres

# Inside psql, run:
CREATE DATABASE review_analyzer;

# Exit psql
\q
```

### ✅ Cara 3: Menggunakan pgAdmin (GUI)

1. Buka pgAdmin
2. Connect ke PostgreSQL server
3. Klik kanan "Databases"
4. Pilih "Create" → "Database"
5. Nama: `review_analyzer`
6. Klik "Save"

### ✅ Cara 4: Menggunakan createdb Command

Jika `createdb` command tersedia:

```bash
createdb -U postgres review_analyzer
```

**Jika command tidak ditemukan, tambahkan ke PATH:**

**Windows:**
1. Buka File Explorer
2. Navigate ke: `C:\Program Files\PostgreSQL\16\bin`
3. Copy path tersebut
4. Add ke System PATH:
   - Win + R → `sysdm.cpl` → Tab "Advanced"
   - Klik "Environment Variables"
   - Di "System variables", pilih "Path" → "Edit"
   - "New" → Paste path `C:\Program Files\PostgreSQL\16\bin`
   - OK semua
   - Restart Command Prompt

### Custom Database Credentials

Jika username/password PostgreSQL berbeda:

**Menggunakan Script dengan Parameter:**
```bash
python backend/create_database.py --user youruser --password yourpass --host localhost --port 5432
```

**Atau buat file `.env` di folder `backend`:**
```env
DATABASE_URL=postgresql://youruser:yourpassword@localhost:5432/review_analyzer
```

Script akan otomatis membaca dari file `.env`.

### Verifikasi Database

Setelah membuat database, verifikasi:

**Menggunakan psql:**
```bash
psql -U postgres -l | findstr review_analyzer
```

**Menggunakan Python:**
```bash
cd backend
python -c "import psycopg2; conn = psycopg2.connect('postgresql://postgres:postgres@localhost:5432/review_analyzer'); print('✅ Database connection successful!')"
```

---

## ⚙️ Setup Aplikasi

### Step 1: Buat File .env

1. **Copy template:**
   ```bash
   cd backend
   copy env_example.txt .env
   ```

2. **Edit file `.env`:**
   ```env
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/review_analyzer
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   **Ganti:**
   - `YOUR_PASSWORD` dengan password PostgreSQL Anda
   - `your_gemini_api_key_here` dengan API key Gemini Anda

### Step 2: Install Dependencies Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# atau
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

### Step 3: Test Koneksi Database

```bash
cd backend
python app.py
```

Jika berhasil, Anda akan melihat:
```
 * Running on http://127.0.0.1:5000
```

Database tables akan dibuat otomatis saat pertama kali run.

---

## 🔧 Troubleshooting

### Issue 1: "psql is not recognized"

**Problem:** PostgreSQL command-line tools tidak di PATH.

**Solusi:**
1. Buka File Explorer
2. Navigate ke: `C:\Program Files\PostgreSQL\16\bin` (ganti 16 dengan versi Anda)
3. Copy path tersebut
4. Add ke System PATH (lihat instruksi di bagian "Membuat Database" - Cara 4)
5. Restart Command Prompt

### Issue 2: "Connection refused"

**Problem:** PostgreSQL service tidak running.

**Solusi:**
1. Buka Services (Win+R → `services.msc`)
2. Cari `postgresql-x64-16` (atau versi Anda)
3. Start service
4. Set "Startup type" menjadi "Automatic"

### Issue 3: "Password authentication failed"

**Problem:** Password salah.

**Solusi A - Reset Password:**
```bash
# Buka Command Prompt sebagai Administrator
cd "C:\Program Files\PostgreSQL\16\bin"
psql -U postgres
ALTER USER postgres PASSWORD 'newpassword';
\q
```

**Solusi B - Update .env:**
- Edit file `backend/.env` dengan password yang benar

### Issue 4: "port 5432 already in use"

**Problem:** Port 5432 sudah digunakan aplikasi lain.

**Solusi A - Cek aplikasi yang menggunakan port:**
```bash
netstat -ano | findstr :5432
```

**Solusi B - Gunakan port berbeda:**
- Install PostgreSQL dengan port berbeda (misal 5433)
- Update `DATABASE_URL` di `.env` file dengan port baru

### Issue 5: "cannot connect to server"

**Solusi:**
1. Pastikan PostgreSQL service running
2. Cek firewall settings
3. Verifikasi host/port di connection string
4. Cek log PostgreSQL di: `C:\Program Files\PostgreSQL\[version]\data\log\`

### Issue 6: Database creation failed

**Solusi:**
1. Pastikan PostgreSQL service running
2. Cek kredensial (username/password)
3. Pastikan user `postgres` punya permission untuk create database
4. Cek log error untuk detail

---

## 📊 Quick Reference

### Checklist Setup

- [ ] PostgreSQL terinstall? (`psql --version`)
- [ ] PostgreSQL service running? (Services.msc)
- [ ] Port 5432 available? (`check_postgresql.bat`)
- [ ] Database `review_analyzer` dibuat? (`create_database.bat`)
- [ ] File `.env` dikonfigurasi? (`backend/.env`)
- [ ] Dependencies terinstall? (`pip install -r requirements.txt`)
- [ ] Aplikasi bisa connect? (`python app.py`)

### Command Reference

| Task | Command |
|------|---------|
| Check PostgreSQL version | `psql --version` |
| Connect to PostgreSQL | `psql -U postgres` |
| List databases | `psql -U postgres -l` |
| Create database | `CREATE DATABASE review_analyzer;` |
| Check service status | `sc query postgresql-x64-16` |
| Start service | `net start postgresql-x64-16` |
| Check port | `netstat -ano \| findstr :5432` |

### Quick Solutions Table

| Masalah | Solusi Cepat |
|---------|--------------|
| PostgreSQL tidak terinstall | Download dari postgresql.org/download/windows/ |
| Service tidak running | Start dari Services.msc atau `net start postgresql-x64-XX` |
| Password salah | Reset password atau update `.env` |
| Port berbeda | Update port di `.env` file |
| createdb not found | Gunakan `create_database.bat` atau `psql` |
| Connection refused | Start PostgreSQL service |

---

## 📖 Informasi Tambahan

### Download Links

- **Official Download:** https://www.postgresql.org/download/windows/
- **Documentation:** https://www.postgresql.org/docs/

### File-File Helper

- `check_postgresql.bat` - Script diagnostic PostgreSQL
- `create_database.bat` - Script untuk membuat database (Windows)
- `create_database.sh` - Script untuk membuat database (Linux/Mac)
- `backend/create_database.py` - Script Python utama

### Log Files Location

PostgreSQL log files biasanya ada di:
```
C:\Program Files\PostgreSQL\[version]\data\log\
```

### Default Credentials

- **Username:** `postgres`
- **Password:** (yang Anda set saat install)
- **Port:** `5432`
- **Host:** `localhost`

---

## ✅ Next Steps

Setelah database setup selesai:

1. ✅ Setup `.env` file dengan kredensial yang benar
2. ✅ Install dependencies backend: `pip install -r requirements.txt`
3. ✅ Install dependencies frontend: `cd frontend && npm install`
4. ✅ Run backend: `cd backend && python app.py`
5. ✅ Run frontend: `cd frontend && npm start`
6. ✅ Test aplikasi di browser: `http://localhost:3000`

---

## 🆘 Butuh Bantuan Lebih?

1. Jalankan `check_postgresql.bat` untuk diagnosis lengkap
2. Cek log PostgreSQL di folder `data/log`
3. Baca dokumentasi resmi: https://www.postgresql.org/docs/
4. Pastikan semua checklist sudah ditandai

Good luck! 🚀

