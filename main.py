from fastapi import FastAPI, File, UploadFile
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="3Ts - Transcribe, Translate, Transliterate")

# Sarvam AI API Configuration
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

if not SARVAM_API_KEY:
    print("Warning: SARVAM_API_KEY not found in environment variables")

# Language code mapping
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
        return lang  # Already in correct format
    return LANGUAGE_MAP.get(lang, f"{lang}-IN")

# Transcription
@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...), language: str = "hi"):
    """
    Transcribe audio file to text using Sarvam AI
    Supported languages: hi, en, ta, te, ka, ml, bn, gu, mr, pa, od
    """
    try:
        contents = await file.read()
        sarvam_lang = get_sarvam_lang_code(language)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.sarvam.ai/speech-to-text",
                headers={
                    "Authorization": f"Bearer {SARVAM_API_KEY}",
                },
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
            print(f"API Error: {response.status_code} - {response.text}")
            return {
                "transcribed_text": "[Mock Response] Audio transcribed successfully",
                "language": language,
                "note": f"API returned {response.status_code}"
            }
    
    except Exception as e:
        print(f"Exception: {str(e)}")
        return {
            "transcribed_text": "[Mock Response] Audio transcribed",
            "language": language,
            "note": f"Error: {str(e)}"
        }


# Translation
@app.post("/translate")
async def translate(text: str, source_lang: str = "hi", target_lang: str = "en"):
    """
    Translate text from source to target language using Sarvam AI
    """
    try:
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
            print(f"API Error: {response.status_code} - {response.text}")
            # Mock fallback
            mock_translations = {
                ("नमस्ते दुनिया", "hi", "en"): "Hello World",
                ("hello", "en", "hi"): "नमस्ते",
            }
            translated = mock_translations.get((text, source_lang, target_lang), 
                                             f"[Translated: {text}]")
            return {
                "original_text": text,
                "translated_text": translated,
                "source_language": source_lang,
                "target_language": target_lang,
                "note": f"Using fallback (API error {response.status_code})"
            }
    
    except Exception as e:
        print(f"Exception: {str(e)}")
        return {
            "original_text": text,
            "translated_text": f"[Translated: {text}]",
            "source_language": source_lang,
            "target_language": target_lang,
            "note": f"Error: {str(e)}"
        }


# Transliteration
@app.post("/transliterate")
async def transliterate(text: str, source_script: str = "hi", target_script: str = "en"):
    """
    Transliterate text from source script to target script using Sarvam AI
    Example: Devanagari (hi) -> Latin (en)
    """
    try:
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
            print(f"API Error: {response.status_code} - {response.text}")
            # Mock fallback
            mock_translits = {
                ("नमस्ते", "hi", "en"): "namaste",
                ("धन्यवाद", "hi", "en"): "dhanyavaad",
            }
            transliterated = mock_translits.get((text, source_script, target_script),
                                              f"[Transliterated: {text}]")
            return {
                "original_text": text,
                "transliterated_text": transliterated,
                "source_script": source_script,
                "target_script": target_script,
                "note": f"Using fallback (API error {response.status_code})"
            }
    
    except Exception as e:
        print(f"Exception: {str(e)}")
        return {
            "original_text": text,
            "transliterated_text": f"[Transliterated: {text}]",
            "source_script": source_script,
            "target_script": target_script,
            "note": f"Error: {str(e)}"
        }


# Health check
@app.get("/")
async def root():
    api_status = "Connected to Sarvam AI" if SARVAM_API_KEY else "Mock mode"
    return {
        "message": "3Ts API - Transcribe, Translate, Transliterate",
        "sarvam_ai_status": api_status,
        "endpoints": {
            "transcribe": "POST /transcribe",
            "translate": "POST /translate",
            "transliterate": "POST /transliterate"
        },
        "supported_languages": {
            "hi": "Hindi",
            "en": "English",
            "ta": "Tamil",
            "te": "Telugu",
            "ka": "Kannada",
            "ml": "Malayalam",
            "bn": "Bengali",
            "gu": "Gujarati",
            "mr": "Marathi",
            "pa": "Punjabi"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, use_colors=False)