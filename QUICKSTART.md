# 🚀 Quick Start Guide - 3Ts App

## ⚡ 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment
```bash
cp .env.example .env
# Edit .env and add your SARVAM_API_KEY
```

### 3. Run the Server
```bash
python main.py
```

Server starts at: `http://localhost:8000`

### 4. Test the API
In another terminal:
```bash
python test_client.py
```

## 📚 API Usage Examples

### Translate Text
```bash
curl -X POST "http://localhost:8000/translate?text=Hello&source_lang=en&target_lang=hi"
```

### Transliterate Text
```bash
curl -X POST "http://localhost:8000/transliterate?text=hello&source_script=en&target_script=hi"
```

### Interactive Documentation
Open browser: `http://localhost:8000/docs`

## 📁 Project Files

```
3ts-app/
├── main.py              ← FastAPI application (CORE)
├── test_client.py       ← Test the API
├── requirements.txt     ← Python dependencies
├── .env.example         ← Template for environment variables
├── Dockerfile           ← For Docker deployment
├── README.md            ← Full documentation
├── GITHUB_SETUP.md      ← How to push to GitHub
└── .gitignore          ← Files to ignore in Git
```

## 🔑 Key Features

✅ **Transcribe**: Audio → Text (via Sarvam AI)  
✅ **Translate**: Text → Different Language  
✅ **Transliterate**: Text → Different Script  
✅ **Production-Grade**: Error handling, async processing  
✅ **Well-Documented**: README, code comments  
✅ **API Docs**: Auto-generated Swagger UI  

## 🎯 For Interview Preparation

### What to Know
1. **Architecture**: FastAPI backend + Sarvam AI integration
2. **Key Challenges**: Handling async requests, API rate limiting, error management
3. **Scalability**: Can handle multiple concurrent requests

### During Interview
1. Run the server: `python main.py`
2. Open Swagger UI: http://localhost:8000/docs
3. Show working API endpoints
4. Walk through code (main.py)
5. Explain architecture decisions

### Talking Points
- "Built production-grade FastAPI backend"
- "Integrated with Sarvam AI REST APIs"
- "Implemented async/await for concurrent requests"
- "Proper error handling and validation"
- "Scalable architecture supporting 50+ language pairs"

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"
```bash
pip install -r requirements.txt
```

### "Connection refused" when testing
Make sure the server is running:
```bash
python main.py
```

### API returns 500 error
Check your `.env` file has the correct `SARVAM_API_KEY`

## 📤 Deploy to GitHub

```bash
git add .
git commit -m "Initial commit: 3Ts FastAPI application"
git remote add origin https://github.com/USERNAME/3ts-app.git
git branch -M main
git push -u origin main
```

See `GITHUB_SETUP.md` for detailed instructions.

## ✨ Next Steps

1. ✅ Test locally
2. ✅ Push to GitHub
3. ✅ Share link in resume: `https://github.com/USERNAME/3ts-app`
4. ✅ Practice explaining in interview
5. ✅ Deploy (optional): Use Docker or AWS

## 📞 Support

For issues:
1. Check README.md for detailed documentation
2. Review main.py for implementation details
3. Check test_client.py for usage examples

---

**You're all set!** The project is ready to showcase. 🎉
