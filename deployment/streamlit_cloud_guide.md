# Cyber Crime Reporting System - Deployment Guide

## Prerequisites

- Python 3.9+
- Supabase account
- Groq API key
- Streamlit Cloud account
- ClamAV (for malware scanning)

## Environment Setup

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd cyber-crime-reporting-system
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Supabase Setup

1. **Create Project**
   - Go to Supabase dashboard
   - Create new project
   - Note project URL and API keys

2. **Database Setup**
   - Run SQL migrations from `database/migrations/`
   - Execute seed data from `database/seeders/`

3. **Storage Setup**
   - Create bucket: `evidence-files`
   - Set public access: false
   - Configure RLS policies

4. **Authentication Setup**
   - Enable email authentication
   - Configure JWT secrets

## Streamlit Cloud Deployment

1. **Connect Repository**
   - Link GitHub repository to Streamlit Cloud
   - Set main branch for deployment

2. **Environment Variables**
   - Add all variables from .env to Streamlit secrets
   - Ensure sensitive keys are properly configured

3. **App Configuration**
   - Set entry point: `frontend/app.py`
   - Configure custom domain (optional)

4. **Deploy**
   - Push changes to trigger deployment
   - Monitor deployment logs

## Backend API Deployment (Optional)

If deploying backend separately:

1. **Docker Build**
   ```bash
   docker build -t cybercrime-api .
   ```

2. **Run Container**
   ```bash
   docker run -p 8000:8000 --env-file .env cybercrime-api
   ```

3. **Cloud Deployment**
   - Deploy to Heroku, Railway, or similar
   - Configure environment variables
   - Set up reverse proxy

## Security Checklist

- [ ] Environment variables configured securely
- [ ] Database RLS policies active
- [ ] HTTPS enabled
- [ ] CORS properly configured
- [ ] Rate limiting active
- [ ] File upload restrictions in place
- [ ] Audit logging enabled
- [ ] Backup procedures configured

## Monitoring Setup

1. **Error Tracking**
   - Set up Sentry or similar for error monitoring

2. **Performance Monitoring**
   - Configure application metrics
   - Set up alerts for downtime

3. **Security Monitoring**
   - Enable log analysis
   - Set up intrusion detection

## Backup Strategy

- **Database**: Daily automated backups via Supabase
- **Files**: Versioned storage with retention policies
- **Code**: Git versioning with protected branches

## Scaling Considerations

- **Horizontal Scaling**: Streamlit Cloud handles scaling
- **Database**: Supabase provides auto-scaling
- **Storage**: CDN integration for file delivery

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Check Python version compatibility
   - Verify all dependencies installed

2. **Database Connection**
   - Verify Supabase credentials
   - Check network connectivity

3. **File Upload Issues**
   - Check file size limits
   - Verify MIME type validation

4. **AI API Errors**
   - Check Groq API key
   - Verify rate limits

### Logs Location

- Application logs: `app.log`
- Streamlit logs: Streamlit Cloud dashboard
- Supabase logs: Supabase dashboard

## Rollback Procedure

1. **Code Rollback**
   ```bash
   git revert <commit-hash>
   git push origin main
   ```

2. **Database Rollback**
   - Use Supabase backup restore
   - Run migration rollback scripts

3. **Full Rollback**
   - Deploy previous stable version
   - Restore database from backup

## Maintenance

- **Regular Updates**: Update dependencies monthly
- **Security Patches**: Apply immediately
- **Performance Tuning**: Monitor and optimize
- **User Feedback**: Regular review and improvements