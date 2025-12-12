# Deployment Guide: Render dengan Docker

Panduan lengkap untuk deploy ReviewInsight ke Render menggunakan Docker.

## Apa itu Render?

Render adalah platform cloud yang:
- ✅ **Gratis** untuk web services (dengan limitations)
- ✅ **Auto-deploy** dari GitHub
- ✅ **Docker support** - deploy langsung dari Dockerfile
- ✅ **HTTPS** otomatis
- ✅ **Custom domains** gratis
- ✅ **Environment variables** management

## Prerequisites

- Akun Render (gratis): https://render.com
- Akun GitHub (untuk auto-deploy)
- Neon database (atau database lain): https://neon.tech
- Repository di GitHub dengan kode aplikasi

## Part 1: Persiapan Database (Neon)

1. **Setup Neon Database** (jika belum):
   - Daftar di https://neon.tech
   - Buat project baru
   - Copy connection string (gunakan pooled connection untuk production)
   - Format: `postgresql://user:pass@ep-xxx-xxx-pooler.region.aws.neon.tech/dbname?sslmode=require`

2. **Test connection** (opsional):
   ```bash
   cd backend
   python test_database_connection.py
   ```

## Part 2: Deploy Backend ke Render

### 2.1 Connect GitHub Repository

1. **Login ke Render**: https://dashboard.render.com
2. Klik **New +** → **Web Service**
3. **Connect GitHub** (jika belum):
   - Klik "Connect GitHub"
   - Authorize Render
   - Pilih repository Anda

### 2.2 Configure Backend Service

1. **Repository**: Pilih repository GitHub Anda
2. **Name**: `review-insight-backend` (atau nama lain)
3. **Region**: Pilih yang terdekat (Singapore untuk Indonesia)
4. **Branch**: `main` atau `master`
5. **Root Directory**: `backend` (penting!)
6. **Runtime**: **Docker**
7. **Dockerfile Path**: `backend/Dockerfile` (atau `./Dockerfile` jika root directory sudah `backend`)
8. **Docker Context**: `backend`

### 2.3 Environment Variables

Tambahkan environment variables berikut:

```
DATABASE_URL=postgresql://user:pass@ep-xxx-xxx-pooler.region.aws.neon.tech/dbname?sslmode=require
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key
USE_GEMINI=true
USE_GROQ_KEY_POINTS=true
USE_HUGGINGFACE_KEY_POINTS=true
FLASK_ENV=production
ALLOWED_ORIGINS=https://your-frontend-url.onrender.com
```

**Penting**: 
- `DATABASE_URL`: Gunakan pooled connection dari Neon
- `ALLOWED_ORIGINS`: Setelah frontend deploy, update dengan URL frontend

### 2.4 Advanced Settings

- **Auto-Deploy**: Yes (auto-deploy dari GitHub)
- **Health Check Path**: `/api/health`
- **Plan**: Free (atau Starter jika perlu always-on)
- **Instance Type**: Free tier (512MB RAM) - cukup untuk 1 worker

**Note**: 
- Free tier menggunakan 1 worker untuk menghemat memory
- Torch + Transformers memakan banyak memory, jadi kita reduce workers
- Jika masih timeout, pertimbangkan upgrade ke Starter plan ($7/month)

### 2.5 Deploy

1. Klik **Create Web Service**
2. Render akan:
   - Build Docker image
   - Deploy container
   - Assign URL (contoh: `review-insight-backend.onrender.com`)

3. **Tunggu build selesai** (5-10 menit pertama kali)

### 2.6 Verify Backend

1. Test health endpoint:
   ```
   https://your-backend-url.onrender.com/api/health
   ```
   Seharusnya return: `{"status": "healthy"}`

2. **Copy backend URL** untuk digunakan di frontend

## Part 3: Deploy Frontend ke Render

### 3.1 Create Frontend Service

1. Klik **New +** → **Web Service**
2. **Repository**: Pilih repository yang sama
3. **Name**: `review-insight-frontend`
4. **Region**: Sama dengan backend
5. **Branch**: `main` atau `master`
6. **Root Directory**: `frontend`
7. **Runtime**: **Docker**
8. **Dockerfile Path**: `frontend/Dockerfile`
9. **Docker Context**: `frontend`

### 3.2 Environment Variables

Tambahkan:

```
VITE_API_URL=https://your-backend-url.onrender.com/api
```

**Penting**: Ganti `your-backend-url` dengan URL backend yang sudah dibuat di Part 2.

### 3.3 Advanced Settings

