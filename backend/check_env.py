"""
Script untuk mengecek apakah file .env bisa dibaca dengan benar
"""
import os
import sys

# Try to import dotenv
try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    print("⚠️ python-dotenv tidak terinstall. Install dengan: pip install python-dotenv")
    HAS_DOTENV = False
    def load_dotenv():
        pass

print("=" * 60)
print("CEK FILE .ENV")
print("=" * 60)

# Cek apakah file .env ada
env_path = os.path.join(os.path.dirname(__file__), '.env')
print(f"\n1. Cek file .env:")
print(f"   Path: {env_path}")
print(f"   File exists: {os.path.exists(env_path)}")

if os.path.exists(env_path):
    print(f"   File size: {os.path.getsize(env_path)} bytes")
    print(f"\n2. Isi file .env (tanpa menampilkan API key lengkap):")
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    if 'API_KEY' in line or 'PASSWORD' in line:
                        # Hide sensitive info
                        parts = line.split('=')
                        if len(parts) == 2:
                            key = parts[0].strip()
                            value = parts[1].strip()
                            if value:
                                print(f"   Line {i}: {key}={value[:10]}...{value[-5:] if len(value) > 15 else '***'}")
                            else:
                                print(f"   Line {i}: {key}= (KOSONG!)")
                        else:
                            print(f"   Line {i}: {line[:50]}...")
                    else:
                        print(f"   Line {i}: {line}")
    except Exception as e:
        print(f"   ❌ Error membaca file: {e}")

print(f"\n3. Load .env dengan python-dotenv:")
if HAS_DOTENV:
    load_dotenv()
    print("   ✅ python-dotenv tersedia")
else:
    print("   ⚠️ python-dotenv tidak tersedia, membaca file manual")
    # Manual read .env file
    if os.path.exists(env_path):
        env_vars = {}
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
        os.environ.update(env_vars)

print(f"\n4. Cek environment variables:")
gemini_key = os.getenv('GEMINI_API_KEY')
database_url = os.getenv('DATABASE_URL')

if gemini_key:
    print(f"   ✅ GEMINI_API_KEY ditemukan!")
    print(f"      Panjang: {len(gemini_key)} karakter")
    print(f"      Preview: {gemini_key[:10]}...{gemini_key[-5:]}")
    print(f"      Ada spasi di awal: {gemini_key[0] == ' ' if gemini_key else 'N/A'}")
    print(f"      Ada spasi di akhir: {gemini_key[-1] == ' ' if gemini_key else 'N/A'}")
    has_quote = gemini_key.startswith('"') or gemini_key.startswith("'")
    print(f"      Ada tanda kutip: {has_quote}")
else:
    print(f"   ❌ GEMINI_API_KEY TIDAK DITEMUKAN!")
    print(f"      Pastikan file .env berisi: GEMINI_API_KEY=your_key_here")

if database_url:
    print(f"   ✅ DATABASE_URL ditemukan!")
    print(f"      Preview: {database_url[:30]}...")
else:
    print(f"   ⚠️ DATABASE_URL tidak ditemukan (akan menggunakan default)")

print(f"\n5. Rekomendasi:")
if not gemini_key:
    print(f"   ❌ MASALAH: GEMINI_API_KEY tidak ditemukan")
    print(f"   ✅ SOLUSI:")
    print(f"      1. Pastikan file .env ada di folder: {os.path.dirname(env_path)}")
    print(f"      2. Format harus: GEMINI_API_KEY=your_key_here")
    print(f"      3. TANPA tanda kutip, TANPA spasi sebelum/sesudah =")
    print(f"      4. Contoh: GEMINI_API_KEY=AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz")
    print(f"      5. Restart server setelah edit .env")
else:
    if gemini_key.startswith('"') or gemini_key.startswith("'"):
        print(f"   ⚠️ PERINGATAN: API key diawali tanda kutip!")
        print(f"      Hapus tanda kutip dari file .env")
    if gemini_key.startswith(' ') or gemini_key.endswith(' '):
        print(f"   ⚠️ PERINGATAN: API key ada spasi di awal/akhir!")
        print(f"      Hapus spasi dari file .env")
    if len(gemini_key) < 20:
        print(f"   ⚠️ PERINGATAN: API key terlalu pendek (mungkin tidak lengkap)")
    if 'your' in gemini_key.lower() or 'here' in gemini_key.lower():
        print(f"   ❌ ERROR: API key masih placeholder!")
        print(f"      Ganti dengan API key yang sebenarnya")

print("\n" + "=" * 60)

