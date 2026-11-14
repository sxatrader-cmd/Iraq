-- نظام الشركاء — نفّذ هذا الملف مرة واحدة في Supabase → SQL Editor.
-- المفتاح العام (anon / publishable) فقط يصل إلى الدوال المسموحة.
-- الشريك يقرأ صفوفه. المدير وحده يغيّر حالة الحجز والعمولة.

create table if not exists public.affiliates (
  id uuid primary key references auth.users (id) on delete cascade,
  full_name text not null,
  phone text not null default '',
  email text not null unique,
  referral_code text not null unique check (referral_code ~ '^[A-Z0-9]{4,12}$'),
  is_admin boolean not null default false,
  created_at timestamptz not null default now()
);

create table if not exists public.referral_clicks (
  id bigint generated always as identity primary key,
  affiliate_id uuid not null references public.affiliates (id) on delete cascade,
  page_path text not null default '',
  created_at timestamptz not null default now()
);

create table if not exists public.bookings (
  id uuid primary key default gen_random_uuid(),
  affiliate_id uuid not null references public.affiliates (id) on delete cascade,
  referral_code text not null,
  customer_name text not null,
  customer_phone text,
  customer_email text,
  program text,
  travel_date text,
  people text,
  language text,
  page_url text,
  details jsonb not null default '{}'::jsonb,
  status text not null default 'pending' check (status in ('pending', 'confirmed', 'cancelled')),
  commission numeric(12, 2) check (commission is null or commission >= 0),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists referral_clicks_affiliate_created_idx
  on public.referral_clicks (affiliate_id, created_at desc);
create index if not exists bookings_affiliate_created_idx
  on public.bookings (affiliate_id, created_at desc);
create index if not exists bookings_status_idx
  on public.bookings (status);

alter table public.affiliates enable row level security;
alter table public.referral_clicks enable row level security;
alter table public.bookings enable row level security;

create or replace function public.is_admin()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1 from public.affiliates
    where id = auth.uid() and is_admin
  );
$$;

create or replace function public.handle_new_affiliate()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  new_code text;
  tries int := 0;
  person_name text;
  person_phone text;
begin
  if exists (select 1 from public.affiliates where id = new.id) then
    return new;
  end if;
  person_name := left(btrim(coalesce(new.raw_user_meta_data->>'full_name', '')), 120);
  if person_name = '' then
    person_name := split_part(coalesce(new.email, 'partner'), '@', 1);
  end if;
  person_phone := left(btrim(coalesce(new.raw_user_meta_data->>'phone', '')), 40);
  loop
    tries := tries + 1;
    new_code := upper(substr(md5(random()::text || clock_timestamp()::text || tries::text), 1, 6));
    begin
      insert into public.affiliates (id, full_name, phone, email, referral_code, is_admin)
      values (new.id, person_name, person_phone, new.email, new_code, false);
      exit;
    exception
      when unique_violation then
        if tries >= 8 then
          raise;
        end if;
    end;
  end loop;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_affiliate();

create or replace function public.record_referral_click(p_code text, p_page text)
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  affiliate uuid;
begin
  select id into affiliate
  from public.affiliates
  where referral_code = upper(btrim(coalesce(p_code, '')));
  if affiliate is null then
    return;
  end if;
  if (
    select count(*) from public.referral_clicks
    where affiliate_id = affiliate and created_at > now() - interval '1 minute'
  ) > 30 then
    return;
  end if;
  insert into public.referral_clicks (affiliate_id, page_path)
  values (affiliate, left(coalesce(p_page, ''), 300));
end;
$$;

create or replace function public.record_referral_booking(p_code text, p_payload jsonb)
returns uuid
language plpgsql
security definer
set search_path = public
as $$
declare
  affiliate uuid;
  code text;
  person text;
  details jsonb;
  booking_id uuid;
begin
  code := upper(btrim(coalesce(p_code, '')));
  select id into affiliate from public.affiliates where referral_code = code;
  if affiliate is null then
    return null;
  end if;
  person := left(btrim(coalesce(p_payload->>'customer_name', '')), 200);
  if person = '' then
    return null;
  end if;
  if (
    select count(*) from public.bookings
    where referral_code = code and created_at > now() - interval '1 minute'
  ) >= 8 then
    return null;
  end if;
  details := coalesce(p_payload->'details', '{}'::jsonb);
  if jsonb_typeof(details) <> 'object' then
    details := '{}'::jsonb;
  end if;
  details := details - 'access_key' - 'botcheck' - 'password' - 'apikey' - 'token' - 'authorization';
  if jsonb_typeof(details->'fields') = 'array' then
    details := jsonb_set(
      details,
      '{fields}',
      coalesce((
        select jsonb_agg(elem)
        from jsonb_array_elements(details->'fields') elem
        where lower(coalesce(elem->>'name', '')) not in
          ('access_key', 'botcheck', 'password', 'apikey', 'token', 'authorization')
      ), '[]'::jsonb)
    );
  end if;
  if octet_length(details::text) > 20000 then
    details := jsonb_build_object('truncated', true);
  end if;
  insert into public.bookings (
    affiliate_id, referral_code, customer_name, customer_phone, customer_email,
    program, travel_date, people, language, page_url, details, status, commission
  ) values (
    affiliate,
    code,
    person,
    nullif(left(btrim(coalesce(p_payload->>'customer_phone', '')), 40), ''),
    nullif(left(btrim(coalesce(p_payload->>'customer_email', '')), 200), ''),
    nullif(left(btrim(coalesce(p_payload->>'program', '')), 300), ''),
    nullif(left(btrim(coalesce(p_payload->>'travel_date', '')), 200), ''),
    nullif(left(btrim(coalesce(p_payload->>'people', '')), 120), ''),
    nullif(left(btrim(coalesce(p_payload->>'language', '')), 12), ''),
    nullif(left(btrim(coalesce(p_payload->>'page_url', '')), 300), ''),
    details,
    'pending',
    null
  )
  returning id into booking_id;
  return booking_id;
