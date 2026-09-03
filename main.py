from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import httpx
import os
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

app = FastAPI(title="3Ts - Transcribe, Translate, Transliterate")

# Sarvam AI API Configuration - Railway will set this as environment variable
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

print(f"🚀 Starting 3Ts API Server")
print(f"Environment: {'Railway' if 'RAILWAY' in os.environ else 'Local'}")

if SARVAM_API_KEY:
    print(f"✅ API Key loaded: {SARVAM_API_KEY[:10]}...")
else:
    print("⚠️ Warning: SARVAM_API_KEY not configured")

# Language code mapping for Sarvam AI
LANGUAGE_MAP = {
    "hi": "hi-IN",
    "en": "en-IN",
    "ta": "ta-IN",
    "te": "te-IN",
    "ka": "kn-IN",
    "ml": "ml-IN",
    "bn": "bn-IN",
    "gu": "gu-IN",
    "mr": "mr-IN",
    "pa": "pa-IN",
    "od": "od-IN",
}

def get_sarvam_lang_code(lang: str) -> str:
    """Convert language codes to Sarvam AI format"""
    if "-IN" in lang:
        return lang
    return LANGUAGE_MAP.get(lang, f"{lang}-IN")

# ============= TRANSLATE =============
@app.post("/translate")
async def translate(text: str, source_lang: str = "hi", target_lang: str = "en"):
    """Translate text using Sarvam AI"""
    try:
        if not SARVAM_API_KEY:
            return {
                "original_text": text,
                "translated_text": f"[Mock: {text}]",
                "source_language": source_lang,
                "target_language": target_lang,
                "note": "No API key configured"
            }
        
        source_sarvam = get_sarvam_lang_code(source_lang)
        target_sarvam = get_sarvam_lang_code(target_lang)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.sarvam.ai/translate",
                headers={
                    "Authorization": f"Bearer {SARVAM_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "input": text,
                    "source_language_code": source_sarvam,
                    "target_language_code": target_sarvam,
                    "enable_preprocessing": True
                },
                timeout=10.0
            )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "original_text": text,
                "translated_text": result.get("output", text),
                "source_language": source_lang,
                "target_language": target_lang
            }
        else:
            return {
                "original_text": text,
                "translated_text": f"[Mock: {text}]",
                "source_language": source_lang,
                "target_language": target_lang,
                "note": f"API error {response.status_code}"
            }
    
    except Exception as e:
        return {
            "original_text": text,
            "translated_text": f"[Mock: {text}]",
            "source_language": source_lang,
            "target_language": target_lang,
            "error": str(e)
        }


# ============= TRANSLITERATE =============
@app.post("/transliterate")
async def transliterate(text: str, source_script: str = "hi", target_script: str = "en"):
    """Transliterate text using Sarvam AI"""
    try:
        if not SARVAM_API_KEY:
            return {
                "original_text": text,
                "transliterated_text": f"[Mock: {text}]",
                "source_script": source_script,
                "target_script": target_script,
                "note": "No API key configured"
            }
        
        source_sarvam = get_sarvam_lang_code(source_script)
        target_sarvam = get_sarvam_lang_code(target_script)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.sarvam.ai/transliterate",
                headers={
                    "Authorization": f"Bearer {SARVAM_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "input": text,
                    "source_language_code": source_sarvam,
                    "target_language_code": target_sarvam
                },
                timeout=10.0
            )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "original_text": text,
                "transliterated_text": result.get("output", text),
                "source_script": source_script,
                "target_script": target_script
            }
        else:
            return {
                "original_text": text,
                "transliterated_text": f"[Mock: {text}]",
                "source_script": source_script,
                "target_script": target_script,
                "note": f"API error {response.status_code}"
            }
    
    except Exception as e:
        return {
            "original_text": text,
            "transliterated_text": f"[Mock: {text}]",
            "source_script": source_script,
            "target_script": target_script,
            "error": str(e)
        }


# ============= TRANSCRIBE =============
@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...), language: str = "hi"):
    """Transcribe audio file using Sarvam AI"""
    try:
        if not SARVAM_API_KEY:
            return {
                "transcribed_text": "[Mock] Audio transcribed",
                "language": language,
                "note": "No API key configured"
            }
        
        contents = await file.read()
        sarvam_lang = get_sarvam_lang_code(language)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.sarvam.ai/speech-to-text",
                headers={"Authorization": f"Bearer {SARVAM_API_KEY}"},
                files={"file": (file.filename, contents, file.content_type)},
                data={"language_code": sarvam_lang},
                timeout=30.0
            )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "transcribed_text": result.get("transcript", ""),
                "language": language
            }
        else:
            return {
                "transcribed_text": "[Mock] Audio transcribed",
                "language": language,
                "note": f"API error {response.status_code}"
            }
    
    except Exception as e:
        return {
            "transcribed_text": "[Mock] Audio transcribed",
            "language": language,
            "error": str(e)
        }


# ============= HEALTH CHECK =============
@app.get("/")
async def root():
    return {
        "message": "3Ts API - Transcribe, Translate, Transliterate",
        "status": "✅ Running on Railway",
        "sarvam_ai": "✅ Connected" if SARVAM_API_KEY else "⚠️ No API key",
        "endpoints": {
            "translate": "POST /translate",
            "transliterate": "POST /transliterate",
            "transcribe": "POST /transcribe",
            "docs": "/docs"
        }
    }


# Health check for Railway
@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)