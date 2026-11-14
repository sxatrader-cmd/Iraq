-- نظام الشركاء (موقع العراق).
-- كل الكائنات ببادئة aff_ حتى لا تتعارض مع الجداول والدوال والتريجرات
-- الموجودة مسبقاً في هذا المشروع (مثل public.bookings و public.is_admin()
-- و trigger on_auth_user_created على auth.users).
-- هذا الملف لا يحذف ولا يعدّل أي كائن قائم.

create table if not exists public.aff_affiliates (
  id uuid primary key references auth.users (id) on delete cascade,
  full_name text not null,
  phone text not null default '',
  email text not null unique,
  referral_code text not null unique check (referral_code ~ '^[A-Z0-9]{4,12}$'),
  is_admin boolean not null default false,
  created_at timestamptz not null default now()
);

create table if not exists public.aff_referral_clicks (
  id bigint generated always as identity primary key,
  affiliate_id uuid not null references public.aff_affiliates (id) on delete cascade,
  page_path text not null default '',
  created_at timestamptz not null default now()
);

create table if not exists public.aff_bookings (
  id uuid primary key default gen_random_uuid(),
  affiliate_id uuid not null references public.aff_affiliates (id) on delete cascade,
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

create table if not exists public.aff_customers (
  id bigint generated always as identity primary key,
  affiliate_id uuid not null references public.aff_affiliates (id) on delete cascade,
  phone_normalized text unique,
  email_normalized text unique,
  created_at timestamptz not null default now(),
  check (phone_normalized is not null or email_normalized is not null)
);

create index if not exists aff_customers_affiliate_idx
  on public.aff_customers (affiliate_id, created_at desc);

create index if not exists aff_referral_clicks_affiliate_created_idx
  on public.aff_referral_clicks (affiliate_id, created_at desc);
create index if not exists aff_bookings_affiliate_created_idx
  on public.aff_bookings (affiliate_id, created_at desc);
create index if not exists aff_bookings_status_idx
  on public.aff_bookings (status);

alter table public.aff_affiliates enable row level security;
alter table public.aff_referral_clicks enable row level security;
alter table public.aff_bookings enable row level security;
alter table public.aff_customers enable row level security;

create or replace function public.aff_is_admin()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1 from public.aff_affiliates
    where id = auth.uid() and is_admin
  );
$$;

-- تريجر مستقل عن on_auth_user_created / handle_new_user القائمين.
-- يضيف صفاً في aff_affiliates فقط، ويتجاهل التعارض، ولا يرمي خطأ أبداً
-- حتى لا يتعطّل تسجيل المواقع الأخرى على نفس المشروع.
create or replace function public.aff_handle_new_user()
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
  begin
    if exists (select 1 from public.aff_affiliates where id = new.id) then
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
        insert into public.aff_affiliates (id, full_name, phone, email, referral_code, is_admin)
        values (new.id, person_name, person_phone, new.email, new_code, false)
        on conflict (id) do nothing;
        exit;
      exception
        when unique_violation then
          if exists (select 1 from public.aff_affiliates where id = new.id) then
            exit;
          end if;
          if tries >= 8 then
            exit;
          end if;
      end;
    end loop;
  exception
    when others then
      null;
  end;
  return new;
end;
$$;

drop trigger if exists aff_on_auth_user_created on auth.users;
create trigger aff_on_auth_user_created
  after insert on auth.users
  for each row execute function public.aff_handle_new_user();

create or replace function public.aff_record_referral_click(p_code text, p_page text)
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  affiliate uuid;
begin
  select id into affiliate
  from public.aff_affiliates
  where referral_code = upper(btrim(coalesce(p_code, '')));
  if affiliate is null then
    return;
  end if;
  if (
    select count(*) from public.aff_referral_clicks
    where affiliate_id = affiliate and created_at > now() - interval '1 minute'
  ) > 30 then
    return;
  end if;
  insert into public.aff_referral_clicks (affiliate_id, page_path)
  values (affiliate, left(coalesce(p_page, ''), 300));
end;
$$;

create or replace function public.aff_normalize_phone(p_phone text)
returns text
language plpgsql
immutable
set search_path = public
as $$
declare
  d text;
