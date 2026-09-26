-- e0f5082 added the grants below to migrations/20260913000000_captures.sql, but that file had already
-- been applied to the live project by then, so `supabase db push` treated it as already-run and skipped
-- the edit. This migration re-issues the same grants on their own; GRANT is idempotent, so running them
-- again here (and on any project that already has them) is a no-op.
grant usage on schema public to service_role;
grant all on table public.captures to service_role;
