-- Remove duplicate cards based on front_text within the same deck.
-- Keeps the oldest record (earliest created_at).

DELETE FROM public.cards
WHERE id IN (
  SELECT id
  FROM (
      SELECT id,
             -- Partition by deck and word to find duplicates in the same deck
             ROW_NUMBER() OVER (
                PARTITION BY deck_id, front_text 
                ORDER BY created_at ASC
             ) as row_num
      FROM public.cards
  ) t
  WHERE t.row_num > 1
);
