# 📊 System Diagrams & Architecture Documentation

**Cyber Crime Reporting System - Pakistan**  
**Comprehensive Visual Guide to System Architecture & Workflows**

---

## 📋 Table of Contents

1. [System Architecture (3-Layer)](#system-architecture)
2. [User Roles & Actors](#user-roles)
3. [Use Cases & Features](#use-cases)
4. [Data Flow Diagram](#data-flow)
5. [Citizen Complaint Workflow](#citizen-workflow)
6. [Officer Case Management Workflow](#officer-workflow)
7. [System Component Diagram](#components)
8. [Database Schema Overview](#database-schema)
9. [Deployment Architecture](#deployment)
10. [Security Architecture](#security)

---

## 🏗️ System Architecture (3-Layer)

### Overview
```
┌─────────────────────────────────────────────────────┐
│             PRESENTATION LAYER                      │
│  ┌─────────────────────────────────────────────┐   │
│  │  Streamlit Frontend (Citizen & Officer UI) │   │
│  │  - Report Form Page                         │   │
│  │  - Officer Login & Dashboard                │   │
│  │  - Law Guide & Tracking                     │   │
│  │  - Chat Bot & Help                          │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
                      ⬇️ HTTP/REST
┌─────────────────────────────────────────────────────┐
│             APPLICATION LAYER                       │
│  ┌────────────────────────────────────────────┐    │
│  │    FastAPI Backend Services                │    │
│  │  ┌──────────────────────────────────────┐  │    │
│  │  │ Services                             │  │    │
│  │  │ - Database Service (CRUD)            │  │    │
│  │  │ - File Service (Upload/Download)     │  │    │
│  │  │ - AI Service (Groq Integration)      │  │    │
│  │  │ - Email Service (Notifications)      │  │    │
│  │  │ - Security Service (Encryption)      │  │    │
│  │  └──────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
                      ⬇️ PostgreSQL
┌─────────────────────────────────────────────────────┐
│             DATA LAYER                              │
│  ┌────────────────────────────────────────────┐    │
│  │    Supabase (PostgreSQL + Storage)         │    │
│  │  ┌──────────────────────────────────────┐  │    │
│  │  │ Databases                            │  │    │
│  │  │ - Users (citizens & officers)        │  │    │
│  │  │ - Complaints                         │  │    │
│  │  │ - Evidence (encrypted files)         │  │    │
│  │  │ - Officer Decisions                  │  │    │
│  │  │ - Cyber Laws (PECA 2016)             │  │    │
│  │  │ - Audit Logs                         │  │    │
│  │  └──────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

---

## 👥 User Roles & Actors

### Actor Relationships
```
┌──────────────────────────────────────────────────┐
│                  SYSTEM USERS                     │
├──────────────────────────────────────────────────┤
│                                                  │
│  👤 CITIZEN / REPORTER                           │
│  ├─ Can file complaints (anonymous or registered)
│  ├─ Can upload evidence (images/videos/PDFs)   │
│  ├─ Can track complaint status                 │
│  ├─ Can view applicable laws                   │
│  └─ Can chat with AI assistant                 │
│                                                  │
│  👮 LAW ENFORCEMENT OFFICER                     │
│  ├─ Can login with auto-generated ID           │
│  ├─ Can view pending complaints                │
│  ├─ Can review evidence                        │
│  ├─ Can search cyber laws                      │
│  ├─ Can record decisions (Approve/Reject)      │
│  ├─ Can add investigation notes                │
│  └─ Can view statistics & analytics            │
│                                                  │
│  👨‍💼 SYSTEM ADMINISTRATOR                         │
│  ├─ Can manage officer accounts                │
│  ├─ Can access audit logs                      │
│  ├─ Can configure system settings              │
│  ├─ Can generate reports                       │
│  └─ Can manage system backups                  │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 🎯 Use Cases & Features

### Complete Feature Map
```
CYBER CRIME REPORTING SYSTEM
│
├── 👤 CITIZEN FEATURES
│   ├── 📋 Submit Complaint
│   │   ├─ Anonymous reporting
│   │   ├─ Registered reporting (CNIC)
│   │   └─ Form validation
│   ├── 📤 Upload Evidence
│   │   ├─ Images (JPG, PNG)
│   │   ├─ Videos (MP4, MOV)
│   │   ├─ PDFs
│   │   └─ Encryption
│   ├── 📍 Track Complaint
│   │   ├─ View tracking ID
│   │   ├─ Check status updates
│   │   └─ See officer notes
│   ├── 📚 View Cyber Laws
│   │   ├─ Search PECA laws
│   │   ├─ Filter by category
│   │   └─ View punishments
│   └── 🤖 AI Assistance
│       ├─ Complaint summarization
│       ├─ Legal category detection
│       └─ Smart recommendations
│
├── 👮 OFFICER FEATURES
│   ├── 🔐 Officer Login
│   │   ├─ ID: CYBER2026 + NAME
│   │   ├─ Password authentication
│   │   └─ Session management
│   ├── 📊 View Dashboard
│   │   ├─ Pending cases count
│   │   ├─ Performance metrics
│   │   └─ Case distribution
│   ├── 📋 Review Complaints
│   │   ├─ Case details
│   │   ├─ View evidence
│   │   └─ Citizen information
│   ├── ⚖️ Record Decisions
│   │   ├─ Approve case
│   │   ├─ Reject case
│   │   └─ Request information
│   ├── 📝 Investigation Notes
│   │   ├─ Add findings
│   │   ├─ Update status
│   │   └─ Timestamp tracking
│   └── 📈 View Statistics
│       ├─ Cases processed
│       ├─ Approval rate
│       └─ Time metrics
│
└── 👨‍💼 ADMIN FEATURES
    ├── 👤 Officer Management
    ├── 📊 System Analytics
    ├── 🔐 Security Logs
    ├── ⚙️ Configuration
    └── 📋 Reports
```

---

## 📊 Data Flow Diagram

### End-to-End Flow
```
CITIZEN COMPLAINT FLOW:

1. SUBMISSION
   Citizen → Complaint Form → Validation → Save to DB
              ↓
           JSON File / Supabase
              ↓
         Generate Tracking ID
              ↓
      Display to Citizen ✅

2. OFFICER REVIEW
   Officer Portal → Fetch Cases → Load Details
                      ↓
              Display Complaint
                      ↓
         View Evidence (Encrypted)
                      ↓
      Check Applicable Laws (AI)
                      ↓
           Make Decision
                      ↓
         Save Decision + Notes
                      ↓
      Update Case Status ✅

3. CITIZEN TRACKING
   Citizen → Enter Tracking ID → Query Database
                      ↓
            Return Case Status
                      ↓
        Display Officer Notes
                      ↓
         Show Current Status ✅
```

---

## 👤 Citizen Complaint Workflow

### Detailed Complaint Journey
```
START
  │
  ├─ Citizen Opens Portal
  │  └─ Home Page
  │     ├─ New complaint?
  │     └─ Track existing?
  │
  ├─ File New Complaint
  │  ├─ Select: Anonymous or Registered
  │  ├─ Fill Complaint Form
  │  │  ├─ Category (Hacking, Fraud, etc)
  │  │  ├─ Description
  │  │  └─ Attachments
  │  ├─ Upload Evidence
  │  │  ├─ Image/Video/PDF
  │  │  ├─ Encryption
  │  │  └─ Validation
  │  ├─ Form Validation
  │  │  ├─ Required fields?
  │  │  ├─ File size OK?
  │  │  └─ Format valid?
  │  ├─ Submit Complaint
  │  │  ├─ Save to Database
  │  │  ├─ Encrypt Evidence
  │  │  └─ Generate Tracking ID
  │  └─ SUCCESS: Show Tracking ID
  │     └─ Citizen notes down ID
  │
  ├─ Track Complaint
  │  ├─ Enter Tracking ID
  │  ├─ Query Database
  │  ├─ Current Status:
  │  │  ├─ Pending (waiting for officer)
  │  │  ├─ Under Review (officer reviewing)
  │  │  ├─ Approved (case accepted)
  │  │  ├─ Rejected (case rejected)
  │  │  └─ Closed (finalized)
  │  └─ Show Officer Notes
  │
  └─ END
```

---

## 👮 Officer Case Management Workflow

### Detailed Officer Journey
```
OFFICER LOGIN
  │
  ├─ Start Page
  │  └─ Unregistered? → Register First
  │     ├─ Enter Name
  │     ├─ Enter Password
  │     ├─ Generate ID: CYBER2026 + NAME
  │     └─ Save Credentials
  │
  ├─ Officer Login
  │  ├─ Enter Officer ID (CYBER2026XXXXX)
  │  ├─ Enter Password
  │  ├─ Authenticate
  │  └─ Create Session
  │
  ├─ DASHBOARD
  │  ├─ Show Pending Cases Count
  │  ├─ Show Statistics
  │  │  ├─ Total Reviewed
  │  │  ├─ Approved Count
  │  │  ├─ Rejected Count
  │  │  └─ Pending Count
  │  └─ Display Case List
  │
  ├─ SELECT CASE
  │  ├─ View Complaint Details
  │  ├─ View Citizen Info
  │  ├─ View Evidence
  │  │  ├─ Images
  │  │  ├─ Videos
  │  │  └─ PDFs
  │  └─ View Category Info
  │
  ├─ AI LAW RECOMMENDATIONS
  │  ├─ Analyze Complaint
  │  ├─ Suggest PECA Sections
  │  ├─ Show Punishment Range
  │  └─ Provide Guidance
  │
  ├─ MAKE DECISION
  │  ├─ Option 1: APPROVE
  │  │  ├─ Select Section of PECA
  │  │  ├─ Add Investigation Notes
  │  │  ├─ Recommend Punishment
  │  │  └─ Save Decision
  │  ├─ Option 2: REJECT
  │  │  ├─ Select Reason
  │  │  ├─ Add Comments
  │  │  └─ Save Decision
  │  └─ Option 3: REQUEST INFO
  │     ├─ Specify What's Needed
  │     ├─ Send to Citizen
  │     └─ Wait for Response
  │
  ├─ UPDATE CASE
  │  ├─ Save to Database
  │  ├─ Notify Citizen
  │  ├─ Update Status
  │  └─ Log Timestamp
  │
  └─ DONE ✅
```

---

## 🔧 System Components

### Module Architecture
```
CYBER CRIME REPORTING SYSTEM
│
├── frontend/ (Streamlit)
│   ├── app.py (Main entry)
│   ├── pages/
│   │   ├── report_form.py (Complaint filing)
│   │   ├── officer_login.py (Officer auth)
│   │   ├── officer_panel.py (Officer dashboard)
│   │   ├── law_guide.py (Legal reference)
│   │   ├── tracking.py (Complaint tracking)
│   │   └── help.py (Support)
│   ├── components/
│   │   └── chatbot.py (AI assistant)
│   ├── data/
│   │   └── cyber_laws.py (PECA laws database)
│   └── utils/
│       └── supabase_sync.py (DB sync)
│
├── backend/ (FastAPI)
│   ├── api/
│   │   └── main.py (API routes)
│   ├── services/
│   │   ├── database_service.py (CRUD ops)
│   │   ├── file_service.py (Upload/Download)
│   │   ├── ai_service.py (Groq API)
│   │   └── email_service.py (Notifications)
│   ├── models/ (Pydantic schemas)
│   └── utils/
│       ├── security.py (Encryption)
│       └── ciphers.py (Crypto)
│
├── database/
│   ├── schema.sql (DB structure)
│   ├── migrations/ (Version control)
│   └── seeds/ (Initial data)
│
└── docs/
    ├── API.md (API docs)
    ├── SECURITY.md (Security guide)
    └── DEPLOYMENT.md (Deploy guide)
```

---

## 💾 Database Schema Overview

### Core Tables
```
users
  ├─ id (PK)
  ├─ email
  ├─ password_hash (bcrypt)
  ├─ role (citizen/officer/admin)
  ├─ created_at
  └─ updated_at

complaints
  ├─ id (PK)
  ├─ user_id (FK)
  ├─ category
  ├─ description
  ├─ is_anonymous
  ├─ tracking_id (UNIQUE)
  ├─ status (pending/approved/rejected)
  ├─ created_at
  └─ updated_at

evidence
  ├─ id (PK)
  ├─ complaint_id (FK)
  ├─ file_name
  ├─ file_type
  ├─ file_path (encrypted)
  ├─ file_hash
  ├─ created_at
  └─ updated_at

officers
  ├─ id (PK)
  ├─ officer_id (UNIQUE) - CYBER2026 + NAME
  ├─ name
  ├─ password_hash (bcrypt)
  ├─ rank
  ├─ jurisdiction
  ├─ created_at
  └─ updated_at

cases
  ├─ id (PK)
  ├─ complaint_id (FK)
  ├─ officer_id (FK)
  ├─ status
  ├─ assigned_at
  ├─ completed_at
  └─ updated_at

decisions
  ├─ id (PK)
  ├─ case_id (FK)
  ├─ officer_id (FK)
  ├─ decision (approve/reject/request)
  ├─ peca_section
  ├─ notes
  ├─ created_at
  └─ updated_at

audit_logs
  ├─ id (PK)
  ├─ user_id (FK)
  ├─ action
  ├─ resource_type
  ├─ resource_id
  ├─ timestamp
  └─ details (JSON)
```

---

## 🚀 Deployment Architecture

### Cloud Deployment
```
┌──────────────────────────────────────────┐
│        GitHub (Source Control)           │
│  FarukhMumtaz/CyberCrime-IS              │
└──────────────────────────────────────────┘
                    ⬇️ Push
┌──────────────────────────────────────────┐
│      Streamlit Cloud (Frontend)          │
│  ├─ Citizen Portal                       │
│  └─ Officer Portal                       │
└──────────────────────────────────────────┘
                    ⬇️ API Calls
┌──────────────────────────────────────────┐
│      Supabase (Backend + Database)       │
│  ├─ FastAPI Backend                      │
│  ├─ PostgreSQL Database                  │
│  ├─ Secure Storage (Evidence)            │
│  └─ Encryption Layer                     │
└──────────────────────────────────────────┘
                    ⬇️ API Call
┌──────────────────────────────────────────┐
│       Groq API (AI Services)             │
│  ├─ Complaint Summarization              │
│  ├─ Category Detection                   │
│  └─ Legal Recommendations                │
└──────────────────────────────────────────┘
```

---

## 🔐 Security Architecture

### Multi-Layer Security
```
LAYER 1: TRANSPORT SECURITY
├─ HTTPS/TLS 1.3 (all connections)
├─ Certificate validation
└─ Secure headers

LAYER 2: APPLICATION SECURITY
├─ JWT Authentication
├─ Session Management
├─ CORS Configuration
├─ Rate Limiting
└─ Input Validation

LAYER 3: DATA SECURITY
├─ AES-256 Encryption (at rest)
├─ bcrypt Password Hashing
├─ Field-level encryption
├─ Secure token storage
└─ Evidence file encryption

LAYER 4: DATABASE SECURITY
├─ Row Level Security (RLS)
├─ SQL Injection Prevention
├─ Data Access Control
├─ Audit Logging
└─ Automatic Backups

LAYER 5: INFRASTRUCTURE SECURITY
├─ DDoS Protection
├─ Firewall Rules
├─ IP Whitelisting
├─ Security Groups
└─ VPC Isolation
```

---

## 📈 System Interaction Diagram

### Complete User Journey
```
USER JOURNEY: Citizen Filing Complaint

Time →

Citizen          Portal UI          Backend          Database
  │                │                   │                │
  │ Opens App      │                   │                │
  ├──────────────→ │                   │                │
  │                │ Load Home         │                │
  │                │                   │                │
  │ Click Report   │                   │                │
  ├──────────────→ │                   │                │
  │                │ Load Form         │                │
  │                │                   │                │
  │ Fill Form      │                   │                │
  ├──────────────→ │                   │                │
  │                │ Validate Data     │                │
  │                ├──────────────────→│                │
  │                │                   │ Check Business│
  │                │                   │ Rules          │
  │                │                   ├───────────────→│
  │                │                   │                │ Save
  │                │                   │                │ Record
  │                │                   │←───────────────┤
  │                │                   │ Record ID      │
  │                │←──────────────────┤                │
  │                │ Generate Tracking │                │
  │                │ ID                │                │
  │                │                   │                │
  │ Success! ✅    │                   │                │
  │←──────────────┤                    │                │
  │ Tracking ID   │                    │                │
```

---

## 📝 Notes

- All diagrams represent current system design (May 2026)
- ASCII diagrams are GitHub-compatible (no external tools needed)
- All components follow microservices principles
- Database schema normalized to 3NF
- Security implemented at every layer
- Scalable to 1000+ concurrent users

---

## 🔗 Related Documents

- [System Architecture](./architecture/system_architecture.md)
- [API Documentation](./api/api_documentation.md)
- [Security Guide](./SECURITY.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [User Guide](./guides/user_guide.md)

---

**Last Updated**: May 18, 2026  
**Status**: ✅ Production Ready  
**Version**: 2.0