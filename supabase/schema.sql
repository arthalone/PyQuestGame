-- =====================================================================
-- PyQuest Online: banco de dados (Supabase / PostgreSQL)
-- Cole TUDO isto no SQL Editor do Supabase e clique em "Run".
-- Pode rodar de novo sem problemas (o script é idempotente).
-- =====================================================================

-- ---------- Itens do jogo e quanto XP cada um vale (definido no SERVIDOR) ----------
create table if not exists public.itens (
  id   text primary key,
  xp   int  not null check (xp >= 0),
  tipo text not null
);

insert into public.itens (id, xp, tipo) values
  ('c1-l0', 10, 'licao'),
  ('c1-l1', 10, 'licao'),
  ('c1-l2', 10, 'licao'),
  ('c1-quiz', 50, 'quiz'),
  ('c1-d0', 30, 'desafio'),
  ('c1-d1', 30, 'desafio'),
  ('c1-d2', 30, 'desafio'),
  ('c1-d3', 30, 'desafio'),
  ('c1-chefe', 100, 'chefe'),
  ('c2-l0', 10, 'licao'),
  ('c2-l1', 10, 'licao'),
  ('c2-l2', 10, 'licao'),
  ('c2-l3', 10, 'licao'),
  ('c2-quiz', 50, 'quiz'),
  ('c2-d0', 30, 'desafio'),
  ('c2-d1', 30, 'desafio'),
  ('c2-d2', 30, 'desafio'),
  ('c2-d3', 30, 'desafio'),
  ('c2-d4', 30, 'desafio'),
  ('c2-chefe', 100, 'chefe'),
  ('c3-l0', 10, 'licao'),
  ('c3-l1', 10, 'licao'),
  ('c3-l2', 10, 'licao'),
  ('c3-quiz', 50, 'quiz'),
  ('c3-d0', 30, 'desafio'),
  ('c3-d1', 30, 'desafio'),
  ('c3-d2', 30, 'desafio'),
  ('c3-d3', 30, 'desafio'),
  ('c3-d4', 30, 'desafio'),
  ('c3-chefe', 100, 'chefe'),
  ('c4-l0', 10, 'licao'),
  ('c4-l1', 10, 'licao'),
  ('c4-l2', 10, 'licao'),
  ('c4-l3', 10, 'licao'),
  ('c4-quiz', 50, 'quiz'),
  ('c4-d0', 30, 'desafio'),
  ('c4-d1', 30, 'desafio'),
  ('c4-d2', 30, 'desafio'),
  ('c4-d3', 30, 'desafio'),
  ('c4-d4', 30, 'desafio'),
  ('c4-d5', 30, 'desafio'),
  ('c4-chefe', 100, 'chefe'),
  ('c5-l0', 10, 'licao'),
  ('c5-l1', 10, 'licao'),
  ('c5-l2', 10, 'licao'),
  ('c5-quiz', 50, 'quiz'),
  ('c5-d0', 30, 'desafio'),
  ('c5-d1', 30, 'desafio'),
  ('c5-d2', 30, 'desafio'),
  ('c5-d3', 30, 'desafio'),
  ('c5-d4', 30, 'desafio'),
  ('c5-chefe', 100, 'chefe'),
  ('c6-l0', 10, 'licao'),
  ('c6-l1', 10, 'licao'),
  ('c6-l2', 10, 'licao'),
  ('c6-quiz', 50, 'quiz'),
  ('c6-d0', 30, 'desafio'),
  ('c6-d1', 30, 'desafio'),
  ('c6-d2', 30, 'desafio'),
  ('c6-d3', 30, 'desafio'),
  ('c6-d4', 30, 'desafio'),
  ('c6-chefe', 100, 'chefe'),
  ('c7-l0', 10, 'licao'),
  ('c7-l1', 10, 'licao'),
  ('c7-l2', 10, 'licao'),
  ('c7-quiz', 50, 'quiz'),
  ('c7-d0', 30, 'desafio'),
  ('c7-d1', 30, 'desafio'),
  ('c7-d2', 30, 'desafio'),
  ('c7-d3', 30, 'desafio'),
  ('c7-d4', 30, 'desafio'),
  ('c7-d5', 30, 'desafio'),
  ('c7-chefe', 100, 'chefe'),
  ('c8-l0', 10, 'licao'),
  ('c8-l1', 10, 'licao'),
  ('c8-l2', 10, 'licao'),
  ('c8-l3', 10, 'licao'),
  ('c8-quiz', 50, 'quiz'),
  ('c8-d0', 30, 'desafio'),
  ('c8-d1', 30, 'desafio'),
  ('c8-d2', 30, 'desafio'),
  ('c8-d3', 30, 'desafio'),
  ('c8-d4', 30, 'desafio'),
  ('c8-d5', 30, 'desafio'),
  ('c8-chefe', 100, 'chefe'),
  ('c9-l0', 10, 'licao'),
  ('c9-l1', 10, 'licao'),
  ('c9-l2', 10, 'licao'),
  ('c9-l3', 10, 'licao'),
  ('c9-quiz', 50, 'quiz'),
  ('c9-d0', 30, 'desafio'),
  ('c9-d1', 30, 'desafio'),
  ('c9-d2', 30, 'desafio'),
  ('c9-d3', 30, 'desafio'),
  ('c9-d4', 30, 'desafio'),
  ('c9-d5', 30, 'desafio'),
  ('c9-chefe', 100, 'chefe'),
  ('c10-l0', 10, 'licao'),
  ('c10-l1', 10, 'licao'),
  ('c10-l2', 10, 'licao'),
  ('c10-l3', 10, 'licao'),
  ('c10-quiz', 50, 'quiz'),
  ('c10-d0', 30, 'desafio'),
  ('c10-d1', 30, 'desafio'),
  ('c10-d2', 30, 'desafio'),
  ('c10-d3', 30, 'desafio'),
  ('c10-d4', 30, 'desafio'),
  ('c10-d5', 30, 'desafio'),
  ('c10-chefe', 100, 'chefe'),
  ('c11-l0', 10, 'licao'),
  ('c11-l1', 10, 'licao'),
  ('c11-l2', 10, 'licao'),
  ('c11-quiz', 50, 'quiz'),
  ('c11-d0', 30, 'desafio'),
  ('c11-d1', 30, 'desafio'),
  ('c11-d2', 30, 'desafio'),
  ('c11-d3', 30, 'desafio'),
  ('c11-d4', 30, 'desafio'),
  ('c11-chefe', 100, 'chefe'),
  ('c12-l0', 10, 'licao'),
  ('c12-l1', 10, 'licao'),
  ('c12-l2', 10, 'licao'),
  ('c12-l3', 10, 'licao'),
  ('c12-quiz', 50, 'quiz'),
  ('c12-d0', 30, 'desafio'),
  ('c12-d1', 30, 'desafio'),
  ('c12-d2', 30, 'desafio'),
  ('c12-d3', 30, 'desafio'),
  ('c12-d4', 30, 'desafio'),
  ('c12-d5', 30, 'desafio'),
  ('c12-chefe', 100, 'chefe'),
  ('c13-l0', 10, 'licao'),
  ('c13-l1', 10, 'licao'),
  ('c13-l2', 10, 'licao'),
  ('c13-l3', 10, 'licao'),
  ('c13-quiz', 50, 'quiz'),
  ('c13-d0', 30, 'desafio'),
  ('c13-d1', 30, 'desafio'),
  ('c13-d2', 30, 'desafio'),
  ('c13-d3', 30, 'desafio'),
  ('c13-d4', 30, 'desafio'),
  ('c13-d5', 30, 'desafio'),
  ('c13-chefe', 100, 'chefe'),
  ('c14-l0', 10, 'licao'),
  ('c14-l1', 10, 'licao'),
  ('c14-l2', 10, 'licao'),
  ('c14-l3', 10, 'licao'),
  ('c14-quiz', 50, 'quiz'),
  ('c14-d0', 30, 'desafio'),
  ('c14-d1', 30, 'desafio'),
  ('c14-d2', 30, 'desafio'),
  ('c14-d3', 30, 'desafio'),
  ('c14-d4', 30, 'desafio'),
  ('c14-d5', 30, 'desafio'),
  ('c14-chefe', 100, 'chefe')
