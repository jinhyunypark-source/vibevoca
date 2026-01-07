-- 1. Create meta_jobs table
create table public.meta_jobs (
  id uuid default gen_random_uuid() primary key,
  code text not null unique,
  label_en text not null,
  label_ko text not null,
  icon text,          -- Material Icon name or asset path
  color text,         -- Hex color code (e.g. #FF5733)
  order_index int default 0,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 2. Create meta_interests table
create table public.meta_interests (
  id uuid default gen_random_uuid() primary key,
  code text not null unique,
  label_en text not null,
  label_ko text not null,
  icon text,
  color text,
  order_index int default 0,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 3. Update profiles table
-- Add job_id (Foreign Key)
alter table public.profiles 
add column job_id uuid references public.meta_jobs(id);

-- Add interest_ids (Array of UUIDs)
alter table public.profiles 
add column interest_ids uuid[] default '{}';

-- 4. Enable RLS and Policies for new tables
alter table public.meta_jobs enable row level security;
alter table public.meta_interests enable row level security;

-- Public Read Policies
create policy "Allow Public Read on Jobs" on public.meta_jobs for select using (true);
create policy "Allow Public Read on Interests" on public.meta_interests for select using (true);

-- 5. Seed Data
-- Seed Jobs
insert into public.meta_jobs (code, label_en, label_ko, icon, color, order_index) values
('student', 'Student', '학생', 'school', '#4CAF50', 10),
('developer', 'Developer', '개발자', 'code', '#2196F3', 20),
('designer', 'Designer', '디자이너', 'brush', '#E91E63', 30),
('business', 'Business/Marketing', '경영/마케팅', 'business_center', '#FF9800', 40),
('freelancer', 'Freelancer', '프리랜서', 'laptop_mac', '#9C27B0', 50),
('other', 'Other', '기타', 'person', '#9E9E9E', 99);

-- Seed Interests
insert into public.meta_interests (code, label_en, label_ko, icon, color, order_index) values
('travel', 'Travel', '여행', 'flight', '#03A9F4', 10),
('business', 'Business', '비즈니스', 'trending_up', '#4CAF50', 20),
('technology', 'Technology', 'IT/기술', 'memory', '#2196F3', 30),
('art', 'Art & Design', '예술/디자인', 'palette', '#E91E63', 40),
('culture', 'Culture', '문화', 'theater_comedy', '#9C27B0', 50),
('food', 'Food & Dining', '음식/맛집', 'restaurant', '#FF5722', 60),
('daily_life', 'Daily Life', '일상', 'local_cafe', '#795548', 70),
('academic', 'Academic', '학습/연구', 'import_contacts', '#607D8B', 80);
