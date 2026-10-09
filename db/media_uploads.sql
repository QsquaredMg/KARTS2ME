-- Applied to production 2026-10-09 (record only)
alter table public.vehicles add column if not exists photo_url text;
alter table public.vehicle_types add column if not exists photo_url text;
alter table public.drivers add column if not exists id_photo_path text;
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('operator-media','operator-media', true, 5242880, array['image/jpeg','image/png','image/webp']) on conflict (id) do nothing;
-- storage.objects policies: operators insert/update/delete only under their own operator-id folder (admins anywhere)
