# Setup Environment Variables di Vercel

## Masalah

Frontend masih mengakses `http://localhost:5000` padahal sudah di-deploy di Vercel.

## Penyebab

Environment variable `VITE_API_URL` belum di-set di Vercel, atau frontend belum di-redeploy setelah set env var.

## Solusi

### Step 1: Set Environment Variable di Vercel

1. **Buka Vercel Dashboard**
   - Login ke https://vercel.com
   - Pilih project `review-insight-nine`

2. **Buka Settings → Environment Variables**

3. **Add Environment Variable:**
   - **Key**: `VITE_API_URL`
   - **Value**: `https://review-insight-backend.onrender.com/api`
     - **PENTING**: Ganti `review-insight-backend` dengan nama service backend Anda di Render!
     - Contoh jika backend Anda: `https://my-backend-abc123.onrender.com/api`
   - **Environment**: Pilih semua (Production, Preview, Development)

4. **Save**

### Step 2: Redeploy Frontend

**Penting**: Setelah set environment variable, Anda HARUS redeploy!

**Cara 1: Via Dashboard**
1. Buka **Deployments** tab
2. Klik **...** (three dots) pada deployment terbaru
3. Pilih **Redeploy**
4. Tunggu build selesai

**Cara 2: Via Git Push**
```bash
# Buat commit kosong untuk trigger redeploy
git commit --allow-empty -m "Trigger Vercel redeploy for env vars"
git push origin main
```

### Step 3: Verify

1. **Check Build Logs:**
   - Buka deployment di Vercel
   - Check build logs
   - Pastikan tidak ada error

2. **Check Browser Console:**
   - Buka `https://review-insight-nine.vercel.app`
   - Open DevTools → Console
   - Check apakah `API_BASE_URL` sudah benar (tidak ada `localhost:5000`)

3. **Test API Call:**
   - Open DevTools → Network tab
   - Coba analisis review
   - Check request URL - harus ke Render backend, bukan localhost

## Troubleshooting

### Masih Mengakses Localhost?

**1. Check Environment Variable:**
   - Pastikan `VITE_API_URL` sudah di-set di Vercel
   - Pastikan value benar (dengan `/api` di akhir)
   - Pastikan environment scope benar (Production, Preview, Development)

**2. Check Build Logs:**
   - Buka deployment → Build Logs
   - Search untuk `VITE_API_URL`
   - Pastikan variable ter-inject saat build

**3. Force Redeploy:**
   ```bash
   # Buat commit untuk trigger redeploy
   git commit --allow-empty -m "Force redeploy"
   git push origin main
   ```

**4. Check Code:**
   - Pastikan `App.jsx` menggunakan `import.meta.env.VITE_API_URL`
   - Pastikan tidak ada hardcoded `localhost:5000` di code

### CORS Error Masih Ada?

Jika setelah set `VITE_API_URL` masih ada CORS error:

1. **Check Backend CORS:**
   - Pastikan backend di Render sudah running
   - Check backend logs di Render dashboard
   - Pastikan CORS allow semua origins (atau set specific origins)

2. **Test Backend Directly:**
   ```bash
   curl https://review-insight-backend.onrender.com/api/health
   ```
   Seharusnya return: `{"status": "healthy"}`

3. **Check Browser Network Tab:**
   - Open DevTools → Network
   - Check request headers
   - Check response headers (harus ada `Access-Control-Allow-Origin`)

## Quick Checklist

- [ ] `VITE_API_URL` sudah di-set di Vercel
- [ ] Value benar (Render backend URL dengan `/api`)
- [ ] Environment scope: Production, Preview, Development
- [ ] Frontend sudah di-redeploy setelah set env var
- [ ] Build logs tidak ada error
- [ ] Browser console tidak ada `localhost:5000`
- [ ] Network tab menunjukkan request ke Render backend
- [ ] Tidak ada CORS error

## Alternative: Update Code Default

Jika tidak ingin set environment variable, Anda bisa update default di `App.jsx`:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.PROD 
    ? 'https://YOUR-ACTUAL-BACKEND-URL.onrender.com/api'  // Ganti dengan URL backend Anda
    : '/api'
  );
```

Tapi lebih baik menggunakan environment variable untuk fleksibilitas.

