# Cyber Crime Reporting System with Electronic Evidence Module
- **DEMO:** https://cyber-crime-reporting-system-sre.streamlit.app/
- A secure, government-grade web platform for Pakistani citizens to report cybercrimes online, inspired by the official Pakistani cybercrime reporting system. Enhanced with modern cybersecurity, digital evidence management, AI assistance, and secure cloud deployment practices.

## Features

- **Secure Complaint Submission**: Anonymous or registered reporting with CNIC validation
- **Electronic Evidence Upload**: Secure handling of videos, images, and PDFs with malware scanning
- **Cyber Law Guidance**: Interactive Pakistan Cyber Crime Rule Book with PECA laws
- **AI-Powered Assistance**: Complaint summarization and legal category detection
- **PDF Report Generation**: Official complaint reports with watermarks and tracking IDs
- **Government-Style UI**: Professional, accessible interface compliant with WCAG 2.1 AA

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **AI**: Groq API
- **Security**: JWT, bcrypt, encryption
- **Deployment**: Streamlit Cloud

## Project Structure

```
cyber-crime-reporting-system/
├── frontend/                 # Streamlit app
├── backend/                  # API services
├── database/                 # Supabase schemas
├── docs/                     # Documentation
├── deployment/               # Deployment configs
├── requirements.txt          # Dependencies
├── .env                      # Environment variables
└── README.md                 # This file
```

## Security Features

- End-to-end encryption for evidence files
- Row Level Security (RLS) in database
- Input validation and sanitization
- Rate limiting and DDoS protection
- Secure authentication with JWT
- Malware scanning for uploads
- Audit logging and monitoring

## Legal Compliance

- Aligned with Pakistan's Prevention of Electronic Crimes Act (PECA) 2016
- Privacy-by-design principles
- Data minimization and retention policies
- Secure handling of sensitive citizen data

## Getting Started

### Prerequisites

- Python 3.9+
- Supabase account
- Groq API key
- Optional local ClamAV for malware scanning (not required on Streamlit Cloud)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd cyber-crime-reporting-system
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and database URLs
   ```

5. Set up Supabase:
   - Create a new project
   - Run database migrations from `database/migrations/`
   - Configure storage buckets

6. Run the application:
   ```bash
   # Frontend
   streamlit run frontend/app.py

   # Backend (if separate)
   uvicorn backend.api.main:app --reload
   ```

> Note: The Streamlit app entrypoint is `frontend/app.py`. This is the correct file path for local development and Streamlit Cloud deployment.

## Documentation

Detailed system diagrams and workflow diagrams are available in `docs/diagrams.md`.

## Development Workflow

- Follow GitHub Professional Workflow
- Implement security-first approach
- Run tests after every module
- Update documentation after milestones
- Commit only stable, tested code

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific tests
pytest frontend/tests/
pytest backend/tests/
```

## Deployment

Deploy to Streamlit Cloud:

1. Connect GitHub repository
2. Set environment variables in Streamlit Cloud
3. Deploy automatically on push to main branch

## Documentation

See `docs/` folder for detailed documentation:
- System Architecture
- Implementation Plan
- Security Architecture
- API Documentation
- Deployment Guide

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement with security in mind
4. Add tests
5. Submit a pull request

## License

This project is developed for educational and governmental use. Contact for licensing details.

## Contact

For support or inquiries:
- Email: [contact-email]
- Emergency: Pakistan Police Cybercrime Helpline (15)
- NCCIA: [contact-details]

---

**Disclaimer**: This system is designed for secure cybercrime reporting. Always follow local laws and regulations.
