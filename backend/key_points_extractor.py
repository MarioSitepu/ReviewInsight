import google.generativeai as genai
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def extract_key_points_simple(text):
    """
    Smart key points extraction without AI (when Gemini quota is exhausted).
    Uses pattern matching and keyword extraction to identify important points.
    """
    import re
    
    # Clean text
    text = text.strip()
    if not text:
        return "Tidak ada teks untuk dianalisis"
    
    # Split into sentences (handle multiple delimiters)
    sentences = re.split(r'[.!?]\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Comprehensive keyword categories
    positive_keywords = [
        'bagus', 'baik', 'excellent', 'sempurna', 'perfect', 'menakjubkan', 'amazing',
        'recommended', 'rekomendasi', 'puas', 'satisfied', 'senang', 'happy',
        'worth', 'layak', 'value', 'nilai', 'mantap', 'top', 'terbaik', 'best',
        'cepat', 'fast', 'efisien', 'efficient', 'mudah', 'easy', 'simple'
    ]
    
    negative_keywords = [
        'buruk', 'jelek', 'bad', 'disappointed', 'kecewa', 'tidak puas', 'unsatisfied',
        'lambat', 'slow', 'rusak', 'broken', 'cacat', 'defect', 'masalah', 'problem',
        'mahal', 'expensive', 'overpriced', 'tidak layak', 'not worth', 'waste',
        'menyesal', 'regret', 'tidak recommended', 'tidak rekomendasi', 'weird', 'strange', 'aneh'
    ]
    
    quality_keywords = [
        'kualitas', 'quality', 'bahan', 'material', 'build', 'konstruksi',
        'awet', 'durable', 'tahan lama', 'long lasting', 'sturdy', 'kokoh'
    ]
    
    feature_keywords = [
        'fitur', 'feature', 'fungsi', 'function', 'spesifikasi', 'spec',
        'desain', 'design', 'tampilan', 'appearance', 'warna', 'color'
    ]
    
    service_keywords = [
        'pengiriman', 'shipping', 'delivery', 'pelayanan', 'service', 'customer service',
        'packaging', 'kemasan', 'garansi', 'warranty', 'support', 'dukungan'
    ]
    
    price_keywords = [
        'harga', 'price', 'biaya', 'cost', 'murah', 'cheap', 'affordable', 'terjangkau',
        'mahal', 'expensive', 'worth', 'layak', 'value', 'nilai', 'budget'
    ]
    
    all_keywords = positive_keywords + negative_keywords + quality_keywords + feature_keywords + service_keywords + price_keywords
    
    # Extract key points
    key_points = []
    seen_sentences = set()  # Avoid duplicates
    
    # Priority 1: Sentences with important keywords
    for sentence in sentences:
        if len(sentence) < 15:  # Skip very short sentences
            continue
            
        sentence_lower = sentence.lower()
        
        # Check for important keywords
        found_keywords = []
        for keyword in all_keywords:
            if keyword.lower() in sentence_lower:
                found_keywords.append(keyword)
        
        if found_keywords:
            # Analyze and categorize the sentence with more context
            category = ""
            analysis = ""
            
            if any(kw in sentence_lower for kw in quality_keywords):
                category = "[KUALITAS]"
                if any(kw in sentence_lower for kw in negative_keywords):
                    analysis = f"Masalah kualitas produk: {sentence}"
                elif any(kw in sentence_lower for kw in positive_keywords):
                    analysis = f"Kualitas produk dinilai baik: {sentence}"
                else:
                    analysis = f"Aspek kualitas: {sentence}"
            elif any(kw in sentence_lower for kw in ['bau', 'smell', 'aroma', 'wangi', 'busuk']):
                category = "[KUALITAS BAU & RASA]"
                if any(kw in sentence_lower for kw in ['aneh', 'tidak enak', 'busuk', 'weird', 'bad', 'tidak normal']):
                    analysis = f"Masalah bau dan rasa: Produk memiliki bau yang tidak normal dan/atau rasa yang tidak enak, mengindikasikan masalah kualitas atau kesegaran produk"
                else:
                    analysis = f"Aspek bau dan rasa: {sentence}"
            elif any(kw in sentence_lower for kw in ['rasa', 'taste', 'enak', 'dimakan', 'diminum']):
                category = "[KUALITAS RASA]"
                if any(kw in sentence_lower for kw in negative_keywords):
                    analysis = f"Masalah rasa: Produk memiliki rasa yang tidak memuaskan, mempengaruhi pengalaman konsumsi"
                else:
                    analysis = f"Aspek rasa: {sentence}"
            elif any(kw in sentence_lower for kw in service_keywords):
                category = "[LAYANAN]"
                analysis = f"Aspek layanan: {sentence}"
            elif any(kw in sentence_lower for kw in price_keywords):
                category = "[HARGA]"
                analysis = f"Aspek harga: {sentence}"
            elif any(kw in sentence_lower for kw in feature_keywords):
                category = "[FITUR]"
                analysis = f"Aspek fitur: {sentence}"
            elif any(kw in sentence_lower for kw in negative_keywords):
                category = "[KUALITAS]"
                # Analyze negative feedback more deeply
                if 'jelek' in sentence_lower or 'buruk' in sentence_lower or 'bad' in sentence_lower:
                    analysis = f"Kualitas produk dinilai buruk oleh pengguna, menunjukkan ketidakpuasan terhadap produk"
                elif 'aneh' in sentence_lower or 'weird' in sentence_lower:
                    analysis = f"Produk memiliki karakteristik yang tidak normal atau mencurigakan"
                else:
                    analysis = f"Umpan balik negatif: {sentence}"
            elif any(kw in sentence_lower for kw in positive_keywords):
                category = "[KUALITAS]"
                analysis = f"Umpan balik positif: {sentence}"
            else:
                category = "[INFORMASI]"
                analysis = sentence
            
            if analysis and sentence not in seen_sentences:
                key_points.append(f"{category}: {analysis}")
                seen_sentences.add(sentence)
    
    # Priority 2: If not enough key points, add meaningful sentences
    if len(key_points) < 3:
        for sentence in sentences:
            if len(sentence) > 30 and sentence not in seen_sentences:
                # Check if sentence seems important (has numbers, specific terms, etc.)
                if any(char.isdigit() for char in sentence) or len(sentence) > 50:
                    key_points.append(f"• {sentence}")
                    seen_sentences.add(sentence)
                    if len(key_points) >= 5:
                        break
    
    # Format output
    if key_points:
        result = "\n".join(key_points[:5])  # Max 5 key points
        return result
    else:
        # For very short reviews, extract what we can
        if len(text.strip()) < 50:
            # Try to extract sentiment and key words from short text
            text_lower = text.lower()
            short_points = []
            
            # Analyze short reviews more intelligently
            if any(word in text_lower for word in ['bau', 'smell', 'aroma']) and any(word in text_lower for word in ['aneh', 'tidak enak', 'busuk', 'weird']):
                short_points.append("[KUALITAS BAU & RASA]: Produk memiliki bau yang tidak normal, mengindikasikan masalah kualitas atau kesegaran produk")
            elif any(word in text_lower for word in ['jelek', 'buruk', 'bad', 'terrible']):
                short_points.append("[KUALITAS]: Produk dinilai buruk oleh pengguna, menunjukkan ketidakpuasan terhadap kualitas produk")
            elif any(word in text_lower for word in ['bagus', 'baik', 'good', 'great', 'excellent', 'mantap']):
                short_points.append("[KUALITAS]: Produk dinilai baik oleh pengguna")
            
            # Check for specific aspects with better analysis
            if any(word in text_lower for word in ['harga', 'price', 'murah', 'mahal', 'cheap', 'expensive']):
                if any(word in text_lower for word in ['mahal', 'expensive', 'overpriced']):
                    short_points.append("[HARGA]: Harga produk dinilai terlalu mahal atau tidak sebanding dengan kualitas")
                elif any(word in text_lower for word in ['murah', 'cheap', 'affordable']):
                    short_points.append("[HARGA]: Harga produk dinilai terjangkau atau sesuai")
                else:
                    short_points.append("[HARGA]: Menyebutkan aspek harga produk")
            
            if any(word in text_lower for word in ['kualitas', 'quality', 'bahan', 'material']):
                short_points.append("[KUALITAS]: Menyebutkan aspek kualitas atau bahan produk")
            
            if any(word in text_lower for word in ['pengiriman', 'delivery', 'shipping']):
                if any(word in text_lower for word in ['cepat', 'fast']):
                    short_points.append("[LAYANAN]: Pengiriman cepat dan memuaskan")
                elif any(word in text_lower for word in ['lambat', 'slow']):
                    short_points.append("[LAYANAN]: Pengiriman lambat, mempengaruhi kepuasan pelanggan")
                else:
                    short_points.append("[LAYANAN]: Menyebutkan aspek pengiriman")
            
            if short_points:
                return "\n".join(short_points)
            else:
                # Analyze the text more intelligently
                if len(text.strip()) > 5:
                    # Try to provide some analysis even for very short reviews
                    if any(word in text_lower for word in ['aneh', 'weird', 'tidak enak']):
                        return "[KUALITAS]: Produk memiliki karakteristik yang tidak normal atau tidak memuaskan"
                    else:
                        return f"[INFORMASI]: {text.strip()}"
                return f"• {text.strip()}"
        
        # Last resort: return first meaningful sentences with better formatting
        meaningful = [s for s in sentences if len(s) > 20][:3]
        if meaningful:
            formatted_points = []
            for s in meaningful:
                # Try to categorize
                s_lower = s.lower()
                if any(kw in s_lower for kw in ['bau', 'smell', 'aroma', 'rasa', 'taste']):
                    formatted_points.append(f"[KUALITAS BAU & RASA]: {s}")
                elif any(kw in s_lower for kw in negative_keywords):
                    formatted_points.append(f"[KUALITAS]: {s}")
                elif any(kw in s_lower for kw in positive_keywords):
                    formatted_points.append(f"[KUALITAS]: {s}")
                else:
                    formatted_points.append(f"[INFORMASI]: {s}")
            return "\n".join(formatted_points)
        return "Tidak ada poin penting yang dapat diekstrak dari review ini"


def extract_key_points_groq(text):
    """
    Extract key points using Groq API (FREE - 14,400 requests/day).
    Very fast GPU-accelerated inference.
    """
    try:
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY tidak dikonfigurasi")
        
        # Groq API endpoint
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Improved prompt - multilingual support (Indonesian & English)
        if len(text.strip()) < 20:
            # For short reviews, analyze and provide insights
            prompt = f"""Review produk: "{text}"

Analisis review di atas dan ekstrak poin penting dengan cara yang informatif dan terstruktur. Jangan hanya mengulang kata-kata dari review, tapi berikan analisis yang lebih mendalam tentang aspek yang disebutkan.

Format output:
• [Aspek]: [Analisis/Insight yang lebih detail]

Contoh:
- Review: "jelek oi"
- Output: • [Kualitas]: Produk dinilai buruk oleh pengguna, menunjukkan ketidakpuasan terhadap kualitas produk

Jawab dalam bahasa yang sama dengan review (Indonesia atau Inggris)."""
        else:
            # For longer reviews, use detailed analytical prompt
            prompt = f"""Review produk: "{text}"

Analisis review di atas dan ekstrak poin penting dengan cara yang informatif dan terstruktur. Jangan hanya mengulang kata-kata dari review secara literal, tapi berikan analisis yang lebih mendalam.

Untuk setiap poin penting yang ditemukan:
1. Identifikasi aspek yang dibahas (kualitas, rasa, bau, harga, pengiriman, dll)
2. Berikan analisis atau insight tentang aspek tersebut
3. Jika ada masalah spesifik, jelaskan dampaknya

Format output (maksimal 3-5 poin):
• [Aspek]: [Analisis detail tentang aspek tersebut]

Contoh:
- Review: "baunya aneh, tidak enak dimulut ketika dimakan"
- Output: 
• [Kualitas Rasa & Bau]: Produk memiliki bau yang tidak normal dan rasa yang tidak enak saat dikonsumsi, mengindikasikan masalah kualitas atau kesegaran produk
• [Pengalaman Pengguna]: Pengalaman konsumsi produk negatif, kemungkinan mempengaruhi kepuasan pelanggan

Jawab dalam bahasa yang sama dengan review (Indonesia atau Inggris). Jangan hanya mengulang kata-kata dari review, tapi berikan analisis yang lebih mendalam."""
        
        data = {
            "model": "llama-3.1-8b-instant",  # Free tier model
            "messages": [
                {"role": "system", "content": "You are an expert product review analyst. Your task is to extract and analyze key points from product reviews in a structured and informative way. Do NOT simply repeat the words from the review. Instead, provide deeper analysis and insights about the aspects mentioned. Format each point as: • [Aspect]: [Detailed analysis/insight]. Always respond in the same language as the review (Indonesian or English). Provide 2-4 key points with meaningful analysis."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 200,
            "temperature": 0.1  # Lower temperature for more focused and accurate output
        }
        
        print("[INFO] Menggunakan Groq API...")
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('choices') and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content'].strip()
                
                # Validate response - if it contains apology or says it can't see, use fallback
                # Check in both Indonesian and English
                invalid_phrases = [
                    "maaf", "saya tidak dapat", "tidak dapat melihat", 
                    "silakan", "berikan review", "tuliskan review", "saya tidak bisa",
                    "sorry", "i cannot", "i can't", "cannot see", "please provide",
                    "please give", "i don't see", "i do not see", "unable to see"
                ]
                if any(phrase in content.lower() for phrase in invalid_phrases):
                    print("[WARNING] Groq menghasilkan response tidak valid, menggunakan ekstraksi cerdas")
                    raise ValueError("Response tidak valid dari Groq")
                
                # Filter out irrelevant points and English translations
                # Check for phrases that indicate something is NOT mentioned
                irrelevant_phrases = [
                    "tidak ada komentar", "tidak disebutkan", "tidak ada", "no comment",
                    "not mentioned", "not discussed", "nothing about", "no mention",
                    "tidak ada informasi", "no information"
                ]
                
                # Remove English translations in parentheses (e.g., "Harga mahal (High price)")
                import re
                # Remove everything in parentheses (including nested)
                content = re.sub(r'\([^()]*\)', '', content)
                # Also remove any remaining English text patterns
                content = re.sub(r'\s*\([^)]*\)', '', content)  # Remove any remaining parentheses
                # Clean up multiple spaces
                content = re.sub(r'\s+', ' ', content).strip()
                
                # Split content into lines and filter out irrelevant ones
                lines = content.split('\n')
                filtered_lines = []
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    line_lower = line.lower()
                    # Skip lines that say something is not mentioned
                    if not any(phrase in line_lower for phrase in irrelevant_phrases):
                        # Remove any remaining English translations
                        line = re.sub(r'\s*\([^)]*\)', '', line).strip()
                        if line:
                            filtered_lines.append(line)
                
                if filtered_lines:
                    content = '\n'.join(filtered_lines).strip()
                    if len(content) < 10:
                        print("[WARNING] Setelah filter, response terlalu pendek, menggunakan ekstraksi cerdas")
                        raise ValueError("Response terlalu pendek setelah filter")
                else:
                    print("[WARNING] Semua poin tidak relevan, menggunakan ekstraksi cerdas")
                    raise ValueError("Semua poin tidak relevan")
                
                # If response is too short or seems incomplete, try to enhance it
                if len(content) < 10:
                    print("[WARNING] Response Groq terlalu pendek, menggunakan ekstraksi cerdas")
                    raise ValueError("Response terlalu pendek")
                
                print("[SUCCESS] Groq API berhasil")
                return content
            else:
                raise Exception("Response tidak valid dari Groq API")
        elif response.status_code == 429:
            raise Exception("Groq API quota habis")
        else:
            raise Exception(f"Groq API error: {response.status_code} - {response.text[:100]}")
            
    except Exception as e:
        error_msg = str(e)
        if "quota" in error_msg.lower() or "429" in error_msg:
            print(f"[WARNING] Groq quota habis: {error_msg[:100]}")
        else:
            print(f"[WARNING] Groq API error: {error_msg[:100]}")
        raise


def extract_key_points_huggingface(text):
    """
    Extract key points using Hugging Face Inference API (FREE - 30,000 requests/month).
    Uses summarization model.
    """
    try:
        api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not api_key:
            raise ValueError("HUGGINGFACE_API_KEY tidak dikonfigurasi")
        
        # Use Facebook BART for summarization
        model = "facebook/bart-large-cnn"
        url = f"https://api-inference.huggingface.co/models/{model}"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        # For key points, we'll use summarization with max_length
        payload = {
            "inputs": f"Ekstrak poin penting dari review ini: {text}",
            "parameters": {
                "max_length": 150,
                "min_length": 50,
                "do_sample": False
            }
        }
        
        print("[INFO] Menggunakan Hugging Face API...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                summary = result[0].get('summary_text', '')
                print("[SUCCESS] Hugging Face API berhasil")
                return summary.strip()
            elif isinstance(result, dict) and 'summary_text' in result:
                print("[SUCCESS] Hugging Face API berhasil")
                return result['summary_text'].strip()
            else:
                raise Exception("Response tidak valid dari Hugging Face API")
        elif response.status_code == 503:
            # Model is loading, wait a bit
            raise Exception("Model sedang loading, coba lagi dalam beberapa detik")
        elif response.status_code == 429:
            raise Exception("Hugging Face API quota habis")
        else:
            raise Exception(f"Hugging Face API error: {response.status_code} - {str(result)[:100]}")
            
    except Exception as e:
        error_msg = str(e)
        if "quota" in error_msg.lower() or "429" in error_msg:
            print(f"[WARNING] Hugging Face quota habis: {error_msg[:100]}")
        else:
            print(f"[WARNING] Hugging Face API error: {error_msg[:100]}")
        raise


def extract_key_points(text):
    """
    Extract key points from review text.
    Tries multiple AI providers in order:
    1. Groq (if configured) - 14,400/day free
    2. Hugging Face (if configured) - 30,000/month free
    3. Gemini (if configured) - 20/day free
    4. Smart extraction (always works, no quota)
    
    Returns: String containing key points
    """
    # Priority order: Groq > Hugging Face > Gemini > Smart Extraction
    
    # Try Groq first (best free tier)
    if os.getenv('GROQ_API_KEY'):
        try:
            use_groq = os.getenv('USE_GROQ_KEY_POINTS', 'true').lower() == 'true'
            if use_groq:
                return extract_key_points_groq(text)
        except Exception as e:
            print(f"[WARNING] Groq gagal, mencoba alternatif: {str(e)[:50]}")
    
    # Try Hugging Face second
    if os.getenv('HUGGINGFACE_API_KEY'):
        try:
            use_hf = os.getenv('USE_HUGGINGFACE_KEY_POINTS', 'true').lower() == 'true'
            if use_hf:
                return extract_key_points_huggingface(text)
        except Exception as e:
            print(f"[WARNING] Hugging Face gagal, mencoba alternatif: {str(e)[:50]}")
    
    # Try Gemini third (lowest priority due to small quota)
    use_gemini = os.getenv('USE_GEMINI', 'true').lower() == 'true'
    
    if use_gemini:
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            try:
                genai.configure(api_key=api_key)
                
                # First, try to list available models to see what's accessible
                try:
                    print("[INFO] Mencari model Gemini yang tersedia...")
                    available_models = genai.list_models()
                    model_names = [m.name for m in available_models if 'generateContent' in m.supported_generation_methods]
                    print(f"[SUCCESS] Model yang tersedia: {len(model_names)} models")
                    
                    # Try multiple models in order of preference (to avoid quota issues)
                    # Free tier has 20 requests/day per model, so try different models
                    models_to_try = [
                        'gemini-pro-latest',  # Most stable
                        'gemini-2.5-flash-lite',  # Lighter model
                        'gemini-flash-lite-latest',  # Alternative
                        'gemini-2.0-flash-lite',  # Another option
                        'gemini-2.5-flash',  # If others fail
                    ]
                    
                    model = None
                    used_model = None
                    
                    for model_name_attempt in models_to_try:
                        # Check if model exists in available models
                        full_model_name = f"models/{model_name_attempt}"
                        model_exists = full_model_name in model_names or model_name_attempt in [m.split('/')[-1] for m in model_names]
                        
                        if model_exists:
                            try:
                                print(f"[INFO] Mencoba model: {model_name_attempt}...")
                                model = genai.GenerativeModel(model_name_attempt)
                                used_model = model_name_attempt
                                print(f"[SUCCESS] Model siap digunakan: {model_name_attempt}")
                                break
                            except Exception as e:
                                error_str = str(e)
                                if "429" in error_str or "quota" in error_str.lower():
                                    print(f"[WARNING] Model {model_name_attempt} quota habis, mencoba model lain...")
                                    continue
                                else:
                                    # Other error, try next model
                                    print(f"[WARNING] Model {model_name_attempt} error: {error_str[:50]}...")
                                    continue
                    
                    # If all preferred models failed, try any available model
                    if model is None:
                        print("[WARNING] Semua model preferred quota habis, mencoba model lain...")
                        for model_name in model_names[:10]:  # Try first 10 available models
                            model_short = model_name.split('/')[-1]
                            if model_short not in [m.split('/')[-1] for m in models_to_try]:
                                try:
                                    print(f"[INFO] Mencoba model: {model_short}...")
                                    model = genai.GenerativeModel(model_short)
                                    used_model = model_short
                                    print(f"[SUCCESS] Menggunakan model: {model_short}")
                                    break
                                except Exception as e:
                                    if "429" not in str(e):
                                        continue
                        
                        if model is None:
                            raise Exception("Semua model Gemini quota habis. Tunggu beberapa saat atau gunakan fallback sederhana.")
                except Exception as list_error:
                    print(f"[WARNING] Tidak bisa list models, mencoba model default: {str(list_error)[:100]}")
                    # Fallback: try common model names
                    models_to_try = [
                        'gemini-pro',
                        'models/gemini-pro', 
                    ]
                    
                    model = None
                    for model_name_attempt in models_to_try:
                        try:
                            print(f"[INFO] Mencoba model: {model_name_attempt}...")
                            model = genai.GenerativeModel(model_name_attempt)
                            print(f"[SUCCESS] Model berhasil dimuat: {model_name_attempt}")
                            break
                        except Exception as e:
                            print(f"[WARNING] Model {model_name_attempt} tidak tersedia")
                            continue
                    
                    if model is None:
                        raise Exception("Tidak ada model Gemini yang tersedia. Pastikan API key valid dan memiliki akses ke Gemini API")
                
                if model is None:
                    raise Exception("Tidak ada model yang tersedia")
                
                prompt = f"""Analisis review produk berikut dan ekstrak poin penting dengan cara yang informatif dan terstruktur. Jangan hanya mengulang kata-kata dari review, tapi berikan analisis yang lebih mendalam tentang aspek yang disebutkan.

Review: {text}

Untuk setiap poin penting:
1. Identifikasi aspek yang dibahas (kualitas, rasa, bau, harga, pengiriman, dll)
2. Berikan analisis atau insight tentang aspek tersebut
3. Jika ada masalah spesifik, jelaskan dampaknya

Format output (maksimal 3-5 poin):
• [Aspek]: [Analisis detail tentang aspek tersebut]

Contoh format:
• [KUALITAS BAU & RASA]: Produk memiliki bau yang tidak normal dan rasa yang tidak enak saat dikonsumsi, mengindikasikan masalah kualitas atau kesegaran produk
• [PENGALAMAN PENGGUNA]: Pengalaman konsumsi produk negatif, kemungkinan mempengaruhi kepuasan pelanggan

Poin Penting:"""
                
                try:
                    response = model.generate_content(prompt)
                    
                    if response and response.text:
                        return response.text.strip()
                    else:
                        return "Tidak dapat mengekstrak poin penting"
                except Exception as gen_error:
                    error_str = str(gen_error)
                    if "429" in error_str or "quota" in error_str.lower() or "exceeded" in error_str.lower():
                        # Quota habis saat generate, gunakan smart extraction
                        print(f"[WARNING] Quota habis saat generate, menggunakan ekstraksi cerdas")
                        return extract_key_points_simple(text)
                    else:
                        raise gen_error
            except Exception as e:
                error_msg = str(e)
                print(f"[ERROR] Error ekstraksi poin penting: {error_msg}")
                
                # More user-friendly error messages with detailed troubleshooting
                if "404" in error_msg or "not found" in error_msg.lower():
                    return f"Model Gemini tidak ditemukan. Error detail: {error_msg[:200]}"
                elif "403" in error_msg or "permission" in error_msg.lower() or "forbidden" in error_msg.lower():
                    return f"API key tidak memiliki izin. Error: {error_msg[:200]}. Pastikan API key valid dan Gemini API diaktifkan."
                elif "429" in error_msg or "quota" in error_msg.lower() or "resource exhausted" in error_msg.lower() or "exceeded" in error_msg.lower():
                    # Quota exceeded - use smart extraction fallback
                    print(f"[WARNING] Quota Gemini API habis (429), menggunakan ekstraksi cerdas sebagai fallback")
                    print(f"          Error detail: {error_msg[:200]}")
                    smart_result = extract_key_points_simple(text)
                    # Return clean result without warning message (since it's working fine)
                    return smart_result
                elif "invalid" in error_msg.lower() or "401" in error_msg:
                    return f"API key tidak valid atau expired. Error: {error_msg[:200]}. Buat API key baru di: https://makersuite.google.com/app/apikey"
                else:
                    # Return more detailed error for debugging
                    print(f"[WARNING] Gemini error, menggunakan ekstraksi cerdas: {error_msg[:100]}")
                    # Fall through to smart extraction
    
    # Final fallback: Smart extraction (always works)
    print("[INFO] Semua AI provider tidak tersedia, menggunakan ekstraksi cerdas")
    return extract_key_points_simple(text)

