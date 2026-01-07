-- Add tracking columns to profiles table
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'profiles' AND column_name = 'email') THEN
        ALTER TABLE public.profiles ADD COLUMN email text;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'profiles' AND column_name = 'auth_provider') THEN
        ALTER TABLE public.profiles ADD COLUMN auth_provider text;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'profiles' AND column_name = 'last_login') THEN
        ALTER TABLE public.profiles ADD COLUMN last_login timestamp with time zone;
    END IF;

    -- created_at might already exist from table creation, but ensuring it just in case
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'profiles' AND column_name = 'created_at') THEN
        ALTER TABLE public.profiles ADD COLUMN created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL;
    END IF;
END $$;