end;
$$;

create or replace function public.set_booking_status(
  p_id uuid,
  p_status text,
  p_commission numeric
)
returns public.bookings
language plpgsql
security definer
set search_path = public
as $$
declare
  row public.bookings;
begin
  if not public.is_admin() then
    raise exception 'not allowed' using errcode = '42501';
  end if;
  if p_status not in ('pending', 'confirmed', 'cancelled') then
    raise exception 'bad status';
  end if;
  if p_commission is not null and p_commission < 0 then
    raise exception 'bad commission';
  end if;
  update public.bookings
     set status = p_status,
         commission = case when p_status = 'confirmed' then p_commission else null end,
         updated_at = now()
   where id = p_id
   returning * into row;
  if row.id is null then
    raise exception 'not found';
  end if;
  return row;
end;
$$;

revoke all on function public.is_admin() from public, anon, authenticated;
grant execute on function public.is_admin() to authenticated;

revoke all on function public.handle_new_affiliate() from public, anon, authenticated;

create or replace function public.ensure_affiliate()
returns public.affiliates
language plpgsql
security definer
set search_path = public
as $$
declare
  row public.affiliates;
  uid uuid := auth.uid();
  em text;
  meta jsonb;
  person_name text;
  person_phone text;
  new_code text;
  tries int := 0;
begin
  if uid is null then
    raise exception 'not allowed' using errcode = '42501';
  end if;
  select * into row from public.affiliates where id = uid;
  if row.id is not null then
    return row;
  end if;
  select email, raw_user_meta_data into em, meta from auth.users where id = uid;
  person_name := left(btrim(coalesce(meta->>'full_name', '')), 120);
  if person_name = '' then
    person_name := split_part(coalesce(em, 'partner'), '@', 1);
  end if;
  person_phone := left(btrim(coalesce(meta->>'phone', '')), 40);
  loop
    tries := tries + 1;
    new_code := upper(substr(md5(random()::text || clock_timestamp()::text || tries::text), 1, 6));
    begin
      insert into public.affiliates (id, full_name, phone, email, referral_code, is_admin)
      values (uid, person_name, person_phone, em, new_code, false)
      returning * into row;
      return row;
    exception
      when unique_violation then
        select * into row from public.affiliates where id = uid;
        if row.id is not null then
          return row;
        end if;
        if tries >= 8 then
          raise;
        end if;
    end;
  end loop;
end;
$$;

revoke all on function public.ensure_affiliate() from public, anon, authenticated;
grant execute on function public.ensure_affiliate() to authenticated;

revoke all on function public.record_referral_click(text, text) from public, anon, authenticated;
grant execute on function public.record_referral_click(text, text) to anon, authenticated;

revoke all on function public.record_referral_booking(text, jsonb) from public, anon, authenticated;
grant execute on function public.record_referral_booking(text, jsonb) to anon, authenticated;

revoke all on function public.set_booking_status(uuid, text, numeric) from public, anon, authenticated;
grant execute on function public.set_booking_status(uuid, text, numeric) to authenticated;

drop policy if exists affiliates_select_own on public.affiliates;
create policy affiliates_select_own
  on public.affiliates
  for select
  to authenticated
  using (id = auth.uid() or public.is_admin());

drop policy if exists clicks_select_own on public.referral_clicks;
create policy clicks_select_own
  on public.referral_clicks
  for select
  to authenticated
  using (affiliate_id = auth.uid() or public.is_admin());

drop policy if exists bookings_select_own on public.bookings;
create policy bookings_select_own
  on public.bookings
  for select
  to authenticated
  using (affiliate_id = auth.uid() or public.is_admin());

revoke all on public.affiliates from anon, authenticated;
revoke all on public.referral_clicks from anon, authenticated;
revoke all on public.bookings from anon, authenticated;
grant select on public.affiliates to authenticated;
grant select on public.referral_clicks to authenticated;
grant select on public.bookings to authenticated;

create or replace view public.affiliate_stats
with (security_invoker = true) as
select
  a.id,
  a.full_name,
  a.phone,
  a.email,
  a.referral_code,
  a.is_admin,
  a.created_at,
  (select count(*) from public.referral_clicks c where c.affiliate_id = a.id) as clicks,
  (select count(*) from public.bookings b where b.affiliate_id = a.id) as bookings,
  (select count(*) from public.bookings b where b.affiliate_id = a.id and b.status = 'confirmed') as confirmed,
  (select coalesce(sum(b.commission), 0) from public.bookings b where b.affiliate_id = a.id and b.status = 'confirmed') as commission
from public.affiliates a;

revoke all on public.affiliate_stats from anon, authenticated;
grant select on public.affiliate_stats to authenticated;

do $$
begin
  alter publication supabase_realtime add table public.bookings;
exception
  when duplicate_object then null;
  when undefined_object then null;
end $$;
