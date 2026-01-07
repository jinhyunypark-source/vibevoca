-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- 1. Categories Table
create table public.categories (
  id uuid default gen_random_uuid() primary key,
  title text not null,
  description text,
  image_url text, -- E.g. "COMMUNICATION"
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 2. Decks Table
create table public.decks (
  id uuid default gen_random_uuid() primary key,
  category_id uuid references public.categories(id) on delete cascade not null,
  title text not null, -- E.g. "LOGIC_CLARITY"
  title_ko text, -- Korean Title (e.g. "논리적 명확성")
  order_index int default 0,
  color text default '#FF5733', 
  icon text, 
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 3. Cards Table
create table public.cards (
  id uuid default gen_random_uuid() primary key,
  deck_id uuid references public.decks(id) on delete cascade not null,
  front_text text not null, -- English Word
  back_text text not null,  -- Korean Definition
  example_sentences text[] default '{}', -- Examples
  audio_url text,           
  order_index int default 0,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 4. User Profiles
create table public.profiles (
  id uuid references auth.users on delete cascade primary key,
  role text,
  interests jsonb default '[]'::jsonb,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 5. User Progress
create type card_status as enum ('new', 'reviewing', 'memorized');

create table public.user_progress (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users on delete cascade not null,
  card_id uuid references public.cards(id) on delete cascade not null,
  status card_status default 'new',
  fail_count int default 0,
  last_reviewed_at timestamp with time zone,
  unique(user_id, card_id)
);

-- Row Level Security (RLS)
alter table public.categories enable row level security;
alter table public.decks enable row level security;
alter table public.cards enable row level security;
alter table public.profiles enable row level security;
alter table public.user_progress enable row level security;

-- Policies
-- Content is readable by everyone, distinct from User Data
create policy "Allow Public Read on Categories" on public.categories for select using (true);
create policy "Allow Public Read on Decks" on public.decks for select using (true);
create policy "Allow Public Read on Cards" on public.cards for select using (true);

-- User Data is private
create policy "Users can view own profile" on public.profiles for select using (auth.uid() = id);
create policy "Users can update own profile" on public.profiles for update using (auth.uid() = id);

create policy "Users can view own progress" on public.user_progress for select using (auth.uid() = user_id);
create policy "Users can insert own progress" on public.user_progress for insert with check (auth.uid() = user_id);
create policy "Users can update own progress" on public.user_progress for update using (auth.uid() = user_id);

-- 6. Contexts Table (Metadata for AI Prompts)
-- Defines scenarios like "Cafe", "Office", "Travel"
create table public.contexts (
    id uuid default gen_random_uuid() primary key,
    type text not null check (type in ('place', 'emotion', 'environment')), -- New Type Column
    slug text not null unique, -- e.g. 'place_cafe'
    label text not null,       -- e.g. 'Cafe'
    icon text,                 -- e.g. 'coffee'
    prompt_description text,   -- e.g. "In a busy cafe with ambient noise..."
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 7. Card Examples Table (Pre-generated Content)
-- Stores the specific sentence generated for a (Card + Context) combo
create table public.card_examples (
    id uuid default gen_random_uuid() primary key,
    card_id uuid references public.cards(id) on delete cascade not null,
    context_id uuid references public.contexts(id) on delete cascade not null,
    sentence text not null,
    translation text,
    audio_url text, -- Future TTS
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    unique(card_id, context_id)
);

-- Security Policies for New Tables
alter table public.contexts enable row level security;
alter table public.card_examples enable row level security;

-- Admin/Public Policies (Simplification: Public Read, Service Role Write)
create policy "Allow Public Read on Contexts" on public.contexts for select using (true);
create policy "Allow Public Read on CardExamples" on public.card_examples for select using (true);
-- Write is restricted to Service Role (Admin) by default unless policies added

