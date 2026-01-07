-- Create user_backups table for simple blob backup
create table if not exists public.user_backups (
  user_id uuid references auth.users not null primary key,
  backup_data jsonb not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- RLS
alter table public.user_backups enable row level security;

create policy "Users can all their own backup"
on public.user_backups for all
using (auth.uid() = user_id)
with check (auth.uid() = user_id);
