# Cara Menjalankan Aplikasi Review Analyzer

## ⚠️ PENTING: Backend HARUS berjalan!

Error `ECONNREFUSED` terjadi karena **backend Flask tidak berjalan**. 

## Langkah-langkah Menjalankan

### 1. Terminal Pertama: Jalankan Backend

Buka PowerShell dan jalankan:

```powershell
cd "C:\Users\ASUS\Documents\Belajar\Kuliah\Tugas PemWeb\TugasPemWeb3\backend"
.\venv\Scripts\Activate.ps1
python app.py
```

**ATAU** gunakan file batch yang sudah dibuat:

```powershell
cd backend
.\start_backend.bat
```

**Output yang benar:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

**JANGAN TUTUP TERMINAL INI!** Backend harus tetap berjalan.

---

### 2. Terminal Kedua: Jalankan Frontend

Buka PowerShell baru (jangan tutup terminal backend) dan jalankan:

```powershell
cd "C:\Users\ASUS\Documents\Belajar\Kuliah\Tugas PemWeb\TugasPemWeb3\frontend"
npm run dev
```

**Output yang benar:**
```
  VITE v5.4.21  ready in XXX ms
  ➜  Local:   http://localhost:5173/
```

---

### 3. Buka Browser

Akses: `http://localhost:5173` (atau port yang ditampilkan di terminal)

---

## Troubleshooting

### ❌ Error: "ModuleNotFoundError: No module named 'flask'"

**Solusi:** Aktifkan virtual environment terlebih dahulu:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python app.py
```

### ❌ Error: "ECONNREFUSED" di frontend

**Penyebab:** Backend tidak berjalan

**Solusi:** 
1. Pastikan backend berjalan di terminal pertama
2. Cek apakah backend berjalan di `http://localhost:5000`
3. Test dengan membuka: `http://localhost:5000/api/health` di browser
   - Harus muncul: `{"status": "healthy"}`

### ❌ Error: Database connection error

**Solusi:** 
1. Pastikan PostgreSQL berjalan
2. Buat database jika belum ada:
   ```powershell
   cd backend
   python create_database.py
   ```

### ❌ Error: Port 5000 sudah digunakan

**Solusi:** 
1. Tutup aplikasi lain yang menggunakan port 5000
2. Atau ubah port di `backend/app.py`:
   ```python
   app.run(debug=True, port=5001)  # Ganti ke port lain
   ```
3. Update `frontend/vite.config.js`:
   ```javascript
   target: 'http://localhost:5001',  // Sesuaikan
   ```

---

## Checklist

- [ ] Backend berjalan di terminal pertama (port 5000)
- [ ] Frontend berjalan di terminal kedua (port 5173)
- [ ] PostgreSQL berjalan
- [ ] Database sudah dibuat
- [ ] Tidak ada error di kedua terminal

---

## Catatan

- **Kedua terminal harus berjalan bersamaan**
- Backend harus berjalan **sebelum** frontend
- Jika salah satu terminal ditutup, aplikasi akan error

