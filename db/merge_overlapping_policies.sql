-- Merge overlapping permissive RLS policies (clears 45 "multiple_permissive_policies" advisor warnings).
-- Behavior-preserving. Run once in Supabase Dashboard -> SQL Editor (needs DROP POLICY permission). Runs in one transaction.
begin;

-- 1) FOR ALL operator policies -> separate INSERT/UPDATE/DELETE, so SELECT no longer overlaps the read policy
do $$
declare t text; old text; ex text;
begin
  for t, old in select * from (values
    ('events','operator writes own events'),
    ('operator_pricing','operator writes own pricing'),
    ('vehicle_types','operator writes own vehicle_types'),
    ('vehicles','operator writes own vehicles')) v(t,o)
  loop
    ex := '((operator_id = (select my_operator_id())) or (select is_platform_admin()))';
    execute format('create policy %I on public.%I for insert with check %s', 'operator inserts own '||t, t, ex);
    execute format('create policy %I on public.%I for update using %s with check %s', 'operator updates own '||t, t, ex, ex);
    execute format('create policy %I on public.%I for delete using %s', 'operator deletes own '||t, t, ex);
    execute format('drop policy %I on public.%I', old, t);
  end loop;
end $$;

create policy "operator inserts own event_drivers" on public.event_drivers for insert
  with check ((exists (select 1 from events e where e.id = event_drivers.event_id and e.operator_id = (select my_operator_id()))) or (select is_platform_admin()));
create policy "operator updates own event_drivers" on public.event_drivers for update
  using ((exists (select 1 from events e where e.id = event_drivers.event_id and e.operator_id = (select my_operator_id()))) or (select is_platform_admin()))
  with check ((exists (select 1 from events e where e.id = event_drivers.event_id and e.operator_id = (select my_operator_id()))) or (select is_platform_admin()));
create policy "operator deletes own event_drivers" on public.event_drivers for delete
  using ((exists (select 1 from events e where e.id = event_drivers.event_id and e.operator_id = (select my_operator_id()))) or (select is_platform_admin()));
drop policy "operator manages own event roster" on public.event_drivers;

-- 2) drivers UPDATE (the second policy's WITH CHECK was already 'true', so the merged check is true)
alter policy "driver updates own" on public.drivers
  using ((id = (select auth.uid())) or (select is_platform_admin()) or ((select my_operator_id()) is not null))
  with check (true);
drop policy "operator can update drivers for employment assignment" on public.drivers;

-- 3) ride_bids SELECT
alter policy "driver can view own bids" on public.ride_bids
  using ((driver_id = (select auth.uid()))
    or (exists (select 1 from rides r where r.id = ride_bids.ride_id and r.primary_rider_id = (select auth.uid())))
    or (select is_platform_admin()));
drop policy "rider can view bids on own ride" on public.ride_bids;

-- 4) rides SELECT
alter policy "rider reads own rides" on public.rides
  using ((primary_rider_id = (select auth.uid())) or (driver_id = (select auth.uid())) or (select is_platform_admin())
    or ((status = 'requested'::ride_status) and (driver_id is null) and exists (select 1 from drivers d where d.id = (select auth.uid()))));
drop policy "drivers see open ride requests" on public.rides;

-- 5) rides UPDATE
alter policy "rider or driver updates ride" on public.rides
  using ((primary_rider_id = (select auth.uid())) or (driver_id = (select auth.uid())) or (select is_platform_admin())
    or ((status = 'requested'::ride_status) and (driver_id is null) and exists (select 1 from drivers d where d.id = (select auth.uid()))))
  with check ((primary_rider_id = (select auth.uid())) or (driver_id = (select auth.uid())) or (select is_platform_admin()));
drop policy "drivers claim open rides" on public.rides;

commit;
