create table deals(
    id uuid primary key default gen_random_uuid(),
    company_id uuid not null references companies(id),
    title text not null,
    amount numeric(14,2) check(amount>=0),
    status text not null,
    expected_close timestamptz,
    metadata jsonb,
    created_at timestamptz not null default current_timestamp
);