# Fix Vercel Deployment Error

## Common Vercel Deployment Errors untuk Vite Apps

### Error 1: "Build Command Failed" atau "Module Not Found"

**Penyebab:**
- Root directory tidak benar
- Build command salah
- Dependencies tidak ter-install

**Solusi:**

1. **Check Project Settings di Vercel:**
   - **Root Directory**: `frontend` (bukan root project)
   - **Framework Preset**: `Vite` (auto-detect)
   - **Build Command**: `npm run build` (atau `cd frontend && npm run build` jika root directory adalah root project)
   - **Output Directory**: `dist`
   - **Install Command**: `npm install` (atau `cd frontend && npm install`)

2. **Jika Root Directory adalah Root Project:**
   - Build Command: `cd frontend && npm run build`
   - Install Command: `cd frontend && npm install`
   - Output Directory: `frontend/dist`

### Error 2: "Cannot find module" atau Import Error

**Penyebab:**
- Path alias `@` tidak ter-resolve
- Dependencies tidak ter-install

**Solusi:**

1. **Check `vite.config.js`:**
   ```javascript
   resolve: {
     alias: {
       "@": path.resolve(__dirname, "./src"),
     },
   }
   ```

2. **Check `jsconfig.json` atau `tsconfig.json`:**
   ```json
   {
     "compilerOptions": {
       "baseUrl": ".",
       "paths": {
         "@/*": ["./src/*"]
       }
     }
   }
   ```

### Error 3: "Build Output Not Found"

**Penyebab:**
- Output directory salah
- Build tidak menghasilkan output

**Solusi:**

1. **Check `vite.config.js`:**
   ```javascript
   build: {
     outDir: 'dist',
   }
   ```

2. **Check Vercel Settings:**
   - Output Directory: `dist` (jika root directory adalah `frontend`)
   - Output Directory: `frontend/dist` (jika root directory adalah root project)

### Error 4: "Environment Variable Not Found"

**Penyebab:**
- Environment variable tidak di-set
- Variable tidak ter-inject saat build

**Solusi:**

1. **Set Environment Variable di Vercel:**
   - Settings → Environment Variables
   - Add: `VITE_API_URL` = `https://your-backend.onrender.com/api`
   - Environment: Production, Preview, Development

2. **Redeploy setelah set env var**

### Error 5: "Build Timeout"

**Penyebab:**
- Build terlalu lama
- Dependencies terlalu besar

**Solusi:**

1. **Optimize Dependencies:**
   - Remove unused dependencies
   - Use `npm ci` instead of `npm install` (faster, more reliable)

2. **Check Build Logs:**
   - Identify slow steps
   - Optimize build process

## Recommended Vercel Configuration

### Option 1: Root Directory = `frontend` (Recommended)

**Vercel Settings:**
- **Root Directory**: `frontend`
- **Framework Preset**: `Vite` (auto-detect)
- **Build Command**: `npm run build` (default)
- **Output Directory**: `dist` (default)
- **Install Command**: `npm install` (default)

**No `vercel.json` needed** - Vercel will auto-detect Vite!

### Option 2: Root Directory = Root Project

**Vercel Settings:**
- **Root Directory**: (empty, root project)
- **Framework Preset**: `Other`
- **Build Command**: `cd frontend && npm run build`
- **Output Directory**: `frontend/dist`
- **Install Command**: `cd frontend && npm install`

**Or use `vercel.json` in root:**
```json
{
  "buildCommand": "cd frontend && npm run build",
  "outputDirectory": "frontend/dist",
  "installCommand": "cd frontend && npm install"
}
```

## Step-by-Step Fix

### 1. Check Current Configuration

1. Buka Vercel Dashboard
2. Pilih project
3. Settings → General
4. Check:
   - Root Directory
   - Build Command
   - Output Directory
   - Install Command

### 2. Update Configuration

**Recommended Settings (Root Directory = `frontend`):**

```
Root Directory: frontend
Framework Preset: Vite
Build Command: npm run build
Output Directory: dist
Install Command: npm install
Node.js Version: 18.x (or latest)
```

### 3. Set Environment Variables

1. Settings → Environment Variables
2. Add:
   ```
   VITE_API_URL=https://review-insight-backend.onrender.com/api
   ```
3. Environment: All (Production, Preview, Development)

### 4. Delete vercel.json (if exists in frontend)

Vercel modern auto-detects Vite, so `vercel.json` might cause conflicts.

**If you need `vercel.json`, use this minimal version:**
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

### 5. Redeploy

1. Deployments tab
2. Click "..." on latest deployment
3. Redeploy
4. Or push new commit to trigger auto-deploy

## Quick Fix Checklist

- [ ] Root Directory set to `frontend`
- [ ] Framework Preset: `Vite`
- [ ] Build Command: `npm run build`
- [ ] Output Directory: `dist`
- [ ] Install Command: `npm install`
- [ ] Environment Variables set (`VITE_API_URL`)
- [ ] `vercel.json` minimal or removed
- [ ] `package.json` has `build` script
- [ ] `vite.config.js` exists and correct
- [ ] No build errors in logs

## Test Locally Before Deploy

```bash
cd frontend
npm install
npm run build
npm run preview
```

If local build works, Vercel should work too!

## Still Having Issues?

1. **Check Build Logs:**
   - Vercel Dashboard → Deployments → Click deployment → View Build Logs
   - Look for specific error messages

2. **Check Dependencies:**
   - Ensure all dependencies are in `package.json`
   - No missing peer dependencies

3. **Check Node Version:**
   - Vercel Settings → Node.js Version
   - Use 18.x or latest LTS

4. **Clear Cache:**
   - Vercel Dashboard → Settings → General
   - Clear Build Cache
   - Redeploy

