# 📊 System Diagrams & Architecture Documentation

**Cyber Crime Reporting System - Pakistan**  
**Professional Visual Guide to System Architecture & Workflows**

---

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [Citizen Complaint Flow](#citizen-flow)
3. [Officer Case Management](#officer-flow)
4. [Database Structure](#database)
5. [Component Architecture](#components)
6. [Security Layers](#security)
7. [Deployment Pipeline](#deployment)
8. [User Interactions](#interactions)

---

## 🏗️ System Architecture

### 3-Layer Architecture Overview

```mermaid
graph TB
    subgraph Frontend["🎨 PRESENTATION LAYER"]
        FE1["📱 Streamlit Citizen Portal"]
        FE2["👮 Streamlit Officer Portal"]
    end

    subgraph Backend["🔧 APPLICATION LAYER"]
        BE1["⚙️ FastAPI Backend"]
        BE2["🔐 Security Services"]
        BE3["🤖 AI Services (Groq)"]
        BE4["📧 Notification Services"]
    end

    subgraph Database["💾 DATA LAYER"]
        DB1["🗄️ PostgreSQL Database"]
        DB2["📁 Secure Storage"]
        DB3["🔑 Encryption Layer"]
    end

    Frontend -->|REST API| Backend
    Backend -->|SQL Queries| Database
    Backend -->|File Operations| Database
    
    style Frontend fill:#e1f5ff,stroke:#01579b,stroke-width:3px
    style Backend fill:#f3e5f5,stroke:#4a148c,stroke-width:3px
    style Database fill:#e8f5e9,stroke:#1b5e20,stroke-width:3px
```

---

## 👥 User Roles & Permissions

```mermaid
graph LR
    subgraph Citizens["👤 CITIZENS"]
        C1["📋 File Complaint"]
        C2["📤 Upload Evidence"]
        C3["📍 Track Status"]
        C4["📚 View Laws"]
    end

    subgraph Officers["👮 OFFICERS"]
        O1["🔐 Login/Register"]
        O2["📊 View Dashboard"]
        O3["📋 Review Cases"]
        O4["✅ Make Decisions"]
        O5["📝 Add Notes"]
    end

    subgraph Admins["👨‍💼 ADMINISTRATORS"]
        A1["👤 Manage Officers"]
        A2["📊 View Analytics"]
        A3["🔐 Security Logs"]
        A4["⚙️ System Config"]
    end

    System["Cyber Crime System"]
    
    Citizens -.->|Access| System
    Officers -.->|Access| System
    Admins -.->|Manage| System
    
    style Citizens fill:#ffebee,stroke:#b71c1c,stroke-width:2px
    style Officers fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style Admins fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
```

---

## 📋 Citizen Complaint Workflow

### End-to-End Citizen Journey

```mermaid
sequenceDiagram
    participant Citizen as 👤 Citizen
    participant Portal as 🌐 Portal
    participant Backend as ⚙️ Backend
    participant Database as 🗄️ Database
    participant Officer as 👮 Officer

    Citizen->>Portal: 📱 Open App
    Portal->>Portal: ✅ Load Home Page
    
    Citizen->>Portal: 📋 Click "File Complaint"
    Portal->>Portal: 📝 Show Form
    
    Citizen->>Portal: ✍️ Fill Details & Upload Evidence
    Portal->>Backend: 🔒 Validate & Encrypt
    Backend->>Backend: 🔐 Check Security
    
    Backend->>Database: 💾 Save Complaint
    Database-->>Backend: ✅ Record ID
    Backend-->>Portal: 🎫 Generate Tracking ID
    Portal-->>Citizen: 📲 Show Success + Tracking ID
    
    Note over Citizen: ⏳ Later...
    
    Citizen->>Portal: 🔍 Enter Tracking ID
    Portal->>Backend: 📊 Query Status
    Backend->>Database: 📂 Fetch Complaint
    Database-->>Backend: 📋 Return Data
    Backend-->>Portal: 📈 Status Info
    Portal-->>Citizen: ✅ Show Status & Officer Notes

    Officer->>Portal: 👮 Login
    Portal->>Backend: 🔐 Authenticate
    Backend-->>Portal: ✅ Approved
    Portal->>Portal: 📊 Show Pending Cases
    
    Officer->>Portal: 🔍 Select Case
    Portal->>Backend: 📚 Fetch Full Details
    Backend->>Database: 🗄️ Query Case
    Database-->>Backend: 📋 Case Data
    Backend-->>Portal: 📄 Display Case
    
    Officer->>Portal: ⚖️ Review & Decide
    Portal->>Backend: 💾 Save Decision
    Backend->>Database: 📝 Update Status
    Database-->>Backend: ✅ Saved
    Backend-->>Portal: ✅ Confirmation
    
    Portal-->>Officer: 🎉 Decision Recorded
    Backend-->>Citizen: 📧 Notification
```

---

## 👮 Officer Case Management Workflow

### Officer Complete Journey

```mermaid
graph TD
    A["🎯 Officer Portal Home"] -->|Register/Login| B["🔐 Authentication"]
    B -->|Valid Credentials| C["📊 Officer Dashboard"]
    B -->|Invalid| B
    
    C -->|View Pending| D["📋 Pending Cases List"]
    C -->|View Statistics| E["📈 Performance Stats"]
    
    D -->|Select Case| F["🔍 Case Details Page"]
    
    F -->|View Evidence| G["📁 Evidence Gallery"]
    F -->|Check Laws| H["📚 AI-Recommended Laws"]
    F -->|Add Notes| I["✏️ Investigation Notes"]
    
    G -->|Reviewed| J["Decision Point"]
    H -->|Selected| J
    I -->|Completed| J
    
    J -->|APPROVE| K["✅ Case Approved"]
    J -->|REJECT| L["❌ Case Rejected"]
    J -->|REQUEST INFO| M["❓ Request Additional Info"]
    
    K -->|Save| N["💾 Update Database"]
    L -->|Save| N
    M -->|Save| N
    
    N -->|Success| O["📧 Notify Citizen"]
    O -->|Done| P["✨ Case Closed"]
    
    P -->|Back to| C
    
    style A fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style C fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style K fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style L fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style P fill:#fff9c4,stroke:#f57f17,stroke-width:2px
```

---

## 💾 Database Schema & Structure

### Complete Database Architecture

```mermaid
graph LR
    subgraph Users["👥 Users Table"]
        U["id, email, password_hash<br/>role, created_at"]
    end

    subgraph Complaints["📋 Complaints Table"]
        C["id, user_id, category<br/>description, tracking_id<br/>status, created_at"]
    end

    subgraph Evidence["📁 Evidence Table"]
        E["id, complaint_id, file_name<br/>file_type, file_path<br/>file_hash, encrypted"]
    end

    subgraph Officers["👮 Officers Table"]
        O["id, officer_id, name<br/>password_hash, rank<br/>jurisdiction, created_at"]
    end

    subgraph Cases["📌 Cases Table"]
        CA["id, complaint_id<br/>officer_id, status<br/>assigned_at, completed_at"]
    end

    subgraph Decisions["⚖️ Decisions Table"]
        D["id, case_id, officer_id<br/>decision, peca_section<br/>notes, created_at"]
    end

    subgraph Logs["📊 Audit Logs Table"]
        L["id, user_id, action<br/>resource_type, timestamp<br/>details JSON"]
    end

    Users -->|1..N| Complaints
    Complaints -->|1..N| Evidence
    Complaints -->|1..N| Cases
    Cases -->|1..1| Officers
    Cases -->|1..N| Decisions
    Officers -->|N..1| Decisions
    Users -->|1..N| Logs
    
    style Users fill:#bbdefb,stroke:#1565c0,stroke-width:2px
    style Complaints fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style Evidence fill:#f8bbd0,stroke:#c2185b,stroke-width:2px
    style Officers fill:#ffe0b2,stroke:#e65100,stroke-width:2px
    style Cases fill:#f0f4c3,stroke:#827717,stroke-width:2px
    style Decisions fill:#d1c4e9,stroke:#512da8,stroke-width:2px
    style Logs fill:#ffccbc,stroke:#bf360c,stroke-width:2px
```

---

## 🔧 System Components & Modules

### Frontend & Backend Architecture

```mermaid
graph TB
    subgraph Frontend["🎨 FRONTEND - Streamlit"]
        FE_App["app.py<br/>Main Entry Point"]
        FE_Pages["📄 Pages Module"]
        FE_Data["📊 Data Module"]
        FE_Utils["🛠️ Utils Module"]
        FE_Components["🧩 Components"]
        
        FE_App -->|Loads| FE_Pages
        FE_Pages -->|Uses| FE_Data
        FE_Pages -->|Uses| FE_Utils
        FE_Pages -->|Uses| FE_Components
    end

    subgraph Backend["⚙️ BACKEND - FastAPI"]
        BE_API["api/main.py<br/>API Endpoints"]
        BE_Services["Services Layer"]
        BE_DB["Database Layer"]
        BE_Security["🔐 Security Layer"]
        
        BE_API -->|Calls| BE_Services
        BE_Services -->|Uses| BE_DB
        BE_Services -->|Uses| BE_Security
    end

    subgraph Database["💾 DATABASE - Supabase"]
        DB_SQL["PostgreSQL"]
        DB_Storage["File Storage"]
        DB_Cache["Cache Layer"]
        
        DB_SQL -->|Stores| DB_Cache
        DB_Storage -->|Manages| DB_Cache
    end

    Frontend -->|REST API| Backend
    Backend -->|SQL Queries| Database
    Backend -->|File Ops| Database
    
    style Frontend fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    style Backend fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    style Database fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
```

---

## 🔐 Security Architecture - 5 Layers

### Complete Security Implementation

```mermaid
graph TB
    subgraph Layer1["🌐 LAYER 1: Transport Security"]
        L1_A["HTTPS/TLS 1.3"]
        L1_B["Certificate Validation"]
        L1_C["Secure Headers"]
    end

    subgraph Layer2["🔐 LAYER 2: Application Security"]
        L2_A["JWT Authentication"]
        L2_B["Session Management"]
        L2_C["CORS Policy"]
        L2_D["Rate Limiting"]
        L2_E["Input Validation"]
    end

    subgraph Layer3["🔒 LAYER 3: Data Security"]
        L3_A["AES-256 Encryption"]
        L3_B["bcrypt Hashing"]
        L3_C["Field Encryption"]
        L3_D["Token Security"]
    end

    subgraph Layer4["🗄️ LAYER 4: Database Security"]
        L4_A["Row Level Security"]
        L4_B["SQL Injection Prevention"]
        L4_C["Access Control"]
        L4_D["Audit Logging"]
        L4_E["Backups"]
    end

    subgraph Layer5["🛡️ LAYER 5: Infrastructure Security"]
        L5_A["DDoS Protection"]
        L5_B["Firewall Rules"]
        L5_C["IP Whitelisting"]
        L5_D["VPC Isolation"]
    end

    Request["🔗 User Request"]
    
    Request -->|Passes through| Layer1
    Layer1 -->|Validates| Layer2
    Layer2 -->|Secures| Layer3
    Layer3 -->|Protects| Layer4
    Layer4 -->|Infrastructure| Layer5
    Layer5 -->|Allows| Response["✅ Secure Response"]
    
    style Layer1 fill:#e0f2f1,stroke:#004d40,stroke-width:2px
    style Layer2 fill:#f1f8e9,stroke:#33691e,stroke-width:2px
    style Layer3 fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    style Layer4 fill:#e3f2fd,stroke:#0d47a1,stroke-width:2px
    style Layer5 fill:#fff3e0,stroke:#e65100,stroke-width:2px
```

---

## 🚀 Deployment Pipeline

### Cloud Infrastructure Flow

```mermaid
graph LR
    subgraph Dev["👨‍💻 Development"]
        DEV_GIT["Git Repository<br/>FarukhMumtaz/CyberCrime-IS"]
        DEV_CODE["Code Changes"]
    end

    subgraph Deploy["☁️ Deployment"]
        DEPLOY_FRONTEND["Streamlit Cloud<br/>Citizen Portal"]
        DEPLOY_OFFICER["Streamlit Cloud<br/>Officer Portal"]
        DEPLOY_BACKEND["Supabase<br/>FastAPI Backend"]
    end

    subgraph Infra["🌐 Infrastructure"]
        INFRA_DB["PostgreSQL<br/>Database"]
        INFRA_STORAGE["Secure Storage<br/>Evidence Files"]
        INFRA_AI["Groq API<br/>AI Services"]
    end

    DEV_CODE -->|Push| DEV_GIT
    DEV_GIT -->|Deploy| DEPLOY_FRONTEND
    DEV_GIT -->|Deploy| DEPLOY_OFFICER
    DEV_GIT -->|Deploy| DEPLOY_BACKEND
    
    DEPLOY_FRONTEND -->|API Calls| DEPLOY_BACKEND
    DEPLOY_OFFICER -->|API Calls| DEPLOY_BACKEND
    DEPLOY_BACKEND -->|Queries| INFRA_DB
    DEPLOY_BACKEND -->|File Ops| INFRA_STORAGE
    DEPLOY_BACKEND -->|AI Calls| INFRA_AI
    
    style Dev fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    style Deploy fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style Infra fill:#bbdefb,stroke:#1565c0,stroke-width:2px
```

---

## 🔄 User Interaction Diagram

### Complete System Interactions

```mermaid
graph TB
    subgraph Citizens["👤 CITIZENS"]
        C1["File Complaint"]
        C2["Upload Evidence"]
        C3["Track Status"]
        C4["View Laws"]
    end

    subgraph System["🎯 CYBER CRIME SYSTEM"]
        S1["Portal UI"]
        S2["Backend API"]
        S3["Database"]
        S4["AI Engine"]
    end

    subgraph Officers["👮 OFFICERS"]
        O1["Login"]
        O2["Review Cases"]
        O3["Make Decisions"]
        O4["View Analytics"]
    end

    C1 -->|Submit| S1
    C2 -->|Upload| S1
    C3 -->|Query| S1
    C4 -->|Search| S1
    
    S1 -->|Process| S2
    S1 -->|Validate| S4
    S2 -->|Store| S3
    S4 -->|Analyze| S3
    
    O1 -->|Authenticate| S1
    O2 -->|Request| S1
    O3 -->|Submit| S1
    O4 -->|View| S1
    
    S1 -->|Display| Officers
    S1 -->|Display| Citizens
    
    style Citizens fill:#ffebee,stroke:#b71c1c,stroke-width:2px
    style System fill:#e3f2fd,stroke:#0d47a1,stroke-width:2px
    style Officers fill:#fff3e0,stroke:#e65100,stroke-width:2px
```

---

## 📊 Feature & Capability Matrix

### All System Features

```mermaid
graph TB
    subgraph Features["✨ SYSTEM FEATURES"]
        F1["🔐 Authentication & Authorization"]
        F2["📋 Complaint Management"]
        F3["📤 Evidence Handling"]
        F4["📚 Legal Reference System"]
        F5["🤖 AI Assistance"]
        F6["📊 Analytics & Statistics"]
        F7["🔒 Security & Encryption"]
        F8["📧 Notifications"]
        F9["⚖️ Decision Workflow"]
        F10["📱 Mobile Responsive"]
    end

    subgraph Users["👥 USER ACCESS"]
        U1["Citizens: F1,F2,F3,F4,F5,F10"]
        U2["Officers: F1,F2,F3,F4,F6,F9,F10"]
        U3["Admins: F1,F6,F7,F8"]
    end

    F1 --> U1
    F1 --> U2
    F1 --> U3
    
    F2 --> U1
    F2 --> U2
    
    F3 --> U1
    F3 --> U2
    
    F4 --> U1
    F4 --> U2
    
    F5 --> U1
    
    F6 --> U2
    F6 --> U3
    
    F9 --> U2
    
    F10 --> U1
    F10 --> U2
    
    style Features fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style Users fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
```

---

## 📝 Notes & Documentation

- **All Diagrams**: Mermaid syntax (GitHub compatible)
- **Rendering**: Works on GitHub without external tools
- **Mobile Friendly**: Responsive and accessible
- **Professional**: Enterprise-grade visualization
- **Current**: As of May 18, 2026
- **Status**: ✅ Production Ready

---

## 🔗 Related Documentation

- [README.md](../README.md) - Project Overview
- [API Documentation](./api/api_documentation.md) - API Reference
- [Security Guide](./SECURITY.md) - Security Details
- [Deployment Guide](./DEPLOYMENT.md) - Deploy Instructions
- [User Guide](./guides/user_guide.md) - How to Use

---

**Last Updated**: May 18, 2026 | **Version**: 2.0 | **Status**: ✅ Production Ready