on conflict (id) do update set xp = excluded.xp, tipo = excluded.tipo;

-- ---------- Perfis públicos (apelido aparece no ranking) ----------
create table if not exists public.perfis (
  id        uuid primary key references auth.users(id) on delete cascade,
  apelido   text not null,
  criado_em timestamptz not null default now(),
  constraint apelido_tamanho check (char_length(apelido) between 3 and 20),
  constraint apelido_chars  check (apelido ~ '^[A-Za-zÀ-ÿ0-9_. -]+$')
);
create unique index if not exists perfis_apelido_unico on public.perfis (lower(apelido));

-- ---------- Progresso: um registro por item concluído ----------
create table if not exists public.progresso (
  user_id      uuid not null references auth.users(id) on delete cascade,
  item_id      text not null references public.itens(id),
  ajuda        text not null default 'nenhuma' check (ajuda in ('nenhuma', 'dica', 'solucao')),
  xp           int  not null default 0,
  concluido_em timestamptz not null default now(),
  primary key (user_id, item_id)
);
create index if not exists progresso_quando on public.progresso (concluido_em);

-- ---------- Bônus diário (1 por dia, horário de Brasília) ----------
create table if not exists public.bonus_diario (
  user_id   uuid not null references auth.users(id) on delete cascade,
  dia       date not null default (now() at time zone 'America/Sao_Paulo')::date,
  xp        int  not null default 10,
  criado_em timestamptz not null default now(),
  primary key (user_id, dia)
);

