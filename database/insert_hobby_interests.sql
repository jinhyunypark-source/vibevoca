-- Insert additional 'hobby' categories into meta_interests
-- Category: 'hobby'
-- Items: social, activity, career, learning, conversation, marketing, health, friendship, movie, technology, medical
-- Icons chosen to match the theme.
-- Column 'tags' is used for related keywords (TEXT[]).

INSERT INTO meta_interests (code, label_en, label_ko, icon, category, tags, order_index)
VALUES 
  ('social', 'Social', '소셜/사교', 'groups', 'hobby', ARRAY['social'], 10),
  ('activity', 'Activity', '활동/액티비티', 'directions_run', 'hobby', ARRAY['activity'], 11),
  ('career', 'Career', '커리어', 'work', 'hobby', ARRAY['career'], 12),
  ('learning', 'Learning', '학습/공부', 'school', 'hobby', ARRAY['learning'], 13),
  ('conversation', 'Conversation', '대화/소통', 'chat', 'hobby', ARRAY['conversation'], 14),
  ('marketing', 'Marketing', '마케팅', 'campaign', 'hobby', ARRAY['marketing'], 15),
  ('health', 'Health', '건강', 'health_and_safety', 'hobby', ARRAY['health'], 16),
  ('friendship', 'Friendship', '우정', 'diversity_1', 'hobby', ARRAY['friendship'], 17),
  ('movie', 'Movie', '영화', 'movie', 'hobby', ARRAY['movie'], 18),
  ('technology', 'Technology', '기술/테크', 'computer', 'hobby', ARRAY['technology'], 19),
  ('medical', 'Medical', '의학/의료', 'medical_services', 'hobby', ARRAY['medical'], 20)
ON CONFLICT (code) DO UPDATE 
SET 
  category = EXCLUDED.category,
  tags = EXCLUDED.tags,
  icon = EXCLUDED.icon;
