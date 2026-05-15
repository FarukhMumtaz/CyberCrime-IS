# Installation & Configuration Checklist

**Project:** Cyber Crime Reporting System  
**Date:** May 13, 2026  
**Status:** Ready for Setup

---

## ✅ Pre-Installation Requirements

- [ ] Python 3.9 or higher installed
- [ ] pip package manager working
- [ ] Git installed (for version control)
- [ ] Internet connection (for API access)
- [ ] Text editor or IDE (VS Code recommended)
- [ ] Administrator access (for installations)

### Verify Prerequisites
```bash
python --version          # Should show 3.9+
pip --version            # Should show version info
git --version            # Should show version info
```

---

## ✅ Step 1: Clone & Setup Environment

### 1.1 Navigate to Project
```bash
cd "d:\4th Semester\Software Requirement Engineering\cyber-crime-reporting-system"
```
- [ ] Directory exists
- [ ] Can access all subdirectories

### 1.2 Create Virtual Environment
```bash
python -m venv venv
```
- [ ] venv/ folder created
- [ ] Activation scripts present

### 1.3 Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```
- [ ] Prompt shows (venv)
- [ ] pip points to venv location

### 1.4 Verify Installation
```bash
python -m pip install --upgrade pip
```
- [ ] pip upgraded successfully

---

## ✅ Step 2: Install Dependencies

### 2.1 Install Required Packages
```bash
pip install -r requirements.txt
```
- [ ] Installation completes without errors
- [ ] No "not found" or "failed" messages

### 2.2 Verify Critical Packages
```bash
pip list | grep -E "streamlit|fastapi|supabase|cryptography|groq"
```
- [ ] streamlit installed
- [ ] fastapi installed
- [ ] supabase installed
- [ ] cryptography installed
- [ ] groq installed

---

## ✅ Step 3: Environment Configuration

### 3.1 Create Environment File
```bash
cp .env.example .env
```
- [ ] .env file created
- [ ] Contains all required variables
- [ ] Not tracked by git (.gitignore includes .env)

### 3.2 Generate Required Keys

#### 3.2.1 Generate JWT Secret Key
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
- [ ] Copy output
- [ ] Paste into JWT_SECRET_KEY in .env

