-- Remove duplicate rows from card_sentences
-- Keeps the row with the smallest ID (earliest insertion) for each unique combination of card_id, sentence_en, and tags.
-- Using sentence_en in the grouping ensures we don't accidentally delete different sentences that happen to have the same tags.

DELETE FROM public.card_sentences
WHERE id NOT IN (
    SELECT MIN(id::text)::uuid
    FROM public.card_sentences
    GROUP BY card_id, sentence_en, tags
);
