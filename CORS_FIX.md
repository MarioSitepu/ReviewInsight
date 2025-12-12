# CORS Fix untuk Vercel + Render

## Masalah

Frontend di Vercel (`https://review-insight-nine.vercel.app`) mendapat CORS error saat mengakses backend di Render.

## Solusi

### 1. Update Backend CORS (backend/app.py)

Backend sudah di-update untuk:
- Allow semua origins di production (untuk fleksibilitas dengan Vercel preview deployments)
- Allow localhost origins di development
- Support `ALLOWED_ORIGINS` environment variable untuk specific origins

### 2. Update Frontend API URL (frontend/src/App.jsx)

Frontend sudah di-update untuk:
- Menggunakan Render backend URL sebagai default di production
- Menggunakan Vite proxy di development

### 3. Set Environment Variable di Vercel

**Penting**: Set `VITE_API_URL` di Vercel environment variables:

1. Buka Vercel Dashboard
2. Pilih project `review-insight-nine`
3. Settings → Environment Variables
4. Add:
   ```
   VITE_API_URL=https://review-insight-backend.onrender.com/api
   ```
   **Ganti `review-insight-backend` dengan nama service backend Anda di Render**

5. Redeploy frontend

### 4. Verify Backend CORS

Backend di Render harus:
- Set `FLASK_ENV=production` di environment variables
- Tidak set `ALLOWED_ORIGINS` (atau set ke specific origins jika perlu)

Jika `ALLOWED_ORIGINS` tidak di-set, backend akan allow semua origins (menggunakan `*`).

## Testing

1. **Test Backend CORS:**
   ```bash
   curl -H "Origin: https://review-insight-nine.vercel.app" \
        -H "Access-Control-Request-Method: POST" \
        -H "Access-Control-Request-Headers: Content-Type" \
        -X OPTIONS \
        https://review-insight-backend.onrender.com/api/analyze-review
   ```
   Seharusnya return headers dengan `Access-Control-Allow-Origin: *`

2. **Test Frontend:**
   - Buka `https://review-insight-nine.vercel.app`
   - Check browser console - tidak ada CORS error
   - Test analisis review

## Troubleshooting

### Masih ada CORS error?

1. **Check Vercel Environment Variables:**
   - Pastikan `VITE_API_URL` sudah di-set
   - Pastikan value benar (dengan `/api` di akhir)
   - Redeploy setelah set environment variable

2. **Check Backend Logs:**
   - Buka Render dashboard → Backend service → Logs
   - Check apakah ada error saat startup
   - Verify CORS configuration loaded dengan benar

3. **Check Browser Console:**
   - Open DevTools → Network tab
   - Check request headers
   - Check response headers (harus ada `Access-Control-Allow-Origin`)

4. **Manual CORS Test:**
   ```bash
   # Test dari command line
   curl -X POST https://review-insight-backend.onrender.com/api/analyze-review \
     -H "Content-Type: application/json" \
     -H "Origin: https://review-insight-nine.vercel.app" \
     -d '{"review_text": "test"}'
   ```

## Security Note

**Production Best Practice:**
Untuk production, lebih baik set specific origins di `ALLOWED_ORIGINS`:

```
ALLOWED_ORIGINS=https://review-insight-nine.vercel.app,https://your-production-domain.com
```

Ini akan membatasi CORS hanya ke domains yang diizinkan, lebih secure daripada menggunakan `*`.

