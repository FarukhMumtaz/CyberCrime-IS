# Cyber Crime Reporting System - API Documentation

## Overview

The Cyber Crime Reporting System provides RESTful APIs for secure complaint submission, evidence management, and legal guidance.

## Base URL
```
http://localhost:8000
```

## Authentication

All protected endpoints require JWT authentication via Bearer token.

### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

email=user@example.com&password=securepassword
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Register
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "phone": "03001234567",
  "cnic": "1234567890123"
}
```

## Complaints

### Create Complaint
```http
POST /complaints/
Authorization: Bearer <token>
Content-Type: application/json

{
  "full_name": "John Doe",
  "phone": "03001234567",
  "cnic": "1234567890123",
  "address": "Karachi, Pakistan",
  "incident_date": "2024-01-15",
  "location": "Karachi",
  "complaint_reason": "Phishing",
  "description": "Received phishing email from unknown sender."
}
```

**Response:**
```json
{
  "tracking_id": "CCRS-PK-2024-ABC123",
  "message": "Complaint submitted successfully",
  "status": "submitted"
}
```

### Get Complaint
```http
GET /complaints/{tracking_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "complaint": {
    "tracking_id": "CCRS-PK-2024-ABC123",
    "status": "submitted",
    "description": "Received phishing email...",
    "ai_category": "Phishing",
    "ai_summary": "Victim received fraudulent email...",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

## Evidence Upload

### Upload Evidence
```http
POST /evidence/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

complaint_id=CCRS-PK-2024-ABC123
files=<evidence_file>
```

**Response:**
```json
{
  "uploaded_files": [
    {
      "file_name": "evidence.jpg",
      "status": "uploaded",
      "size": 1024000
    }
  ]
}
```

## Legal Information

### Get Laws
```http
GET /laws/?category=Hacking&search=unauthorized
```

**Response:**
```json
{
  "laws": [
    {
      "section": "13",
      "title": "Unauthorized access to information system",
      "category": "Unauthorized Access",
      "description": "Whoever intentionally accesses...",
      "punishment": "Imprisonment up to 3 years...",
      "relevant_pepa_sections": "PECA Section 13"
    }
  ]
}
```

## PDF Generation

### Generate PDF Report
```http
GET /pdf/{tracking_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "pdf_data": "<base64_encoded_pdf>",
  "filename": "complaint_CCRS-PK-2024-ABC123.pdf"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid token"
}
```

### 404 Not Found
```json
{
  "detail": "Complaint not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

- 100 requests per 15 minutes per IP
- Applied to all endpoints

## Security Features

- JWT authentication
- Input validation and sanitization
- File type and size validation
- Malware scanning
- Data encryption
- Audit logging