begin
  d := regexp_replace(coalesce(p_phone, ''), '[^0-9]', '', 'g');
  d := regexp_replace(d, '^(00)+', '');
  if left(d, 3) = '964' then
    d := substr(d, 4);
  end if;
  if left(d, 1) = '0' then
    d := substr(d, 2);
  end if;
  if length(d) < 8 then
    return null;
  end if;
  return d;
end;
$$;

create or replace function public.aff_normalize_email(p_email text)
returns text
language plpgsql
immutable
set search_path = public
as $$
declare
  e text;
begin
  e := lower(btrim(coalesce(p_email, '')));
  if e = '' or position('@' in e) < 2 or position('@' in e) = length(e) then
    return null;
  end if;
  return left(e, 200);
end;
$$;

create or replace function public.aff_claim_customer(
  p_affiliate uuid,
  p_phone text,
  p_email text
)
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
  if p_affiliate is null then
    return;
  end if;
  if p_phone is not null then
    insert into public.aff_customers (affiliate_id, phone_normalized)
    values (p_affiliate, p_phone)
    on conflict (phone_normalized) do nothing;
  end if;
  if p_email is not null then
    insert into public.aff_customers (affiliate_id, email_normalized)
    values (p_affiliate, p_email)
    on conflict (email_normalized) do nothing;
  end if;
end;
$$;

create or replace function public.aff_owner_for_customer(p_phone text, p_email text)
returns uuid
language plpgsql
stable
security definer
set search_path = public
as $$
declare
  owner uuid;
begin
  select c.affiliate_id into owner
  from public.aff_customers c
  where (p_phone is not null and c.phone_normalized = p_phone)
     or (p_email is not null and c.email_normalized = p_email)
  order by c.created_at asc, c.id asc
  limit 1;
  return owner;
end;
$$;

create or replace function public.aff_record_referral_booking(p_code text, p_payload jsonb)
returns uuid
language plpgsql
security definer
set search_path = public
as $$
declare
  affiliate uuid;
  locked uuid;
  code text;
  person text;
  details jsonb;
  booking_id uuid;
  phone_norm text;
  email_norm text;
