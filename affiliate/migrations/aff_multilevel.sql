-- عمولات المستويين (التجنيد).
-- شغّل هذا الملف مرة واحدة في Supabase → SQL Editor على المشروع الحي.
-- لا يحذف حجوزات ولا يغيّر الجداول القديمة خارج بادئة aff_.
-- آمن لإعادة التشغيل.

alter table public.aff_affiliates
  add column if not exists sponsor_id uuid references public.aff_affiliates (id) on delete set null;

alter table public.aff_affiliates
  drop constraint if exists aff_affiliates_no_self_sponsor;
alter table public.aff_affiliates
  add constraint aff_affiliates_no_self_sponsor
  check (sponsor_id is null or sponsor_id <> id);

create index if not exists aff_affiliates_sponsor_idx
  on public.aff_affiliates (sponsor_id);

alter table public.aff_bookings
  add column if not exists amount numeric(12, 2) check (amount is null or amount >= 0);

create table if not exists public.aff_commissions (
  id bigint generated always as identity primary key,
  booking_id uuid not null references public.aff_bookings (id) on delete cascade,
  affiliate_id uuid not null references public.aff_affiliates (id) on delete cascade,
  level int not null check (level in (0, 1, 2)),
  rate numeric(6, 4) not null check (rate >= 0 and rate <= 1),
  amount numeric(12, 2) check (amount is null or amount >= 0),
  status text not null check (status in ('pending', 'confirmed', 'rejected')),
  created_at timestamptz not null default now(),
  unique (booking_id, affiliate_id, level)
);

create index if not exists aff_commissions_affiliate_idx
  on public.aff_commissions (affiliate_id, status);

alter table public.aff_commissions enable row level security;

-- الراعي يُثبَّت عند إنشاء الصف فقط. أي تعديل لاحق يُتجاهل.
create or replace function public.aff_lock_sponsor()
returns trigger
language plpgsql
set search_path = public
as $$
begin
  if tg_op = 'UPDATE' and new.sponsor_id is distinct from old.sponsor_id then
    new.sponsor_id := old.sponsor_id;
  end if;
  return new;
end;
$$;

drop trigger if exists aff_lock_sponsor on public.aff_affiliates;
create trigger aff_lock_sponsor
  before update on public.aff_affiliates
  for each row execute function public.aff_lock_sponsor();

create or replace function public.aff_resolve_sponsor(p_code text, p_self uuid)
returns uuid
language plpgsql
stable
security definer
set search_path = public
as $$
declare
  sid uuid;
  walk uuid;
  seen uuid[] := '{}';
  steps int := 0;
begin
  if p_code is null or btrim(p_code) = '' then
    return null;
  end if;
  if upper(btrim(p_code)) !~ '^[A-Z0-9]{4,12}$' then
    return null;
  end if;
  select id into sid
  from public.aff_affiliates
  where referral_code = upper(btrim(p_code));
  if sid is null or sid = p_self then
    return null;
  end if;
  walk := sid;
  while walk is not null and steps < 12 loop
    if walk = p_self or walk = any (seen) then
      return null;
    end if;
    seen := array_append(seen, walk);
    steps := steps + 1;
    select sponsor_id into walk from public.aff_affiliates where id = walk;
  end loop;
  if walk is not null then
    return null;
  end if;
  return sid;
end;
$$;

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
  sponsor uuid;
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
    sponsor := public.aff_resolve_sponsor(new.raw_user_meta_data->>'sponsor', new.id);
    loop
      tries := tries + 1;
      new_code := upper(substr(md5(random()::text || clock_timestamp()::text || tries::text), 1, 6));
      begin
        insert into public.aff_affiliates (id, full_name, phone, email, referral_code, is_admin, sponsor_id)
        values (new.id, person_name, person_phone, new.email, new_code, false, sponsor)
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
  sponsor uuid;
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
  sponsor := public.aff_resolve_sponsor(meta->>'sponsor', uid);
  loop
    tries := tries + 1;
    new_code := upper(substr(md5(random()::text || clock_timestamp()::text || tries::text), 1, 6));
    begin
      insert into public.aff_affiliates (id, full_name, phone, email, referral_code, is_admin, sponsor_id)
      values (uid, person_name, person_phone, em, new_code, false, sponsor)
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

-- 10% من قيمة الحجز. بلا راعٍ: البائع 10%.
-- راعٍ واحد: البائع 5% والراعي 5%.
-- راعٍ وراعٍ للراعي: البائع 5%، الراعي 2.5%، والأعلى 2.5%. لا مستوى ثالث.
create or replace function public.aff_write_commissions(p_booking uuid)
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  b public.aff_bookings%rowtype;
  p1 uuid;
  p2 uuid;
  st text;
  seller numeric;