#### 3.2.2 Generate Encryption Key
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```
- [ ] Copy output
- [ ] Paste into ENCRYPTION_KEY in .env

### 3.3 Configure Supabase
- [ ] Create Supabase account (supabase.com)
- [ ] Create new project
- [ ] Copy Project URL → paste into SUPABASE_URL
- [ ] Copy Anon Key → paste into SUPABASE_ANON_KEY
- [ ] Copy Service Role Key → paste into SUPABASE_SERVICE_KEY

### 3.4 Configure Groq API
- [ ] Create Groq account (groq.com)
- [ ] Generate API key
- [ ] Paste into GROQ_API_KEY

### 3.5 Review .env File
```bash
# Check .env has all required values (not placeholders)
cat .env | grep -E "URL|KEY|GROQ|SECRET|ENCRYPTION"
```
- [ ] JWT_SECRET_KEY has value
- [ ] ENCRYPTION_KEY has value
- [ ] SUPABASE_URL has value
- [ ] SUPABASE_ANON_KEY has value
- [ ] SUPABASE_SERVICE_KEY has value
- [ ] GROQ_API_KEY has value

---

## ✅ Step 4: Database Setup

### 4.1 Create Database Tables
1. Go to Supabase Dashboard
2. Navigate to SQL Editor
3. [ ] Run database/schemas/main_schema.sql
4. [ ] Tables created successfully:
   - [ ] users
   - [ ] complaints
   - [ ] evidence
   - [ ] laws
   - [ ] audit_logs

### 4.2 Run Initial Migration
1. In Supabase SQL Editor
2. [ ] Run database/migrations/001_initial_setup.sql
3. [ ] No errors reported

### 4.3 (Optional) Seed Sample Data
1. In Supabase SQL Editor
2. [ ] Run database/seeders/cyber_laws.sql
3. [ ] Sample laws added to database

### 4.4 Enable Row Level Security
In Supabase Dashboard:
- [ ] Go to Authentication settings
- [ ] Enable RLS on users table
- [ ] Enable RLS on complaints table
- [ ] Enable RLS on evidence table

---

## ✅ Step 5: Verify Installation

### 5.1 Run Verification Script
```bash
python setup_verification.py
```
- [ ] Python Version - PASS ✓
- [ ] Project Structure - PASS ✓
- [ ] Imports - PASS ✓
- [ ] Environment Variables - PASS ✓
- [ ] Database Files - PASS ✓
- [ ] All checks pass

### 5.2 Manual Verification
```bash
# Test Python imports
python -c "import streamlit; print('Streamlit OK')"
python -c "import fastapi; print('FastAPI OK')"
python -c "import supabase; print('Supabase OK')"
```
- [ ] All imports successful

---

## ✅ Step 6: Run Application

### 6.1 Start Backend API
```bash
cd backend/api
python main.py
# or: uvicorn main:app --reload
```
- [ ] Server starts successfully
- [ ] No error messages
- [ ] Listening on http://localhost:8000
- [ ] Wait until you see "Uvicorn running on..."

### 6.2 Start Frontend (New Terminal)
```bash
# New terminal window, keep backend running
streamlit run frontend/app.py
```
- [ ] Frontend compiles successfully
- [ ] Browser opens automatically
- [ ] Listening on http://localhost:8501
- [ ] "You can now view your Streamlit app in your browser"

### 6.3 Test Application Connectivity
1. Open Frontend: http://localhost:8501
   - [ ] Page loads without errors
   - [ ] Navigation sidebar visible
   - [ ] Styling applied correctly

2. Check Backend: http://localhost:8000/docs
   - [ ] Swagger UI loads
   - [ ] All endpoints listed
   - [ ] Can expand endpoints

3. Test Frontend-Backend Connection
   - Go to "Report Cybercrime" page
   - Fill out form partially
   - [ ] No connection errors
   - [ ] Form accepts input

---

## ✅ Step 7: Functionality Testing

### 7.1 Test Registration (if implemented)
- [ ] Navigate to registration endpoint
- [ ] Create test account
- [ ] Account saved to database
- [ ] Password properly hashed

### 7.2 Test Complaint Submission
- [ ] Fill complaint form
- [ ] Submit complaint
- [ ] Tracking ID generated
- [ ] Displayed to user
- [ ] Saved to database

### 7.3 Test Complaint Tracking
- [ ] Use tracking ID from submission
- [ ] Navigate to tracking page
- [ ] Enter tracking ID
- [ ] Status retrieves correctly

### 7.4 Test Law Guide
- [ ] Navigate to Law Guide
- [ ] Search functionality works
- [ ] Filters work correctly
- [ ] Laws display properly

### 7.5 Test Evidence Upload (if enabled)
- [ ] Select file for upload
- [ ] File validates correctly
- [ ] Encryption/security works
- [ ] File stored securely

---

## ✅ Step 8: Security Verification

### 8.1 Check Encryption
```bash
# Verify encryption key is loaded
grep "ENCRYPTION_KEY" .env
```
- [ ] Key is present
- [ ] Key is not placeholder

### 8.2 Check JWT Token
```bash
# In Python
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
secret = os.getenv('JWT_SECRET_KEY')
print(f'JWT Secret: {secret[:20]}...')
"
```
- [ ] Secret key loaded
- [ ] Key is not placeholder

### 8.3 Test API Authentication
1. Call API without auth:
   ```bash
   curl http://localhost:8000/protected-endpoint
   ```
   - [ ] Returns 401 Unauthorized (expected)

2. Call API with mock token:
   ```bash
   curl -H "Authorization: Bearer invalid-token" \
        http://localhost:8000/protected-endpoint
   ```
   - [ ] Returns 401 Unauthorized (expected)

---

## ✅ Step 9: Run Tests

### 9.1 Run All Tests
```bash
pytest
```
- [ ] All tests pass
- [ ] No failed tests
- [ ] No errors reported

### 9.2 Run Frontend Tests
```bash
pytest frontend/tests/
```
- [ ] Frontend tests pass
- [ ] All components tested

### 9.3 Run Backend Tests
```bash
pytest backend/tests/
```
- [ ] API endpoints tested
- [ ] Service methods tested
- [ ] Database operations tested

---

## ✅ Step 10: Preparation for Deployment

### 10.1 Final Checks
- [ ] All tests passing
- [ ] No error messages in logs
- [ ] Application responds correctly
- [ ] Database connectivity verified
- [ ] API endpoints working
- [ ] Frontend rendering correctly
- [ ] Security features active
- [ ] Environment variables configured

### 10.2 Review Documentation
- [ ] README.md reviewed
- [ ] API docs reviewed
- [ ] Architecture doc reviewed
- [ ] Security practices understood

### 10.3 Performance Check
- [ ] Application starts in < 10 seconds
- [ ] Page loads in < 3 seconds
- [ ] API responses in < 1 second
- [ ] Database queries optimized

### 10.4 Backup Configuration
- [ ] .env file backed up securely
- [ ] Database backup created
- [ ] Configuration documented
- [ ] Secrets stored safely

---

## 📋 Troubleshooting Checklist

### If Application Won't Start

1. **Python Issues**
   - [ ] Python version is 3.9+
   - [ ] Virtual environment activated
   - [ ] pip upgraded

2. **Dependency Issues**
   - [ ] All packages installed: `pip install -r requirements.txt`
   - [ ] No conflicts: `pip check`
   - [ ] Correct versions: `pip list`

3. **Environment Issues**
   - [ ] .env file exists
   - [ ] All required variables set
   - [ ] No syntax errors in .env
   - [ ] Keys are valid (not placeholders)

4. **Connection Issues**
   - [ ] Internet connection available
   - [ ] Supabase project accessible
   - [ ] Groq API key valid
   - [ ] Firewall allows connections

### If Database Won't Connect

1. **Check Supabase**
   - [ ] Project created
   - [ ] Database running
   - [ ] Tables created
   - [ ] URL is correct

2. **Check Credentials**
   - [ ] SUPABASE_URL correct
   - [ ] SUPABASE_ANON_KEY correct
   - [ ] Key is not revoked

3. **Check Network**
   - [ ] Internet connection stable
   - [ ] No firewall blocking connections
   - [ ] No VPN issues

### If Imports Fail

1. **Check Installation**
   - [ ] Run: `pip install -r requirements.txt`
   - [ ] Run: `pip check`

2. **Check Paths**
   - [ ] Files in correct locations
   - [ ] No circular imports
   - [ ] __init__.py files present

3. **Check Versions**
   - [ ] Compatible package versions
   - [ ] Python version compatible

---

## 📞 Support Resources

### Documentation
- [README.md](README.md) - Main documentation
- [COMPLETION_REPORT.md](COMPLETION_REPORT.md) - Detailed analysis
- [QUICK_START.md](QUICK_START.md) - Quick reference
- [FILES_STATUS.md](FILES_STATUS.md) - File status

### External Resources
- [Streamlit Docs](https://docs.streamlit.io)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Supabase Docs](https://supabase.com/docs)
- [Groq Docs](https://console.groq.com/docs)

### Emergency Contacts
- Python Support: python.org
- Project Issues: Check documentation
- Emergency Reporting: Pakistan Police (15)

---

## ✅ Final Verification

### Completion Checklist
- [ ] All prerequisites met
- [ ] Installation completed
- [ ] Configuration done
- [ ] Database set up
- [ ] Tests passing
- [ ] Application running
- [ ] All functionality tested
- [ ] Deployment ready

### When All Checked:
1. Document any customizations
2. Backup configuration
3. Create deployment plan
4. Ready for production

---

**Installation Status: ✓ READY TO PROCEED**

Once all items are checked, your system is ready for deployment.

For next steps, see COMPLETION_REPORT.md or QUICK_START.md

---

**Last Updated:** May 13, 2026  
**Checklist Version:** 1.0  
**Prepared By:** SRE Team
