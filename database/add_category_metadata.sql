-- Add new columns to categories table
ALTER TABLE public.categories ADD COLUMN IF NOT EXISTS icon text;
ALTER TABLE public.categories ADD COLUMN IF NOT EXISTS title_ko text;
ALTER TABLE public.categories ADD COLUMN IF NOT EXISTS color text DEFAULT '#4A90E2';

-- Update Metadata for known categories
-- Communication
UPDATE public.categories 
SET 
  title_ko = '소통과 표현', 
  icon = 'forum', 
  color = '#4A90E2' -- Blue associated with communication
WHERE title ILIKE 'Communication%';

-- Sense & Style
UPDATE public.categories 
SET 
  title_ko = '감각과 스타일', 
  icon = 'palette', 
  color = '#9B59B6' -- Purple associated with creativity/style
WHERE title ILIKE 'Sense & Style%';

-- Intelligence & Judgment
UPDATE public.categories 
SET 
  title_ko = '지혜와 통찰', 
  icon = 'lightbulb', 
  color = '#F1C40F' -- Yellow associated with ideas/intelligence
WHERE title ILIKE 'Intelligence%';

-- Relationships & Social
UPDATE public.categories 
SET 
  title_ko = '관계와 사회', 
  icon = 'diversity_3', 
  color = '#2ECC71' -- Green associated with harmony/social
WHERE title ILIKE 'Relationships%';

-- Change & Growth (Assuming title is 'Change & Growth' or similar)
UPDATE public.categories 
SET 
  title_ko = '변화와 성장', 
  icon = 'trending_up', 
  color = '#E67E22' -- Orange associated with energy/change
WHERE title ILIKE 'Change%';

-- Power & Authority
UPDATE public.categories 
SET 
  title_ko = '권력과 권위', 
  icon = 'gavel', 
  color = '#E74C3C' -- Red associated with power
WHERE title ILIKE 'Power%';

-- Difficulty & Complexity
UPDATE public.categories 
SET 
  title_ko = '난이도와 복잡성', 
  icon = 'extension', 
  color = '#34495E' -- Dark Grey/Blue associated with complexity
WHERE title ILIKE 'Difficulty%';

-- Size & Quantity
UPDATE public.categories 
SET 
  title_ko = '규모와 수량', 
  icon = 'bar_chart', 
  color = '#1ABC9C' -- Teal
WHERE title ILIKE 'Size%';

-- Money & Finance
UPDATE public.categories 
SET 
  title_ko = '돈과 경제', 
  icon = 'attach_money', 
  color = '#27AE60' -- Green (Money)
WHERE title ILIKE 'Money%';

-- Time & Duration
UPDATE public.categories 
SET 
  title_ko = '시간과 기간', 
  icon = 'schedule', 
  color = '#95A5A6' -- Grey (Time)
WHERE title ILIKE 'Time%';
