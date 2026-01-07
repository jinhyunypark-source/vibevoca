-- Drop old progress table if exists (optional, or keeping parallel for migration)
-- DROP TABLE IF EXISTS public.user_progress;

-- Create the Optimized State Table
CREATE TABLE public.user_deck_states (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id uuid REFERENCES auth.users ON DELETE CASCADE NOT NULL,
  deck_id uuid REFERENCES public.decks(id) ON DELETE CASCADE NOT NULL,
  
  -- Aggregated Statistics (For instant UI rendering)
  total_count int DEFAULT 0,
  memorized_count int DEFAULT 0,
  remind_count int DEFAULT 0,
  
  -- Detailed Card Progress (JSONB)
  -- Data Structure Explanation:
  -- [
  --   { 
  --     "id": "card_uuid", 
  --     "s": "new" | "review" | "memo",  (Status)
  --     "rc": int, (Remind Count)
  --     "mc": int  (Re-memorize Count)
  --   }
  -- ]
  card_states jsonb DEFAULT '[]'::jsonb, 
  
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  
  UNIQUE(user_id, deck_id)
);

-- Index for fast lookup by user
CREATE INDEX idx_deck_states_user ON public.user_deck_states(user_id);

-- Enable RLS
ALTER TABLE public.user_deck_states ENABLE ROW LEVEL SECURITY;

-- Policy: Users can see their own states
CREATE POLICY "Users can view own deck states" 
ON public.user_deck_states FOR SELECT 
USING (auth.uid() = user_id);

-- Policy: Users can insert/update their own states
CREATE POLICY "Users can upsert own deck states" 
ON public.user_deck_states FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own deck states" 
ON public.user_deck_states FOR UPDATE
USING (auth.uid() = user_id);