begin
  select * into b from public.aff_bookings where id = p_booking;
  if b.id is null then
    return;
  end if;
  delete from public.aff_commissions where booking_id = b.id;
  if b.amount is null or b.amount <= 0 then
    update public.aff_bookings
       set commission = null
     where id = b.id and commission is not null;
    return;
  end if;
  st := case b.status
    when 'confirmed' then 'confirmed'
    when 'cancelled' then 'rejected'
    else 'pending'
  end;
  select sponsor_id into p1 from public.aff_affiliates where id = b.affiliate_id;
  if p1 = b.affiliate_id then
    p1 := null;
  end if;
  if p1 is not null then
    select sponsor_id into p2 from public.aff_affiliates where id = p1;
  end if;
  if p2 = b.affiliate_id or p2 = p1 then
    p2 := null;
  end if;
  if p1 is null then
    insert into public.aff_commissions (booking_id, affiliate_id, level, rate, amount, status)
    values (b.id, b.affiliate_id, 0, 0.10, round(b.amount * 0.10, 2), st);
  elsif p2 is null then
    insert into public.aff_commissions (booking_id, affiliate_id, level, rate, amount, status)
    values
      (b.id, b.affiliate_id, 0, 0.05, round(b.amount * 0.05, 2), st),
      (b.id, p1, 1, 0.05, round(b.amount * 0.05, 2), st);
  else
    insert into public.aff_commissions (booking_id, affiliate_id, level, rate, amount, status)
    values
      (b.id, b.affiliate_id, 0, 0.05, round(b.amount * 0.05, 2), st),
      (b.id, p1, 1, 0.025, round(b.amount * 0.025, 2), st),
      (b.id, p2, 2, 0.025, round(b.amount * 0.025, 2), st);
  end if;
  select amount into seller
  from public.aff_commissions
  where booking_id = b.id and level = 0;
  update public.aff_bookings
     set commission = case when b.status = 'confirmed' then seller else null end
   where id = b.id
     and commission is distinct from (case when b.status = 'confirmed' then seller else null end);
end;
$$;

create or replace function public.aff_bookings_sync_commissions()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  if tg_op = 'UPDATE'
     and new.status is not distinct from old.status
     and new.amount is not distinct from old.amount
     and new.affiliate_id is not distinct from old.affiliate_id then
    return new;
  end if;
  if new.amount is null then
    return new;
  end if;
  perform public.aff_write_commissions(new.id);
  return new;
end;
$$;

drop trigger if exists aff_bookings_sync_commissions on public.aff_bookings;
create trigger aff_bookings_sync_commissions
  after insert or update on public.aff_bookings
  for each row execute function public.aff_bookings_sync_commissions();

-- p_amount هو قيمة الحجز بالدولار، لا مبلغ العمولة. تُقسَم العمولة في الخادم.
create or replace function public.aff_confirm_booking(
  p_id uuid,
  p_status text,
  p_amount numeric
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
  if p_amount is not null and p_amount < 0 then
    raise exception 'bad amount';
  end if;
  update public.aff_bookings
     set status = p_status,
         amount = case
           when p_status = 'pending' then null
           when p_status = 'confirmed' then p_amount
           else amount
         end,
         updated_at = now()
   where id = p_id
   returning * into row;
  if row.id is null then
    raise exception 'not found';
  end if;
  return row;
end;
$$;

create or replace function public.aff_my_team()
returns table (
  id uuid,
  full_name text,
  created_at timestamptz,
  depth int,
  bookings bigint
)
language sql
stable
security definer
set search_path = public
as $$
  select a.id, a.full_name, a.created_at, 1,
         (select count(*) from public.aff_bookings b where b.affiliate_id = a.id)
  from public.aff_affiliates a
  where a.sponsor_id = auth.uid()
  union all
  select c.id, c.full_name, c.created_at, 2,
         (select count(*) from public.aff_bookings b where b.affiliate_id = c.id)
  from public.aff_affiliates c
  join public.aff_affiliates p on p.id = c.sponsor_id
  where p.sponsor_id = auth.uid();
$$;

drop policy if exists aff_commissions_select_own on public.aff_commissions;
create policy aff_commissions_select_own
  on public.aff_commissions
  for select
  to authenticated
  using (affiliate_id = auth.uid() or public.aff_is_admin());

revoke all on public.aff_commissions from anon, authenticated;
grant select on public.aff_commissions to authenticated;

revoke all on function public.aff_resolve_sponsor(text, uuid) from public, anon, authenticated;
revoke all on function public.aff_write_commissions(uuid) from public, anon, authenticated;
revoke all on function public.aff_bookings_sync_commissions() from public, anon, authenticated;
revoke all on function public.aff_lock_sponsor() from public, anon, authenticated;

revoke all on function public.aff_confirm_booking(uuid, text, numeric) from public, anon, authenticated;
grant execute on function public.aff_confirm_booking(uuid, text, numeric) to authenticated;

revoke all on function public.aff_my_team() from public, anon, authenticated;
grant execute on function public.aff_my_team() to authenticated;

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
  a.sponsor_id,
  (select s.full_name from public.aff_affiliates s where s.id = a.sponsor_id) as sponsor_name,
  (select s.referral_code from public.aff_affiliates s where s.id = a.sponsor_id) as sponsor_code,
  (select count(*) from public.aff_referral_clicks c where c.affiliate_id = a.id) as clicks,
  (select count(*) from public.aff_bookings b where b.affiliate_id = a.id) as bookings,
  (select count(*) from public.aff_bookings b where b.affiliate_id = a.id and b.status = 'confirmed') as confirmed,
  (select coalesce(sum(b.commission), 0) from public.aff_bookings b where b.affiliate_id = a.id and b.status = 'confirmed') as commission
from public.aff_affiliates a;

revoke all on public.aff_affiliate_stats from anon, authenticated;
grant select on public.aff_affiliate_stats to authenticated;