- **Auto-Deploy**: Yes
- **Health Check Path**: `/` (atau kosongkan)

### 3.4 Deploy

1. Klik **Create Web Service**
2. Tunggu build selesai
3. Frontend akan tersedia di: `review-insight-frontend.onrender.com`

## Part 4: Update CORS (Backend)

Setelah frontend deploy, update `ALLOWED_ORIGINS` di backend:

1. Buka backend service di Render dashboard
2. **Environment** tab
3. Update `ALLOWED_ORIGINS`:
   ```
   https://review-insight-frontend.onrender.com
   ```
4. **Save Changes** → Auto-redeploy

## Part 5: Setup Custom Domain (Optional)

### Backend

1. Buka backend service
2. **Settings** → **Custom Domain**
3. Add domain: `api.yourdomain.com`
4. Update DNS records sesuai instruksi Render

### Frontend

1. Buka frontend service
2. **Settings** → **Custom Domain**
3. Add domain: `yourdomain.com` atau `www.yourdomain.com`
4. Update DNS records

## Part 6: Using render.yaml (Alternative Method)

Jika ingin deploy dengan satu file konfigurasi:

1. **Commit `render.yaml`** ke repository
2. Di Render dashboard:
   - **New +** → **Blueprint**
   - Connect repository
   - Render akan auto-detect `render.yaml`
   - Review configuration
   - **Apply**

**Keuntungan**: Deploy backend dan frontend sekaligus dengan satu klik.

## Troubleshooting

### Build Fails

**Error: "Cannot find Dockerfile"**
- Pastikan `Root Directory` benar
- Check `Dockerfile Path` relative dari root directory

**Error: "Module not found"**
- Check `requirements.txt` lengkap
- Pastikan semua dependencies terinstall di Dockerfile

### Backend Issues

**Database Connection Error**
- Verify `DATABASE_URL` benar
- Pastikan menggunakan pooled connection untuk Neon
- Check SSL mode: `?sslmode=require`

**CORS Error**
- Update `ALLOWED_ORIGINS` dengan frontend URL
- Check backend logs di Render dashboard

**Port Error**
- Render menggunakan `$PORT` environment variable
- Pastikan Dockerfile menggunakan `${PORT:-5000}`

### Frontend Issues

**API Calls Fail**
- Verify `VITE_API_URL` benar
- Check browser console untuk errors
- Pastikan backend URL accessible

**Build Fails**
- Check build logs di Render
- Verify `package.json` dan dependencies
- Pastikan Node.js version compatible

### Performance

**Slow First Request**
- Normal untuk free tier (cold start)
- Render free tier sleep setelah 15 menit idle
- Upgrade ke paid plan untuk always-on

## Render Free Tier Limits

- **Web Services**: 
  - 750 hours/month (cukup untuk 1 service 24/7)
  - Sleep setelah 15 menit idle
  - 512MB RAM
- **Bandwidth**: 100GB/month
- **Build time**: Unlimited

**Note**: Untuk production dengan traffic tinggi, pertimbangkan upgrade.

## Monitoring

### View Logs

1. Buka service di Render dashboard
2. **Logs** tab
3. Real-time logs atau download

### Metrics

- **Metrics** tab untuk:
  - CPU usage
  - Memory usage
  - Request count
  - Response time

## Auto-Deploy

Render auto-deploy ketika:
- Push ke branch yang di-configure
- Manual trigger dari dashboard

**Disable auto-deploy**:
- Settings → **Auto-Deploy** → Disable

## Cost Estimate

- **Free Tier**: 
  - Backend: Free (dengan sleep)
  - Frontend: Free (dengan sleep)
  - Database: Neon free tier
  - **Total: $0/month**

- **Paid Tier** (jika perlu always-on):
  - Starter plan: $7/month per service
  - **Total: ~$14/month** (backend + frontend)

## Best Practices

1. **Environment Variables**: Jangan commit secrets ke Git
2. **Health Checks**: Setup health check path
3. **Logs**: Monitor logs regularly
4. **Backup**: Setup database backups (Neon auto-backup)
5. **Monitoring**: Setup alerts untuk errors
6. **Updates**: Keep dependencies updated

## Next Steps

1. ✅ Backend deployed
2. ✅ Frontend deployed
3. ✅ CORS configured
4. ✅ Test all features
5. ✅ Setup custom domain (optional)
6. ✅ Monitor logs and metrics

## Support

- Render Docs: https://render.com/docs
- Render Status: https://status.render.com
- Render Community: https://community.render.com

