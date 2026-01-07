-- Index for performance
CREATE INDEX IF NOT EXISTS idx_card_sentences_card_id ON public.card_sentences(card_id);
CREATE INDEX IF NOT EXISTS idx_card_sentences_tags ON public.card_sentences USING GIN(tags);

-- Function to get relevant vibe sentences for a whole deck based on user context tags
-- Returns a TABLE: card_id, sentence_en, sentence_ko, tags
CREATE OR REPLACE FUNCTION get_vibe_sentences_for_deck(
  p_deck_id UUID,
  p_user_tags TEXT[]
)
RETURNS TABLE (
  card_id UUID,
  sentence_en TEXT,
  sentence_ko TEXT,
  tags TEXT[]
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    cs.card_id,
    cs.sentence_en,
    cs.sentence_ko,
    cs.tags
  FROM
    public.card_sentences cs
  JOIN
    public.cards c ON cs.card_id = c.id
  WHERE
    c.deck_id = p_deck_id
    AND cs.tags && p_user_tags -- Overlap check: true if any tag matches
  ORDER BY
    random() -- Randomize if we have many
  LIMIT
    500; -- Safety limit
END;
$$;
