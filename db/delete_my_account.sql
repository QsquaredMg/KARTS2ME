-- In-app account deletion (required by Apple App Store 5.1.1(v) and Google Play).
-- Run once in Supabase Dashboard -> SQL Editor.
-- Returns: 1 = fully deleted, 2 = anonymized (ride/payment history kept for legal & accounting),
--          -1 = not signed in, -2 = has an active ride, -3 = staff/admin account (remove via admin).
create or replace function public.delete_my_account() returns integer
language plpgsql security definer set search_path to 'public' as $f$
declare
  v_uid uuid := auth.uid();
  v_role text;
begin
  if v_uid is null then return -1; end if;
  select role::text into v_role from public.profiles where id = v_uid;
  if v_role in ('platform_admin','operator_staff') then return -3; end if;
  if exists (select 1 from public.rides where (primary_rider_id = v_uid or driver_id = v_uid)
             and status in ('requested','matching','assigned','in_progress')) then
    return -2;
  end if;

  -- Full delete when there is no history that must be preserved
  begin
    delete from auth.users where id = v_uid;
    return 1;
  exception when foreign_key_violation then
    null;
  end;

  -- Otherwise anonymize: strip personal data, lock the login, keep ride & payment records
  delete from public.push_subscriptions where user_id = v_uid;
  update public.profiles set full_name = 'Deleted user', phone = null, photo_url = null where id = v_uid;
  update public.drivers set is_online = false, current_lat = null, current_lng = null, location_updated_at = null where id = v_uid;
  delete from auth.sessions where user_id = v_uid;
  delete from auth.identities where user_id = v_uid;
  update auth.users set
    email = 'deleted-' || v_uid::text || '@deleted.invalid',
    phone = null,
    encrypted_password = null,
    raw_user_meta_data = '{}'::jsonb,
    raw_app_meta_data = '{}'::jsonb,
    banned_until = 'infinity'
  where id = v_uid;
  return 2;
end;
$f$;
revoke all on function public.delete_my_account() from public, anon;
grant execute on function public.delete_my_account() to authenticated;
