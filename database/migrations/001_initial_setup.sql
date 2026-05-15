-- Initial Migration for Cyber Crime Reporting System
-- Run this in Supabase SQL Editor or via migration tool

-- This file contains the complete database setup
-- Execute the contents of schemas/main_schema.sql

-- After running this migration:
-- 1. Verify tables are created
-- 2. Check RLS policies are active
-- 3. Test with sample data
-- 4. Set up storage buckets for evidence files

-- Storage bucket setup (run in Supabase Dashboard)
-- Create bucket: 'evidence-files'
-- Set public: false
-- Configure RLS policies for secure access

-- Sample test data (optional)
-- INSERT INTO complaints (tracking_id, complaint_reason, description, incident_date)
-- VALUES (generate_tracking_id(), 'Phishing', 'Received phishing email', CURRENT_DATE);