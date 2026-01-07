-- Add completed_deck_ids to profiles to track fully mastered decks
ALTER TABLE public.profiles 
ADD COLUMN IF NOT EXISTS completed_deck_ids text[] DEFAULT '{}';

-- Function to append a deck ID to the completed list
CREATE OR REPLACE FUNCTION public.append_completed_deck(user_uuid uuid, deck_uuid text)
RETURNS void AS $$
BEGIN
  UPDATE public.profiles
  SET completed_deck_ids = array_append(completed_deck_ids, deck_uuid)
  WHERE id = user_uuid AND NOT (completed_deck_ids @> ARRAY[deck_uuid]);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