-- ---------- Partidas do Desafio Relâmpago ----------
create table if not exists public.relampago (
  id        bigint generated always as identity primary key,
  user_id   uuid not null references auth.users(id) on delete cascade,
  acertos   int  not null check (acertos between 0 and 60),
  criado_em timestamptz not null default now()
);
create index if not exists relampago_user on public.relampago (user_id, criado_em desc);

-- =====================================================================
-- Gatilhos: o servidor decide dono, data e XP (o navegador não manda nisso)
-- =====================================================================
create or replace function public.tg_progresso() returns trigger
language plpgsql security definer set search_path = public as $$
declare base int;
begin
  select xp into base from public.itens where id = new.item_id;
  if base is null then
    raise exception 'Item inválido: %', new.item_id;
  end if;
  new.user_id := auth.uid();
  new.concluido_em := now();
  new.xp := case new.ajuda when 'solucao' then 5 when 'dica' then base / 2 else base end;
  return new;
end $$;

drop trigger if exists progresso_xp on public.progresso;
create trigger progresso_xp before insert on public.progresso
  for each row execute function public.tg_progresso();

create or replace function public.tg_bonus() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  new.user_id := auth.uid();
  new.dia := (now() at time zone 'America/Sao_Paulo')::date;
  new.xp := 10;
  new.criado_em := now();
  return new;
end $$;

drop trigger if exists bonus_regras on public.bonus_diario;
create trigger bonus_regras before insert on public.bonus_diario
  for each row execute function public.tg_bonus();

create or replace function public.tg_relampago() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  new.user_id := auth.uid();
  new.criado_em := now();
  -- uma partida dura 60 s: impede envios em rajada
  if exists (select 1 from public.relampago
             where user_id = new.user_id and criado_em > now() - interval '50 seconds') then
    raise exception 'Calma! Espere a partida terminar.';
  end if;
  return new;
end $$;

drop trigger if exists relampago_regras on public.relampago;
create trigger relampago_regras before insert on public.relampago
  for each row execute function public.tg_relampago();

-- Perfil criado automaticamente no primeiro login, com apelido anônimo
create or replace function public.tg_novo_usuario() returns trigger
language plpgsql security definer set search_path = public as $$
declare nome text;
begin
  loop
    nome := 'Jogador' || ((1000 + floor(random() * 99000))::int)::text;
    exit when not exists (select 1 from public.perfis where lower(apelido) = lower(nome));
  end loop;
  insert into public.perfis (id, apelido) values (new.id, nome) on conflict (id) do nothing;
  return new;
end $$;

drop trigger if exists pyquest_novo_usuario on auth.users;
create trigger pyquest_novo_usuario after insert on auth.users
  for each row execute function public.tg_novo_usuario();

-- =====================================================================
-- Segurança (Row Level Security)
-- =====================================================================
alter table public.itens        enable row level security;
alter table public.perfis       enable row level security;
alter table public.progresso    enable row level security;
alter table public.bonus_diario enable row level security;
alter table public.relampago    enable row level security;

