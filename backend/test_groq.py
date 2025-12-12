"""
Test script untuk Groq API
"""
import os
from dotenv import load_dotenv
import requests

load_dotenv()

def test_groq():
    """Test Groq API connection and key points extraction"""
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("❌ GROQ_API_KEY tidak ditemukan di .env")
        print("💡 Tambahkan GROQ_API_KEY ke file backend/.env")
        return False
    
    print(f"✅ GROQ_API_KEY ditemukan (panjang: {len(api_key)} karakter)")
    
    # Test API call
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    test_text = "Produk ini sangat bagus! Kualitas bahan sangat baik dan awet. Harga juga terjangkau. Pengiriman cepat sekali. Recommended!"
    
    prompt = f"""Ekstrak poin-poin penting dari review produk ini. 
Buat daftar poin utama dalam format bullet-point yang ringkas.
Fokus pada aspek penting seperti kualitas produk, fitur, layanan pelanggan, nilai, dll.

Review: {test_text}

Poin Penting:"""
    
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "Anda adalah asisten yang membantu mengekstrak poin penting dari review produk."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200,
        "temperature": 0.3
    }
    
    print("\n🔄 Menguji koneksi ke Groq API...")
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('choices') and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print("✅ Groq API berhasil!")
                print("\n📝 Hasil ekstraksi:")
                print("-" * 50)
                print(content)
                print("-" * 50)
                return True
            else:
                print(f"❌ Response tidak valid: {result}")
                return False
        elif response.status_code == 401:
            print("❌ API key tidak valid atau tidak memiliki akses")
            print("💡 Pastikan API key benar dan aktif di: https://console.groq.com/")
            return False
        elif response.status_code == 429:
            print("⚠️ Quota habis (429)")
            print("💡 Groq free tier: 14,400 requests/hari. Tunggu reset atau cek quota di console")
            return False
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout - koneksi terlalu lama")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - cek koneksi internet")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Test Groq API")
    print("=" * 60)
    test_groq()
    print("\n" + "=" * 60)

