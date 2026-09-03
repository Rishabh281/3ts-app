import requests
import json

BASE_URL = "http://localhost:8000"

def test_translate():
    """Test translation endpoint"""
    print("\nTesting translation...")
    payload = {
        "text": "नमस्ते दुनिया",
        "source_lang": "hi",
        "target_lang": "en"
    }
    response = requests.post(f"{BASE_URL}/translate", params=payload)
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_transliterate():
    """Test transliteration endpoint"""
    print("\nTesting transliteration...")
    payload = {
        "text": "नमस्ते",
        "source_script": "hi",
        "target_script": "en"
    }
    response = requests.post(f"{BASE_URL}/transliterate", params=payload)
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_transcribe():
    """Test transcription endpoint with audio file"""
    print("\nTesting transcription...")
    print("(Note: Requires an audio file)")
    # This would require an actual audio file
    print("Upload an audio file to test this endpoint")


def test_health():
    """Test health endpoint"""
    print("\nTesting health check...")
    response = requests.get(BASE_URL)
    print(f"Response: {json.dumps(response.json(), indent=2)}")


if __name__ == "__main__":
    print("=" * 50)
    print("3Ts API - Test Client")
    print("=" * 50)
    
    try:
        test_health()
        test_translate()
        test_transliterate()
        test_transcribe()
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to API")
        print("Make sure the server is running: python main.py")
