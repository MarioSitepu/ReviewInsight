# Render Troubleshooting Guide

Panduan troubleshooting khusus untuk masalah deployment di Render.

## Masalah: Worker Timeout / Out of Memory

### Gejala:
```
[CRITICAL] WORKER TIMEOUT (pid:23)
[ERROR] Worker (pid:23) was sent SIGKILL! Perhaps out of memory?
```

### Penyebab:
- Torch + Transformers memakan banyak memory (~2GB+)
- Free tier Render hanya punya 512MB RAM
- 2 workers terlalu banyak untuk free tier

### Solusi:

**1. Reduce Workers (Sudah di-fix di start.sh)**
- Menggunakan 1 worker instead of 2
- File: `backend/start.sh`

**2. Upgrade Plan (Jika masih timeout)**
- Free tier: 512MB RAM
- Starter plan: $7/month - 512MB RAM (tapi lebih reliable)
- Standard plan: $25/month - 2GB RAM (recommended untuk production)

**3. Optimize Model Loading**
- Model di-load saat pertama kali digunakan (lazy loading)
- Sudah di-implement di `sentiment_analyzer.py`

**4. Use CPU-only Torch (Optional)**
- Torch dengan CUDA lebih besar
- CPU-only lebih kecil tapi lebih lambat
- Sudah di-set `device=-1` untuk force CPU

## Masalah: Port Not Detected

### Gejala:
```
==> No open HTTP ports detected on 0.0.0.0
==> Port scan timeout reached, no open HTTP ports detected
```

### Penyebab:
- Aplikasi tidak listen di port yang benar
- PORT environment variable tidak digunakan
- Aplikasi listen di 127.0.0.1 instead of 0.0.0.0

### Solusi:

**1. Check start.sh**
- Pastikan menggunakan `$PORT` environment variable
- Pastikan bind ke `0.0.0.0`, bukan `127.0.0.1`

**2. Check Logs**
- Lihat log untuk melihat port yang digunakan
- Seharusnya: `Listening at: http://0.0.0.0:XXXX`

**3. Manual Port Check**
- Di Render dashboard, check environment variables
- Pastikan `PORT` tidak di-set manual (Render set otomatis)

## Masalah: Slow Build / Dependency Resolution

### Gejala:
```
INFO: pip is looking at multiple versions of grpcio-status...
This is taking longer than usual...
```

### Penyebab:
- Dependency resolution kompleks (torch dependencies)
- Banyak versi yang perlu di-check
- Normal untuk pertama kali

### Solusi:

**1. Wait it Out**
- Normal untuk build pertama kali (5-10 menit)
- Subsequent builds lebih cepat (Docker cache)

**2. Optimize requirements.txt**
- Pin specific versions untuk mengurangi resolution time
- Contoh: `grpcio-status==1.62.3` instead of range

**3. Use Build Cache**
- Render menggunakan Docker layer caching
- Perubahan kecil tidak perlu rebuild semua

## Masalah: Build Timeout

### Gejala:
- Build gagal dengan timeout
- Download torch/transformers terputus

### Solusi:

**1. Increase Timeout (Render Dashboard)**
- Settings → Build Command
- Add timeout jika ada opsi

**2. Split Dependencies**
- Install torch separately dengan timeout lebih lama
- Update Dockerfile untuk install torch dengan `--timeout=600`

**3. Use Pre-built Image**
- Build image lokal
- Push ke Docker Hub
- Pull di Render (lebih cepat)

## Best Practices untuk Render

### 1. Memory Management
- ✅ Use 1 worker untuk free tier
- ✅ Lazy load models
- ✅ Use CPU-only torch
- ✅ Monitor memory usage di Render dashboard

### 2. Port Configuration
- ✅ Always use `$PORT` environment variable
- ✅ Bind to `0.0.0.0`, not `127.0.0.1`
- ✅ Don't hardcode port numbers

### 3. Build Optimization
- ✅ Use `.dockerignore` untuk exclude files besar
- ✅ Multi-stage builds untuk reduce image size
- ✅ Cache dependencies dengan proper layer ordering

### 4. Monitoring
- ✅ Check logs regularly
- ✅ Monitor memory usage
- ✅ Setup alerts untuk errors
- ✅ Check health check status

## Quick Fixes

### Fix Worker Timeout:
```bash
# Update start.sh - reduce workers
--workers 1  # Instead of 2
```

### Fix Port Issue:
```bash
# Check start.sh uses $PORT
PORT=${PORT:-5000}
exec gunicorn --bind 0.0.0.0:$PORT ...
```

### Fix Memory Issue:
```python
# In sentiment_analyzer.py
pipeline(..., device=-1)  # Force CPU
```

## Upgrade Path

Jika masalah persist dengan free tier:

1. **Starter Plan ($7/month)**
   - 512MB RAM (sama, tapi lebih reliable)
   - Always-on (no sleep)
   - Better support

2. **Standard Plan ($25/month)**
   - 2GB RAM (cukup untuk 2 workers)
   - Always-on
   - Better performance

3. **Alternative: Use Lighter Models**
   - Gunakan model yang lebih kecil
   - Trade-off: accuracy vs memory

## Support

- Render Docs: https://render.com/docs
- Render Status: https://status.render.com
- Render Community: https://community.render.com

