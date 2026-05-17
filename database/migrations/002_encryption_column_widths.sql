-- Widen fields that store classical-cipher ciphertext.
--
-- Ciphertext values are longer than the original plaintext values, so narrow
-- VARCHAR columns such as cnic VARCHAR(13) must become TEXT. This keeps existing
-- data, constraints, foreign keys, policies, triggers, and laws data intact.

DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'complaints' AND column_name = 'email'
    ) THEN
        ALTER TABLE public.complaints ALTER COLUMN email TYPE TEXT;
    END IF;

    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'complaints' AND column_name = 'full_name'
    ) THEN
        ALTER TABLE public.complaints ALTER COLUMN full_name TYPE TEXT;
    END IF;

    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'complaints' AND column_name = 'phone'
    ) THEN
        ALTER TABLE public.complaints ALTER COLUMN phone TYPE TEXT;
    END IF;

    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'complaints' AND column_name = 'cnic'
    ) THEN
        ALTER TABLE public.complaints ALTER COLUMN cnic TYPE TEXT;
    END IF;

    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'complaints' AND column_name = 'address'
    ) THEN
        ALTER TABLE public.complaints ALTER COLUMN address TYPE TEXT;
    END IF;

    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'complaints' AND column_name = 'location'
    ) THEN
        ALTER TABLE public.complaints ALTER COLUMN location TYPE TEXT;
    END IF;

    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'complaints' AND column_name = 'description'
    ) THEN
        ALTER TABLE public.complaints ALTER COLUMN description TYPE TEXT;
    END IF;

    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'complaints' AND column_name = 'detailed_log'
    ) THEN
        ALTER TABLE public.complaints ALTER COLUMN detailed_log TYPE TEXT;
    END IF;

    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'evidence' AND column_name = 'file_name'
    ) THEN
        ALTER TABLE public.evidence ALTER COLUMN file_name TYPE TEXT;
    END IF;

    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'evidence' AND column_name = 'original_name'
    ) THEN
        ALTER TABLE public.evidence ALTER COLUMN original_name TYPE TEXT;
    END IF;

    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'evidence' AND column_name = 'file_path'
    ) THEN
        ALTER TABLE public.evidence ALTER COLUMN file_path TYPE TEXT;
    END IF;

    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'evidence' AND column_name = 'mime_type'
    ) THEN
        ALTER TABLE public.evidence ALTER COLUMN mime_type TYPE TEXT;
    END IF;
END $$;
