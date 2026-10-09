insert into companies(name,domain,industry,employees,active,metadata)
values('Zylen Solutions', 'zylensolutions.com', 'Software', 50, true,'{"source": "referral", "priority": "high"}'),
('Google', 'google.com', 'Technology', 180000, true,'{"source": "website", "priority": "medium"}'),
('Zoho', 'zoho.com', 'Software', 15000, true,'{"source": "referral", "priority": "high"}'),
('Amazon', 'amazon.com', 'E-commerce', 1500000, true,'{"source": "website", "priority": "low"}'),
('Tesla', 'tesla.com', 'Automotive', 140000, false,'{"source": "partner", "priority": "medium"}')
returning *;