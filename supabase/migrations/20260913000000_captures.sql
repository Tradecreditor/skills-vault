-- Capture queue written by the `capture` Edge Function (service role only; no client policies).
create table if not exists public.captures (
  url         text primary key,                    -- normalised URL
  note        text,
  source      text not null default 'shortcut',    -- shortcut | telegram | manual
  status      text not null default 'queued',      -- queued | fired | fire_failed | done
  session_id  text,                                -- claude_code_session_id returned by the Routine fire API
  session_url text,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
alter table public.captures enable row level security;
-- No policies on purpose: only the service role (used inside the Edge Function) can read/write.
-- Newer projects no longer grant new tables to service_role automatically; without this the function gets
-- "permission denied for table captures" and every link comes back as db_error ("Vault: 0 queued").
grant usage on schema public to service_role;
grant all on table public.captures to service_role;
create or replace function public.touch_updated_at() returns trigger language plpgsql as $$
begin new.updated_at = now(); return new; end $$;
drop trigger if exists captures_touch on public.captures;
create trigger captures_touch before update on public.captures for each row execute function public.touch_updated_at();