begin
  code := upper(btrim(coalesce(p_code, '')));
  person := left(btrim(coalesce(p_payload->>'customer_name', '')), 200);
  if person = '' then
    return null;
  end if;
  phone_norm := public.aff_normalize_phone(coalesce(p_payload->>'customer_phone', ''));
  email_norm := public.aff_normalize_email(coalesce(p_payload->>'customer_email', ''));
  locked := public.aff_owner_for_customer(phone_norm, email_norm);
  if locked is not null then
    affiliate := locked;
  else
    if code = '' then
      return null;
    end if;
    select id into affiliate from public.aff_affiliates where referral_code = code;
    if affiliate is null then
      return null;
    end if;
  end if;
  if locked is not null then
    select referral_code into code from public.aff_affiliates where id = affiliate;
  end if;
  if (
    select count(*) from public.aff_bookings
    where affiliate_id = affiliate and created_at > now() - interval '1 minute'
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
  insert into public.aff_bookings (
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
  perform public.aff_claim_customer(affiliate, phone_norm, email_norm);
  return booking_id;
end;
$$;

create or replace function public.aff_set_booking_status(
  p_id uuid,
  p_status text,
  p_commission numeric
)
returns public.aff_bookings
language plpgsql
security definer
set search_path = public
as $$
declare
  row public.aff_bookings;
begin
  if not public.aff_is_admin() then
    raise exception 'not allowed' using errcode = '42501';
  end if;
  if p_status not in ('pending', 'confirmed', 'cancelled') then
    raise exception 'bad status';
  end if;
  if p_commission is not null and p_commission < 0 then
    raise exception 'bad commission';
  end if;
  update public.aff_bookings
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

revoke all on function public.aff_is_admin() from public, anon, authenticated;
grant execute on function public.aff_is_admin() to authenticated;

revoke all on function public.aff_handle_new_user() from public, anon, authenticated;

create or replace function public.aff_ensure_affiliate()
returns public.aff_affiliates
language plpgsql
security definer
set search_path = public
as $$
declare
  row public.aff_affiliates;
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
  select * into row from public.aff_affiliates where id = uid;
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
      insert into public.aff_affiliates (id, full_name, phone, email, referral_code, is_admin)
      values (uid, person_name, person_phone, em, new_code, false)
      on conflict (id) do nothing;
      select * into row from public.aff_affiliates where id = uid;
      if row.id is not null then
        return row;
      end if;
      if tries >= 8 then
        raise exception 'could not create affiliate';
      end if;
    exception
      when unique_violation then
        select * into row from public.aff_affiliates where id = uid;
        if row.id is not null then
          return row;
        end if;
        if tries >= 8 then
          raise exception 'could not create affiliate';
        end if;
    end;
  end loop;
end;
$$;

revoke all on function public.aff_ensure_affiliate() from public, anon, authenticated;
grant execute on function public.aff_ensure_affiliate() to authenticated;

revoke all on function public.aff_record_referral_click(text, text) from public, anon, authenticated;
grant execute on function public.aff_record_referral_click(text, text) to anon, authenticated;

revoke all on function public.aff_record_referral_booking(text, jsonb) from public, anon, authenticated;
grant execute on function public.aff_record_referral_booking(text, jsonb) to anon, authenticated;

revoke all on function public.aff_set_booking_status(uuid, text, numeric) from public, anon, authenticated;
grant execute on function public.aff_set_booking_status(uuid, text, numeric) to authenticated;

drop policy if exists aff_affiliates_select_own on public.aff_affiliates;
create policy aff_affiliates_select_own
  on public.aff_affiliates
  for select
  to authenticated
  using (id = auth.uid() or public.aff_is_admin());

drop policy if exists aff_clicks_select_own on public.aff_referral_clicks;
create policy aff_clicks_select_own
  on public.aff_referral_clicks
  for select
  to authenticated
  using (affiliate_id = auth.uid() or public.aff_is_admin());

drop policy if exists aff_bookings_select_own on public.aff_bookings;
create policy aff_bookings_select_own
  on public.aff_bookings
  for select
  to authenticated
  using (affiliate_id = auth.uid() or public.aff_is_admin());

revoke all on public.aff_affiliates from anon, authenticated;
revoke all on public.aff_referral_clicks from anon, authenticated;
revoke all on public.aff_bookings from anon, authenticated;
grant select on public.aff_affiliates to authenticated;
grant select on public.aff_referral_clicks to authenticated;
grant select on public.aff_bookings to authenticated;

revoke all on function public.aff_normalize_phone(text) from public, anon, authenticated;
revoke all on function public.aff_normalize_email(text) from public, anon, authenticated;
revoke all on function public.aff_claim_customer(uuid, text, text) from public, anon, authenticated;
revoke all on function public.aff_owner_for_customer(text, text) from public, anon, authenticated;

drop policy if exists aff_customers_select_own on public.aff_customers;
create policy aff_customers_select_own
  on public.aff_customers
  for select
  to authenticated
  using (affiliate_id = auth.uid() or public.aff_is_admin());

revoke all on public.aff_customers from anon, authenticated;
grant select on public.aff_customers to authenticated;

create or replace view public.aff_affiliate_stats
with (security_invoker = true) as
select
  a.id,
  a.full_name,
  a.phone,
  a.email,
  a.referral_code,
  a.is_admin,
  a.created_at,
  (select count(*) from public.aff_referral_clicks c where c.affiliate_id = a.id) as clicks,
  (select count(*) from public.aff_bookings b where b.affiliate_id = a.id) as bookings,
  (select count(*) from public.aff_bookings b where b.affiliate_id = a.id and b.status = 'confirmed') as confirmed,
  (select coalesce(sum(b.commission), 0) from public.aff_bookings b where b.affiliate_id = a.id and b.status = 'confirmed') as commission
from public.aff_affiliates a;

revoke all on public.aff_affiliate_stats from anon, authenticated;
grant select on public.aff_affiliate_stats to authenticated;

create or replace function public.aff_bookings_claim_customer()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  begin
    perform public.aff_claim_customer(
      new.affiliate_id,
      public.aff_normalize_phone(new.customer_phone),
      public.aff_normalize_email(new.customer_email)
    );
  exception
    when others then
      null;
  end;
  return new;
end;
$$;

revoke all on function public.aff_bookings_claim_customer() from public, anon, authenticated;

drop trigger if exists aff_bookings_claim_customer on public.aff_bookings;
create trigger aff_bookings_claim_customer
  after insert on public.aff_bookings
  for each row execute function public.aff_bookings_claim_customer();

do $$
begin
  alter publication supabase_realtime add table public.aff_bookings;
exception
  when duplicate_object then null;
  when undefined_object then null;
end $$;
