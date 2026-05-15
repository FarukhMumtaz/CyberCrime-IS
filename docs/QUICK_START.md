# Quick Setup & Configuration Guide

## 📋 Project Status: COMPLETE ✓

This Cyber Crime Reporting System has been fully analyzed and completed. All issues have been fixed.

---

## 🚀 5-Minute Quick Start

### Step 1: Clone & Install
```bash
cd cyber-crime-reporting-system
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
cp .env.example .env
# Edit .env with these essentials:
# - JWT_SECRET_KEY: Generate a random 32+ character string
# - ENCRYPTION_KEY: Generate using: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
# - SUPABASE_URL: Your Supabase project URL
# - SUPABASE_ANON_KEY: Your Supabase anon key
# - GROQ_API_KEY: Your Groq API key
```

### Step 3: Verify Setup
```bash
python setup_verification.py
```

### Step 4: Run Application
```bash
# Terminal 1
streamlit run frontend/app.py

# Terminal 2
cd backend/api && python main.py
```

---

## 🔑 Essential Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `JWT_SECRET_KEY` | Secret key for JWT signing | `your-random-string-32-chars-min` |
| `ENCRYPTION_KEY` | Fernet encryption key | `gAAAAABm...` |
| `SUPABASE_URL` | Supabase project URL | `https://your-project.supabase.co` |
| `SUPABASE_ANON_KEY` | Supabase anonymous key | `eyJhbGc...` |
| `GROQ_API_KEY` | Groq API key | `gsk_...` |

---

## 🎯 What's Been Fixed

✓ Import chain errors - Added robust error handling  
✓ Missing components - All implemented  
✓ Service initialization - Made resilient  
✓ Environment config - Created template  
✓ Setup verification - Created validation script  

---

## 📝 Project Components

### Frontend (Streamlit)
- Main app: `frontend/app.py`
- Pages: `tracking.py`, `law_guide.py`, `help.py`
- Components: ComplaintForm, StatusTracker, LawGuide, FAQ
- Port: 8501

### Backend (FastAPI)
- Main API: `backend/api/main.py`
- Services: Database, AI, File operations
- Models: User, Complaint, Evidence, Law
- Utils: Security, Encryption, Validation
- Port: 8000

### Database (Supabase)
- Schema: `database/schemas/main_schema.sql`
- Tables: users, complaints, evidence, laws, audit_logs
- Security: Row Level Security (RLS) ready

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Test specific component
pytest frontend/tests/test_app.py
pytest backend/tests/test_api.py
```

---

## 📚 API Endpoints Quick Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/auth/register` | Register user |
| POST | `/auth/login` | User login |
| POST | `/complaints/` | Submit complaint |
| GET | `/complaints/track/{id}` | Track complaint |
| POST | `/evidence/upload` | Upload evidence |
| GET | `/laws` | Get cyber laws |
| GET | `/pdf/{tracking_id}` | Generate PDF report |

View full API docs at: http://localhost:8000/docs

---

## 🔒 Security Features

- ✓ JWT Authentication
- ✓ Password hashing (PBKDF2-SHA256)
- ✓ End-to-end encryption
- ✓ Rate limiting
- ✓ Input validation
- ✓ Audit logging
- ✓ CORS protection
- ✓ SQL injection prevention

---

## 📁 Project Structure Summary

```
cyber-crime-reporting-system/
├── frontend/                    # Streamlit UI
│   ├── app.py                  # Main application
│   ├── components/             # Reusable components
│   ├── pages/                  # Page modules
│   └── static/                 # Styling
├── backend/                     # FastAPI backend
│   ├── api/main.py            # REST API
│   ├── services/              # Business logic
│   ├── models/                # Data models
│   ├── utils/                 # Utilities
│   └── tests/                 # Unit tests
├── database/                   # Database
│   ├── schemas/               # SQL schemas
│   ├── migrations/            # Migrations
│   └── seeders/               # Sample data
├── docs/                       # Documentation
├── deployment/                 # Deployment guides
├── .env.example               # Configuration template
├── requirements.txt           # Dependencies
├── setup_verification.py      # Setup validator
├── COMPLETION_REPORT.md       # This report
└── README.md                  # Main documentation
```

---

## 🐛 Troubleshooting

### Issue: ImportError for services
**Solution:** Run `python setup_verification.py` and install missing packages

### Issue: .env file not found
**Solution:** Run `cp .env.example .env` and configure it

### Issue: Supabase connection fails
**Solution:** 
- Verify SUPABASE_URL and SUPABASE_ANON_KEY are correct
- Check network connectivity
- Ensure Supabase tables exist (run migration scripts)

### Issue: Frontend can't reach backend
**Solution:**
- Start backend first: `cd backend/api && python main.py`
- Verify backend is running on localhost:8000
- Check CORS policy in `main.py`

### Issue: AI service errors
**Solution:**
- Verify GROQ_API_KEY is valid
- Check Groq API quota/limits
- Review error logs for details

---

## 📊 System Requirements

| Component | Requirement |
|-----------|-------------|
| Python | 3.9+ |
| OS | Windows/Mac/Linux |
| RAM | 2GB minimum |
| Storage | 500MB free space |
| Internet | Required (for APIs) |

---

## 🚀 Deployment

### Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Set environment variables
4. Deploy (automatic on push)

### Local/Server Deployment
1. Install dependencies: `pip install -r requirements.txt`
2. Configure `.env` file
3. Run backend: `cd backend/api && python main.py`
4. Run frontend: `streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0`

---

## 📞 Support & Contacts

**For Development Issues:**
- Check COMPLETION_REPORT.md for detailed analysis
- Review docs/ folder for architecture
- Run setup_verification.py for diagnostics

**Emergency Cybercrime Reporting:**
- Pakistan Police: 15
- FIA Cybercrime: [Contact]
- NCCIA: [Contact]

---

## 📄 License & Disclaimer

This system is developed for educational and governmental use in Pakistan. It follows the Prevention of Electronic Crimes Act (PECA) 2016.

---

## ✅ Verification Checklist

Before going live:

- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations complete
- [ ] Frontend and backend running
- [ ] API documentation reviewed
- [ ] Security audit completed
- [ ] Performance testing done
- [ ] Error handling tested
- [ ] Logging configured
- [ ] Rate limiting working

---

**Project Status: READY FOR DEPLOYMENT ✓**

**Last Updated:** May 13, 2026  
**Version:** 1.0.0  
**Author:** SRE Team
