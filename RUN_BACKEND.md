# Cara Menjalankan Backend

## Masalah: "Gagal memuat review" atau "ECONNREFUSED"

Error ini terjadi karena **backend Flask tidak berjalan**. Backend harus berjalan di port 5000 agar frontend bisa terhubung.

## Solusi: Jalankan Backend

### Langkah 1: Buka terminal baru (PowerShell)

Jangan tutup terminal frontend yang sedang berjalan!

### Langkah 2: Aktifkan virtual environment (jika ada)

```powershell
cd backend
.\venv\Scripts\Activate.ps1
```

### Langkah 3: Jalankan backend Flask

```powershell
python app.py
```

Atau jika menggunakan virtual environment:

```powershell
python app.py
```

### Langkah 4: Pastikan backend berjalan

Anda akan melihat output seperti:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Langkah 5: Test backend

Buka browser dan akses: `http://localhost:5000/api/health`

Harus muncul: `{"status": "healthy"}`

## Troubleshooting

### Jika ada error database:

1. Pastikan PostgreSQL berjalan
2. Buat database jika belum ada:
   ```powershell
   python create_database.py
   ```

### Jika ada error dependencies:

```powershell
pip install -r requirements.txt
```

### Jika port 5000 sudah digunakan:

Ubah port di `backend/app.py`:
```python
app.run(debug=True, port=5001)  # Ganti ke port lain
```

Dan update `frontend/vite.config.js`:
```javascript
target: 'http://localhost:5001',  // Sesuaikan dengan port baru
```

## Catatan

- **Frontend** harus berjalan di terminal pertama (port 5173)
- **Backend** harus berjalan di terminal kedua (port 5000)
- Keduanya harus berjalan **bersamaan**

