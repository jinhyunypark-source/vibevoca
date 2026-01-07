-- Enable INSERT permission for authenticated users on profiles table
-- This is required for 'upsert' to create a new profile if one doesn't exist.

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'profiles' AND policyname = 'Users can insert own profile'
    ) THEN
        CREATE POLICY "Users can insert own profile" 
        ON public.profiles 
        FOR INSERT 
        WITH CHECK (auth.uid() = id);
    END IF;
END $$;
