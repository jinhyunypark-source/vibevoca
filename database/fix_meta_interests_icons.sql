-- Fix meta_interests icons with correct Material Icons
-- This script updates icons for all interests to ensure they display correctly

-- Update hobby interests with correct icons
UPDATE meta_interests SET icon = 'sports_soccer' WHERE code = 'soccer';
UPDATE meta_interests SET icon = 'sports_soccer' WHERE code = 'football';
UPDATE meta_interests SET icon = 'groups' WHERE code = 'social';
UPDATE meta_interests SET icon = 'flight' WHERE code = 'travel';
UPDATE meta_interests SET icon = 'directions_run' WHERE code = 'activity';
UPDATE meta_interests SET icon = 'work' WHERE code = 'career';
UPDATE meta_interests SET icon = 'school' WHERE code = 'learning';
UPDATE meta_interests SET icon = 'chat' WHERE code = 'conversation';
UPDATE meta_interests SET icon = 'campaign' WHERE code = 'marketing';
UPDATE meta_interests SET icon = 'favorite' WHERE code = 'health';
UPDATE meta_interests SET icon = 'diversity_1' WHERE code = 'friendship';
UPDATE meta_interests SET icon = 'movie' WHERE code = 'movie';
UPDATE meta_interests SET icon = 'computer' WHERE code = 'technology';
UPDATE meta_interests SET icon = 'medical_services' WHERE code = 'medical';

-- Update job/occupation interests with correct icons
UPDATE meta_interests SET icon = 'school' WHERE code = 'student';
UPDATE meta_interests SET icon = 'code' WHERE code = 'developer';
UPDATE meta_interests SET icon = 'work' WHERE code = 'office_worker';
UPDATE meta_interests SET icon = 'business_center' WHERE code = 'business';

-- Insert missing interests if they don't exist
-- Soccer/Football (if not exists)
INSERT INTO meta_interests (code, label_en, label_ko, icon, category, tags, order_index)
VALUES ('soccer', 'Soccer', '축구', 'sports_soccer', 'hobby', ARRAY['soccer', 'sports'], 21)
ON CONFLICT (code) DO UPDATE
SET icon = EXCLUDED.icon, label_en = EXCLUDED.label_en, label_ko = EXCLUDED.label_ko;

-- Travel (if not exists)
INSERT INTO meta_interests (code, label_en, label_ko, icon, category, tags, order_index)
VALUES ('travel', 'Travel', '여행', 'flight', 'hobby', ARRAY['travel', 'trip'], 22)
ON CONFLICT (code) DO UPDATE
SET icon = EXCLUDED.icon, label_en = EXCLUDED.label_en, label_ko = EXCLUDED.label_ko;

-- Display updated records
SELECT code, label_ko, icon, category, order_index
FROM meta_interests
WHERE category = 'hobby' OR category = 'job'
ORDER BY category, order_index;
