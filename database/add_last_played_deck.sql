-- Add last_played_deck_id to profiles for Resume feature
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'profiles' AND column_name = 'last_played_deck_id') THEN
        ALTER TABLE public.profiles ADD COLUMN last_played_deck_id uuid REFERENCES public.decks(id);
    END IF;
END $$;
