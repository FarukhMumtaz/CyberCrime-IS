-- Cyber Crime Reporting System Database Schema
-- Supabase PostgreSQL

-- Enable Row Level Security
ALTER DATABASE postgres SET "app.jwt_secret" TO 'your-jwt-secret';

-- Users table (optional registration)
CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    phone VARCHAR(20),
    cnic VARCHAR(13) UNIQUE, -- 13-digit CNIC validation
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Complaints table
CREATE TABLE IF NOT EXISTS complaints (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    tracking_id VARCHAR(20) UNIQUE NOT NULL, -- Format: CCRS-PK-YYYY-XXXXXX
    user_id UUID REFERENCES users(id) ON DELETE SET NULL, -- NULL for anonymous
    full_name VARCHAR(255),
    phone VARCHAR(20),
    cnic VARCHAR(13), -- Encrypted if stored
    address TEXT,
    incident_date DATE NOT NULL,
    location VARCHAR(255),
    complaint_reason VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'submitted', -- submitted, under_review, resolved
    ai_summary TEXT, -- AI-generated summary
    ai_category VARCHAR(100), -- AI-detected category
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Evidence table
CREATE TABLE IF NOT EXISTS evidence (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    complaint_id UUID NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    original_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL, -- Supabase storage path
    file_type VARCHAR(10) NOT NULL, -- video, image, pdf
    mime_type VARCHAR(100) NOT NULL,
    file_size BIGINT NOT NULL, -- in bytes
    sha256_hash VARCHAR(64) NOT NULL, -- For integrity
    is_encrypted BOOLEAN DEFAULT TRUE,
    malware_scan_status VARCHAR(20) DEFAULT 'pending', -- pending, clean, infected
    metadata JSONB, -- EXIF/IPTC data, dimensions, etc.
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Cyber laws table
CREATE TABLE IF NOT EXISTS laws (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    category VARCHAR(100) NOT NULL, -- e.g., Hacking, Phishing
    section VARCHAR(50) NOT NULL, -- e.g., 13, 14
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    punishment TEXT, -- Fine and/or imprisonment details
    relevant_pepa_sections TEXT, -- Related PECA sections
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Audit log table
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL, -- e.g., complaint_submitted, evidence_uploaded
    resource_type VARCHAR(50) NOT NULL, -- e.g., complaint, evidence
    resource_id UUID NOT NULL,
    details JSONB, -- Additional context
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_complaints_tracking_id ON complaints(tracking_id);
CREATE INDEX IF NOT EXISTS idx_complaints_user_id ON complaints(user_id);
CREATE INDEX IF NOT EXISTS idx_complaints_status ON complaints(status);
CREATE INDEX IF NOT EXISTS idx_complaints_created_at ON complaints(created_at);
CREATE INDEX IF NOT EXISTS idx_evidence_complaint_id ON evidence(complaint_id);
CREATE INDEX IF NOT EXISTS idx_evidence_file_type ON evidence(file_type);
CREATE INDEX IF NOT EXISTS idx_laws_category ON laws(category);
CREATE INDEX IF NOT EXISTS idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

-- Row Level Security Policies

-- Users table RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid() = id);

-- Complaints table RLS
ALTER TABLE complaints ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own complaints" ON complaints
    FOR SELECT USING (auth.uid() = user_id OR user_id IS NULL);

CREATE POLICY "Users can insert own complaints" ON complaints
    FOR INSERT WITH CHECK (auth.uid() = user_id OR user_id IS NULL);

CREATE POLICY "Users can update own complaints" ON complaints
    FOR UPDATE USING (auth.uid() = user_id);

-- Evidence table RLS
ALTER TABLE evidence ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view evidence for own complaints" ON evidence
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM complaints
            WHERE complaints.id = evidence.complaint_id
            AND (complaints.user_id = auth.uid() OR complaints.user_id IS NULL)
        )
    );

CREATE POLICY "Users can insert evidence for own complaints" ON evidence
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM complaints
            WHERE complaints.id = evidence.complaint_id
            AND (complaints.user_id = auth.uid() OR complaints.user_id IS NULL)
        )
    );

-- Laws table RLS (public read)
ALTER TABLE laws ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Everyone can read laws" ON laws
    FOR SELECT USING (true);

-- Audit logs RLS (admin only)
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Only admins can view audit logs" ON audit_logs
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM auth.users
            WHERE auth.users.id = auth.uid()
            AND auth.users.raw_user_meta_data->>'role' = 'admin'
        )
    );

-- Functions

-- Function to generate tracking ID
CREATE OR REPLACE FUNCTION generate_tracking_id()
RETURNS VARCHAR(20) AS $$
DECLARE
    year_part VARCHAR(4);
    random_part VARCHAR(6);
    tracking_id VARCHAR(20);
    counter INTEGER := 0;
BEGIN
    year_part := EXTRACT(YEAR FROM NOW())::VARCHAR;
    random_part := UPPER(SUBSTRING(MD5(RANDOM()::TEXT) FROM 1 FOR 6));

    tracking_id := 'CCRS-PK-' || year_part || '-' || random_part;

    -- Ensure uniqueness
    WHILE EXISTS (SELECT 1 FROM complaints WHERE complaints.tracking_id = tracking_id) AND counter < 100 LOOP
        random_part := UPPER(SUBSTRING(MD5(RANDOM()::TEXT) FROM 1 FOR 6));
        tracking_id := 'CCRS-PK-' || year_part || '-' || random_part;
        counter := counter + 1;
    END LOOP;

    IF counter >= 100 THEN
        RAISE EXCEPTION 'Unable to generate unique tracking ID';
    END IF;

    RETURN tracking_id;
END;
$$ LANGUAGE plpgsql;

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_complaints_updated_at
    BEFORE UPDATE ON complaints
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_laws_updated_at
    BEFORE UPDATE ON laws
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert initial law data (sample)
INSERT INTO laws (category, section, title, description, punishment, relevant_pepa_sections) VALUES
('Unauthorized Access', '13', 'Unauthorized access to information system', 'Whoever intentionally accesses or causes access to any information system without lawful authority shall be punished.', 'Imprisonment up to 3 years or fine up to Rs. 5 million or both', 'PECA Section 13'),
('Data Damage', '14', 'Damage to information system or data', 'Whoever intentionally damages or causes damage to any information system or data shall be punished.', 'Imprisonment up to 5 years or fine up to Rs. 10 million or both', 'PECA Section 14'),
('Cyberstalking', '20', 'Cyberstalking', 'Whoever uses information system to stalk or harass another person shall be punished.', 'Imprisonment up to 3 years or fine up to Rs. 1 million or both', 'PECA Section 20')
ON CONFLICT DO NOTHING;