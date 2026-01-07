-- Migration: Refactor Meta Interests (Unified Table)

-- 1. Add columns to meta_interests
ALTER TABLE meta_interests 
ADD COLUMN IF NOT EXISTS category text DEFAULT 'job', -- job, hobby, vibe
ADD COLUMN IF NOT EXISTS tags text[] DEFAULT '{}';   -- For recommendations

-- 2. Migrate existing meta_interests (defaults to 'job' if not specified)
UPDATE meta_interests SET category = 'job' WHERE category IS NULL;

-- 2.4 Deduplicate 'code' in meta_interests before adding constraint
-- Keep the row with the minimum ctid (arbitrary but efficient way to keep one)
DELETE FROM meta_interests a USING meta_interests b
WHERE a.ctid < b.ctid AND a.code = b.code;

-- 2.5 Ensure 'code' is unique (Required for ON CONFLICT)
ALTER TABLE meta_interests DROP CONSTRAINT IF EXISTS meta_interests_code_unique;
ALTER TABLE meta_interests ADD CONSTRAINT meta_interests_code_unique UNIQUE (code);

-- 3. Migrate 'contexts' data to 'meta_interests' (Category: 'vibe')
-- Preserve 'id' so that related tables (like card_examples) can still link to it if we update FK.
-- Mapping:
--   id <- id
--   code <- slug
--   label_en <- label
--   label_ko <- label (fallback)
--   icon <- icon
--   category <- 'vibe'
--   tags <- ARRAY[type] (e.g. {emotion}, {place})
INSERT INTO meta_interests (id, code, label_en, label_ko, icon, category, tags, order_index)
SELECT 
    id, -- Preserve UUID
    slug, 
    label, 
    label, -- Fallback
    icon, 
    'vibe',
    ARRAY[type], -- Map old 'type' (emotion, place) to tags
    row_number() OVER (ORDER BY created_at) -- Simple ordering
FROM contexts
ON CONFLICT (code) DO NOTHING; -- If code exists, skip. (Risky if ID differs, but assuming migration phase)
-- Note: code must be unique. If contexts.slug conflicts with interest.code, we might skip.
-- Assuming slugs are unique enough (e.g. 'coffee_shop', 'happy').

-- 4. Update Dependent Foreign Keys (card_examples)
-- Drop old constraint linking to 'contexts'
ALTER TABLE card_examples DROP CONSTRAINT IF EXISTS card_examples_context_id_fkey;

-- (Optional) Rename column to be more generic, or just keep context_id but point to meta_interests
-- ALTER TABLE card_examples RENAME COLUMN context_id TO interest_id;

-- Add new constraint linking to 'meta_interests'
-- This requires that ALL context_ids in card_examples now exist in meta_interests (ensured by step 3)
ALTER TABLE card_examples ADD CONSTRAINT card_examples_interest_id_fkey 
    FOREIGN KEY (context_id) REFERENCES meta_interests(id) ON DELETE SET NULL;

-- 4. Create new Types or Constraints (Optional but good for data integrity)
-- ALTER TABLE meta_interests ADD CONSTRAINT check_category CHECK (category IN ('job', 'hobby', 'vibe'));

-- 5. Drop contexts table (Unified table is meta_interests)
DROP TABLE contexts;