drop policy if exists itens_ler on public.itens;
create policy itens_ler on public.itens for select using (true);

drop policy if exists perfis_ler on public.perfis;
create policy perfis_ler on public.perfis for select using (true);
drop policy if exists perfis_editar on public.perfis;
create policy perfis_editar on public.perfis for update
  using (id = auth.uid()) with check (id = auth.uid());
drop policy if exists perfis_criar on public.perfis;
create policy perfis_criar on public.perfis for insert with check (id = auth.uid());

drop policy if exists progresso_ler on public.progresso;
create policy progresso_ler on public.progresso for select using (user_id = auth.uid());
drop policy if exists progresso_criar on public.progresso;
create policy progresso_criar on public.progresso for insert with check (user_id = auth.uid());
drop policy if exists progresso_apagar on public.progresso;
create policy progresso_apagar on public.progresso for delete using (user_id = auth.uid());

drop policy if exists bonus_ler on public.bonus_diario;
create policy bonus_ler on public.bonus_diario for select using (user_id = auth.uid());
drop policy if exists bonus_criar on public.bonus_diario;
create policy bonus_criar on public.bonus_diario for insert with check (user_id = auth.uid());
drop policy if exists bonus_apagar on public.bonus_diario;
create policy bonus_apagar on public.bonus_diario for delete using (user_id = auth.uid());

drop policy if exists relampago_ler on public.relampago;
create policy relampago_ler on public.relampago for select using (user_id = auth.uid());
drop policy if exists relampago_criar on public.relampago;
create policy relampago_criar on public.relampago for insert with check (user_id = auth.uid());
drop policy if exists relampago_apagar on public.relampago;
create policy relampago_apagar on public.relampago for delete using (user_id = auth.uid());

-- =====================================================================
-- Rankings (leitura pública, mesmo sem login)
-- =====================================================================
create or replace function public.ranking(periodo text default 'geral', limite int default 50)
returns table (posicao bigint, user_id uuid, apelido text, xp bigint, chefes bigint)
language sql stable security definer set search_path = public as $$
  with inicio as (
    select case when periodo = 'semana'
      then (date_trunc('week', now() at time zone 'America/Sao_Paulo') at time zone 'America/Sao_Paulo')
      else '-infinity'::timestamptz end as t
  ),
  eventos as (
    select p.user_id, p.xp, p.item_id, p.concluido_em as quando from public.progresso p
    union all
    select b.user_id, b.xp, 'bonus', b.criado_em from public.bonus_diario b
  ),
  somas as (
    select e.user_id, sum(e.xp)::bigint as xp,
           count(*) filter (where e.item_id like '%-chefe') as chefes,
           max(e.quando) as ultimo
    from eventos e, inicio
    where e.quando >= inicio.t
    group by e.user_id
  ),
  ordenado as (
    select rank() over (order by s.xp desc, s.ultimo asc) as posicao,
           s.user_id, pf.apelido, s.xp, s.chefes
    from somas s join public.perfis pf on pf.id = s.user_id
  )
  select o.posicao, o.user_id, o.apelido, o.xp, o.chefes from ordenado o
  where o.posicao <= least(greatest(limite, 1), 200) or o.user_id = auth.uid()
  order by o.posicao;
$$;

create or replace function public.ranking_relampago(limite int default 50)
returns table (posicao bigint, user_id uuid, apelido text, acertos int)
language sql stable security definer set search_path = public as $$
  with melhor as (
    select r.user_id, max(r.acertos) as acertos, min(r.criado_em) as quando
    from public.relampago r
    group by r.user_id
  ),
  ordenado as (
    select rank() over (order by m.acertos desc, m.quando asc) as posicao,
           m.user_id, pf.apelido, m.acertos
    from melhor m join public.perfis pf on pf.id = m.user_id
    where m.acertos > 0
  )
  select o.posicao, o.user_id, o.apelido, o.acertos from ordenado o
  where o.posicao <= least(greatest(limite, 1), 200) or o.user_id = auth.uid()
  order by o.posicao;
$$;

grant execute on function public.ranking(text, int) to anon, authenticated;
grant execute on function public.ranking_relampago(int) to anon, authenticated;
