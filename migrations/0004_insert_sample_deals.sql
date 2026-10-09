insert into deals(company_id,title,amount,status,expected_close,metadata)
values
((select id from companies where domain='zylensolutions.com'),'CRM Automation', 250000.00, 'won', '2026-09-30', '{"source":"referral","priority":"high"}'),
((select id from companies where domain='google.com'),'AI Revenue Platform', 750000.00, 'won', '2026-10-15', '{"source":"website","priority":"medium"}'),
((select id from companies where domain='zoho.com'),'Sales Automation', 400000.00, 'negotiation', '2026-10-05', '{"source":"referral","priority":"high"}'),
((select id from companies where domain='amazon.com'),'Cloud Revenue System', 1200000.00, 'proposal', '2026-11-01', '{"source":"website","priority":"high"}'),
((select id from companies where domain='tesla.com'),'AI Analytics', 600000.00, 'lost', NULL, '{"source":"partner","priority":"low"}')
returning * ;