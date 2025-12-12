"""
Test script untuk mengecek apakah Gemini API key valid dan bisa digunakan
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def test_gemini_api():
    print("=" * 60)
    print("TEST GEMINI API KEY")
    print("=" * 60)
    
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY tidak ditemukan di file .env")
        print("\nCara fix:")
        print("1. Buka file backend/.env")
        print("2. Tambahkan: GEMINI_API_KEY=your_api_key_here")
        print("3. Dapatkan API key dari: https://makersuite.google.com/app/apikey")
        return False
    
    print(f"✅ API Key ditemukan: {api_key[:10]}...{api_key[-5:]}")
    print(f"   Panjang: {len(api_key)} karakter")
    
    try:
        print("\n🔄 Mengkonfigurasi Gemini API...")
        genai.configure(api_key=api_key)
        print("✅ Konfigurasi berhasil")
        
        print("\n🔄 Mencoba list models yang tersedia...")
        models = genai.list_models()
        model_list = list(models)
        print(f"✅ Berhasil! Total {len(model_list)} models tersedia")
        
        print("\n📋 Models yang mendukung generateContent:")
        gemini_models = []
        for model in model_list:
            if 'generateContent' in model.supported_generation_methods:
                gemini_models.append(model.name)
                print(f"   - {model.name}")
        
        if not gemini_models:
            print("   ⚠️ Tidak ada model yang mendukung generateContent!")
            return False
        
        print(f"\n🔄 Mencoba menggunakan model: {gemini_models[0]}")
        model = genai.GenerativeModel(gemini_models[0].split('/')[-1])
        
        print("🔄 Mencoba generate content...")
        response = model.generate_content("Halo, ini test")
        
        if response and response.text:
            print(f"✅ SUCCESS! Response: {response.text[:50]}...")
            print("\n" + "=" * 60)
            print("✅ API KEY VALID DAN BERFUNGSI!")
            print("=" * 60)
            return True
        else:
            print("❌ ERROR: Tidak dapat generate content")
            return False
            
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ ERROR: {error_msg}")
        
        if "429" in error_msg or "quota" in error_msg.lower():
            print("\n⚠️ Mungkin masalah quota atau rate limit")
            print("   Cek: https://makersuite.google.com/app/apikey")
            print("   Pastikan quota masih tersedia")
        elif "403" in error_msg or "permission" in error_msg.lower():
            print("\n⚠️ Masalah permission")
            print("   Pastikan API key memiliki akses ke Gemini API")
            print("   Buat API key baru di: https://makersuite.google.com/app/apikey")
        elif "401" in error_msg or "invalid" in error_msg.lower():
            print("\n⚠️ API key tidak valid atau expired")
            print("   Buat API key baru di: https://makersuite.google.com/app/apikey")
            print("   Pastikan API key benar-benar di-copy dengan lengkap")
        else:
            print(f"\n⚠️ Error detail: {error_msg}")
            print("   Cek dokumentasi: https://ai.google.dev/gemini-api/docs")
        
        return False

if __name__ == '__main__':
    success = test_gemini_api()
    if not success:
        print("\n❌ API KEY TIDAK BERFUNGSI. Perbaiki masalah di atas.")
    else:
        print("\n✅ Semua test passed! API key siap digunakan.")


