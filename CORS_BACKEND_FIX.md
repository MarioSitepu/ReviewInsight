# Fix CORS Error - Backend di Render

## Masalah

Frontend di Vercel (`https://review-insight-nine.vercel.app`) mendapat CORS error saat mengakses backend di Render (`https://reviewinsight-xomf.onrender.com`).

Error:
```
Access to XMLHttpRequest at 'https://reviewinsight-xomf.onrender.com/api/reviews' 
from origin 'https://review-insight-nine.vercel.app' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present
```

## Penyebab

Backend di Render tidak mengirim CORS headers dengan benar, atau CORS configuration belum di-update.

## Solusi

### Step 1: Verify Backend Environment Variables di Render

1. **Buka Render Dashboard**
   - Login ke https://render.com
   - Pilih service `reviewinsight-xomf` (atau nama backend Anda)

2. **Buka Environment Tab**
   - Check environment variables:
     - `FLASK_ENV=production` (harus ada!)
     - `ALLOWED_ORIGINS` (opsional, bisa dikosongkan untuk allow all)

3. **Update Environment Variables:**
   ```
   FLASK_ENV=production
   ALLOWED_ORIGINS=  (kosongkan untuk allow all origins)
   ```
   Atau set specific origins:
   ```
   ALLOWED_ORIGINS=https://review-insight-nine.vercel.app,https://*.vercel.app
   ```

### Step 2: Redeploy Backend

**Penting**: Setelah update environment variables atau code, backend HARUS di-redeploy!

1. **Via Dashboard:**
   - Render Dashboard → Service → Manual Deploy → Deploy latest commit
   - Atau tunggu auto-deploy jika sudah connect ke GitHub

2. **Via Git Push:**
   ```bash
   git add .
   git commit -m "fix: update CORS configuration"
   git push origin main
   ```

### Step 3: Test Backend CORS

**Test dengan curl:**

```bash
# Test OPTIONS request (preflight)
curl -X OPTIONS \
  -H "Origin: https://review-insight-nine.vercel.app" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v \
  https://reviewinsight-xomf.onrender.com/api/reviews

# Expected response headers:
# Access-Control-Allow-Origin: *
# Access-Control-Allow-Methods: GET, POST, DELETE, OPTIONS
# Access-Control-Allow-Headers: Content-Type, Authorization
```

**Test GET request:**

```bash
curl -X GET \
  -H "Origin: https://review-insight-nine.vercel.app" \
  -v \
  https://reviewinsight-xomf.onrender.com/api/reviews

# Expected response headers:
# Access-Control-Allow-Origin: *
```

### Step 4: Check Backend Logs

1. **Buka Render Dashboard**
2. **Service → Logs**
3. **Check untuk CORS messages:**
   ```
   [CORS] Production mode: Allowing all origins (*)
   ```
   Atau:
   ```
   [CORS] Production mode: Using specific origins: [...]
   ```

4. **Check untuk errors:**
   - Pastikan tidak ada error saat startup
   - Pastikan Flask app berhasil start

## Troubleshooting

### Masih Ada CORS Error?

**1. Check Backend Status:**
   - Pastikan backend sudah running di Render
   - Check health endpoint: `https://reviewinsight-xomf.onrender.com/api/health`
   - Seharusnya return: `{"status": "healthy"}`

**2. Check Environment Variables:**
   - Pastikan `FLASK_ENV=production` sudah di-set
   - Pastikan `ALLOWED_ORIGINS` kosong (atau set ke specific origins)
   - Redeploy setelah update env vars

**3. Check Backend Code:**
   - Pastikan `backend/app.py` sudah di-update dengan CORS fix
   - Pastikan `flask-cors` sudah di-install (`requirements.txt`)

**4. Test Backend Directly:**
   ```bash
   # Test health endpoint
   curl https://reviewinsight-xomf.onrender.com/api/health
   
   # Test with CORS headers
   curl -H "Origin: https://review-insight-nine.vercel.app" \
        -H "Access-Control-Request-Method: GET" \
        -X OPTIONS \
        https://reviewinsight-xomf.onrender.com/api/reviews \
        -v
   ```

**5. Check Browser Network Tab:**
   - Open DevTools → Network
   - Check request headers (harus ada `Origin: https://review-insight-nine.vercel.app`)
   - Check response headers (harus ada `Access-Control-Allow-Origin: *`)

### Backend Not Responding?

**1. Check Backend Logs:**
   - Render Dashboard → Service → Logs
   - Check untuk errors atau warnings
   - Pastikan Gunicorn sudah start dengan benar

**2. Check Backend Health:**
   ```bash
   curl https://reviewinsight-xomf.onrender.com/api/health
   ```
   Jika tidak respond, backend mungkin:
   - Masih starting up (tunggu 1-2 menit)
   - Error saat startup (check logs)
   - Sleep (free tier sleep setelah 15 menit idle)

**3. Restart Backend:**
   - Render Dashboard → Service → Manual Deploy → Deploy latest commit

## Quick Fix Checklist

- [ ] `FLASK_ENV=production` sudah di-set di Render
- [ ] `ALLOWED_ORIGINS` kosong (atau set ke specific origins)
- [ ] Backend code sudah di-update dengan CORS fix
- [ ] Backend sudah di-redeploy setelah update
- [ ] Backend logs menunjukkan CORS configuration
- [ ] Health endpoint accessible: `/api/health`
- [ ] CORS headers muncul di response (test dengan curl)
- [ ] Browser Network tab menunjukkan CORS headers

## Expected CORS Headers

Response dari backend harus include:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 3600
```

Jika headers ini tidak muncul, CORS configuration belum benar.

## Alternative: Set Specific Origins

Jika ingin lebih secure, set specific origins di `ALLOWED_ORIGINS`:

```
ALLOWED_ORIGINS=https://review-insight-nine.vercel.app,https://review-insight-nine-git-main-yourusername.vercel.app
```

Tapi ini akan block preview deployments. Lebih baik gunakan `*` untuk development/testing.

