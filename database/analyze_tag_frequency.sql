-- 1. Unnest the tags array to get one row per tag
-- 2. Group by the tag to count occurrences
-- 3. Order by count descending
SELECT
  tag,
  COUNT(*) as card_count
FROM (
  SELECT unnest(tags) as tag
  FROM public.card_sentences
) sub
GROUP BY tag
ORDER BY card_count DESC;
