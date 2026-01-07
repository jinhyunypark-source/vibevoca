-- 1. Modify meta_interests table to add category (safely)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'meta_interests' AND column_name = 'category') THEN
        ALTER TABLE public.meta_interests ADD COLUMN category text DEFAULT 'interest';
    END IF;
END $$;

-- 2. Update Constraints: Replace single uniqueness on 'code' with composite (category, code)
-- This allows 'business' to exist as both a 'job' and an 'interest'
ALTER TABLE public.meta_interests DROP CONSTRAINT IF EXISTS meta_interests_code_key;
-- If constraint name is different, try generic drop or just add the new one first (though new one doesn't fix old one blocking).
-- Assuming default name "meta_interests_code_key". 

ALTER TABLE public.meta_interests DROP CONSTRAINT IF EXISTS meta_interests_category_code_key; -- prevent error if re-run
ALTER TABLE public.meta_interests ADD CONSTRAINT meta_interests_category_code_key UNIQUE (category, code);

-- 3. Migrate Jobs to meta_interests
INSERT INTO public.meta_interests (id, category, code, label_en, label_ko, icon, color, order_index, created_at)
SELECT id, 'job', code, label_en, label_ko, icon, color, order_index, created_at
FROM public.meta_jobs
ON CONFLICT (id) DO NOTHING; -- Avoid re-inserting if already run

-- 4. Update profiles table to unify job_id into interest_ids
UPDATE public.profiles
SET interest_ids = array_append(interest_ids, job_id)
WHERE job_id IS NOT NULL 
  AND (interest_ids IS NULL OR NOT (interest_ids @> ARRAY[job_id])); -- Prevent duplicates

-- 5. Clean up
ALTER TABLE public.profiles DROP COLUMN IF EXISTS job_id;
DROP TABLE IF EXISTS public.meta_jobs;

-- 6. Finalize constraints
ALTER TABLE public.meta_interests ALTER COLUMN category SET NOT NULL;
