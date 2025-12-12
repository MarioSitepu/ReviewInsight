# Setup Database dengan Neon

Panduan lengkap untuk setup database menggunakan Neon (Serverless PostgreSQL).

## Apa itu Neon?

Neon adalah serverless PostgreSQL yang:
- ✅ **Gratis** untuk development (512MB storage, unlimited projects)
- ✅ **Auto-scaling** - tidak perlu manage server
- ✅ **Branching** - bisa buat database branches seperti Git
- ✅ **Instant setup** - setup dalam hitungan detik
- ✅ **Connection pooling** - built-in connection pooling

## Langkah Setup

### 1. Daftar di Neon

1. Kunjungi https://neon.tech
2. Klik **Sign Up** (bisa pakai GitHub, Google, atau email)
3. Verifikasi email jika diperlukan

### 2. Buat Project Baru

1. Setelah login, klik **Create Project**
2. Isi informasi:
   - **Project name**: `review-insight` (atau nama lain)
   - **Region**: Pilih yang terdekat (Singapore untuk Indonesia)
   - **PostgreSQL version**: 15 atau 16 (recommended)
3. Klik **Create Project**

### 3. Dapatkan Connection String

1. Setelah project dibuat, Anda akan melihat dashboard
2. Di bagian **Connection Details**, ada beberapa opsi:
   - **Connection string** (untuk development)
   - **Pooled connection** (untuk production, recommended)

3. **Copy connection string** yang sesuai:
   ```
   postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
   ```

   Atau untuk pooled connection (recommended):
   ```
   postgresql://username:password@ep-xxx-xxx-pooler.region.aws.neon.tech/dbname?sslmode=require
   ```

### 4. Setup di Aplikasi

#### Untuk Development (Local)

1. **Backend `.env` file:**
   ```env
   DATABASE_URL=postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
   GEMINI_API_KEY=your_gemini_api_key
   FLASK_ENV=development
   ```

2. **Test connection:**
   ```bash
   cd backend
   python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database connected!')"
   ```

#### Untuk Production (PythonAnywhere)

1. **Upload `.env` ke PythonAnywhere:**
   ```env
   DATABASE_URL=postgresql://username:password@ep-xxx-xxx-pooler.region.aws.neon.tech/dbname?sslmode=require
   GEMINI_API_KEY=your_gemini_api_key
   FLASK_ENV=production
   ```

2. **Gunakan pooled connection** untuk production (lebih efisien)

#### Untuk Docker

1. **Update `docker-compose.yml` atau `.env`:**
   ```env
   DATABASE_URL=postgresql://username:password@ep-xxx-xxx-pooler.region.aws.neon.tech/dbname?sslmode=require
   ```

2. **Hapus service postgres** dari docker-compose.yml (tidak perlu lagi)

### 5. Create Database Tables

Setelah connection string di-set, jalankan:

```bash
cd backend
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Tables created!')"
```

Atau jika menggunakan PythonAnywhere:
```python
# Di PythonAnywhere console
from app import app, db
with app.app_context():
    db.create_all()
    print("Tables created!")
```

## Keuntungan Neon vs Local PostgreSQL

| Feature | Neon | Local PostgreSQL |
|---------|------|------------------|
| Setup | Instant | Perlu install & config |
| Maintenance | Zero | Perlu manage sendiri |
| Scaling | Auto | Manual |
| Backup | Automatic | Manual setup |
| Cost | Free tier available | Free (self-hosted) |
| Access | From anywhere | Local only |
| Branching | ✅ Yes | ❌ No |

## Neon Free Tier Limits

- **Storage**: 512MB (cukup untuk development)
- **Projects**: Unlimited
- **Branches**: Unlimited
- **Compute time**: 0.5 vCPU hours/day
- **Data transfer**: 5GB/month

**Note**: Untuk production dengan traffic tinggi, pertimbangkan upgrade ke paid plan.

## Connection String Format

### Standard Connection
```
postgresql://username:password@hostname/dbname?sslmode=require
```

### Pooled Connection (Recommended for Production)
```
postgresql://username:password@hostname-pooler.region.aws.neon.tech/dbname?sslmode=require
```

**Perbedaan:**
- **Standard**: Direct connection, lebih cepat tapi limited connections
- **Pooled**: Connection pooling, lebih efisien untuk production, handle lebih banyak concurrent connections

## Troubleshooting

### Connection Error: "SSL required"

**Solusi**: Pastikan connection string include `?sslmode=require`

```env
# ✅ Correct
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require

# ❌ Wrong
DATABASE_URL=postgresql://user:pass@host/db
```

### Connection Timeout

**Solusi**: 
1. Check internet connection
2. Verify connection string benar
3. Check Neon dashboard untuk status project
4. Pastikan IP tidak di-block (Neon allow all IPs by default)

### "Database does not exist"

**Solusi**: 
1. Neon auto-create database dengan nama project
2. Atau create manual di Neon dashboard
3. Update connection string dengan database name yang benar

### "Too many connections"

**Solusi**: 
1. Gunakan **pooled connection** untuk production
2. Close connections properly di code
3. Check connection pooling settings

## Best Practices

1. **Development**: Gunakan standard connection
2. **Production**: Gunakan pooled connection
3. **Environment Variables**: Jangan commit connection string ke Git
4. **Backup**: Neon auto-backup, tapi bisa export manual jika perlu
5. **Monitoring**: Check Neon dashboard untuk usage & performance

## Migration dari Local PostgreSQL

Jika sudah punya data di local PostgreSQL:

1. **Export data:**
   ```bash
   pg_dump -U postgres review_analyzer > backup.sql
   ```

2. **Import ke Neon:**
   ```bash
   psql "postgresql://user:pass@neon-host/dbname?sslmode=require" < backup.sql
   ```

3. **Update connection string** di aplikasi

## Resources

- Neon Documentation: https://neon.tech/docs
- Neon Dashboard: https://console.neon.tech
- Connection Guide: https://neon.tech/docs/connect/connect-from-any-app
- Pricing: https://neon.tech/pricing

## Support

- Neon Discord: https://discord.gg/neondatabase
- Neon Docs: https://neon.tech/docs
- GitHub Issues: Check project repository

