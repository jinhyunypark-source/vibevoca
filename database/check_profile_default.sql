-- Check default value for interest_ids in profiles table
SELECT column_name, column_default, data_type
FROM information_schema.columns
WHERE table_name = 'profiles' AND column_name = 'interest_ids';
