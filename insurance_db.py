"""
Insurance Database Creation Script - Updated Version
Markets: Middle Market, National Program, National Account, Public Sector
Policy Types: GC (Guaranteed Cost), LS (Loss Sensitive)
"""

import sqlite3
from datetime import datetime, timedelta
import random

print("="*70)
print("Creating Updated Insurance Database...")
print("="*70)

## Connect to SQLite
connection = sqlite3.connect("insurance.db")
cursor = connection.cursor()

## Drop existing tables if they exist
print("\n[1/7] Dropping existing tables (if any)...")
cursor.execute('DROP TABLE IF EXISTS claims')
cursor.execute('DROP TABLE IF EXISTS payments')
cursor.execute('DROP TABLE IF EXISTS policies')
cursor.execute('DROP TABLE IF EXISTS account')
cursor.execute('DROP TABLE IF EXISTS agents')
cursor.execute('DROP TABLE IF EXISTS ongoing_claims')
cursor.execute('DROP TABLE IF EXISTS quoted_policies')
cursor.execute('DROP TABLE IF EXISTS issued_policies')
print("✓ Existing tables dropped")

## Create Tables
print("\n[2/7] Creating database schema...")

# 1. ACCOUNTS table (renamed from customers)
cursor.execute('''
CREATE TABLE account (
    account_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    address VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    date_of_birth DATE,
    gender VARCHAR(10)
)
''')
print("✓ Created ACCOUNTS table")

# 2. AGENTS table
cursor.execute('''
CREATE TABLE agents (
    agent_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    city VARCHAR(50),
    commission_rate DECIMAL(5,2),
    join_date DATE,
    status VARCHAR(20)
)
''')
print("✓ Created AGENTS table")

# 3. POLICIES table (UPDATED with new market types and policy types)
cursor.execute('''
CREATE TABLE policies (
    policy_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    agent_id INTEGER,
    market_type VARCHAR(50),
    policy_type VARCHAR(50),
    policy_number VARCHAR(50),
    start_date DATE,
    end_date DATE,
    premium_amount DECIMAL(10,2),
    coverage_amount DECIMAL(12,2),
    status VARCHAR(20),
    FOREIGN KEY (account_id) REFERENCES account(account_id),
    FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
)
''')
print("✓ Created POLICIES table")

# 4. CLAIMS table
cursor.execute('''
CREATE TABLE claims (
    claim_id INTEGER PRIMARY KEY,
    policy_id INTEGER,
    account_id INTEGER,
    claim_number VARCHAR(50),
    claim_date DATE,
    claim_amount DECIMAL(10,2),
    approved_amount DECIMAL(10,2),
    claim_type VARCHAR(50),
    status VARCHAR(20),
    settlement_date DATE,
    FOREIGN KEY (policy_id) REFERENCES policies(policy_id),
    FOREIGN KEY (account_id) REFERENCES account(account_id)
)
''')
print("✓ Created CLAIMS table")

# 5. PAYMENTS table
cursor.execute('''
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    policy_id INTEGER,
    account_id INTEGER,
    payment_date DATE,
    amount DECIMAL(10,2),
    payment_method VARCHAR(30),
    status VARCHAR(20),
    FOREIGN KEY (policy_id) REFERENCES policies(policy_id),
    FOREIGN KEY (account_id) REFERENCES account(account_id)
)
''')
print("✓ Created PAYMENTS table")

# 6. ONGOING_CLAIMS table (NEW)
cursor.execute('''
CREATE TABLE ongoing_claims (
    ongoing_claim_id INTEGER PRIMARY KEY,
    policy_id INTEGER,
    account_id INTEGER,
    claim_number VARCHAR(50),
    claim_date DATE,
    claim_amount DECIMAL(10,2),
    current_status VARCHAR(50),
    assigned_adjuster VARCHAR(100),
    last_update_date DATE,
    FOREIGN KEY (policy_id) REFERENCES policies(policy_id),
    FOREIGN KEY (account_id) REFERENCES account(account_id)
)
''')
print("✓ Created ONGOING_CLAIMS table")

# 7. QUOTED_POLICIES table (NEW)
cursor.execute('''
CREATE TABLE quoted_policies (
    quote_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    agent_id INTEGER,
    market_type VARCHAR(50),
    policy_type VARCHAR(50),
    quote_number VARCHAR(50),
    quote_date DATE,
    quoted_premium DECIMAL(10,2),
    quoted_coverage DECIMAL(12,2),
    quote_status VARCHAR(20),
    expiry_date DATE,
    FOREIGN KEY (account_id) REFERENCES account(account_id),
    FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
)
''')
print("✓ Created QUOTED_POLICIES table")

# 8. ISSUED_POLICIES table (NEW)
cursor.execute('''
CREATE TABLE issued_policies (
    issue_id INTEGER PRIMARY KEY,
    policy_id INTEGER,
    account_id INTEGER,
    issue_date DATE,
    issued_by VARCHAR(100),
    delivery_method VARCHAR(50),
    confirmation_number VARCHAR(50),
    FOREIGN KEY (policy_id) REFERENCES policies(policy_id),
    FOREIGN KEY (account_id) REFERENCES account(account_id)
)
''')
print("✓ Created ISSUED_POLICIES table")

## Insert Sample Data
print("\n[3/7] Inserting sample data...")

# Insert Accounts (20 accounts)
accounts_data = [
    (1, 'Acme Corporation', 'contact@acmecorp.com', '555-0101', '123 Business Ave', 'New York', 'NY', '10001', '1990-03-15', 'Corporate'),
    (2, 'TechStart Inc', 'info@techstart.com', '555-0102', '456 Innovation Dr', 'San Francisco', 'CA', '94102', '1995-07-22', 'Corporate'),
    (3, 'Global Manufacturing Ltd', 'contact@globalmfg.com', '555-0103', '789 Industrial Rd', 'Chicago', 'IL', '60601', '1985-11-30', 'Corporate'),
    (4, 'Healthcare Plus', 'info@healthplus.com', '555-0104', '321 Medical Center', 'Houston', 'TX', '77001', '2000-05-18', 'Corporate'),
    (5, 'City School District', 'admin@cityschools.edu', '555-0105', '654 Education Blvd', 'Phoenix', 'AZ', '85001', '1975-09-25', 'Public'),
    (6, 'Metro Transit Authority', 'contact@metrotransit.gov', '555-0106', '987 Transit Hub', 'Philadelphia', 'PA', '19101', '1980-12-08', 'Public'),
    (7, 'Premier Hotels Group', 'info@premierhotels.com', '555-0107', '147 Hospitality Way', 'Las Vegas', 'NV', '89101', '1998-04-14', 'Corporate'),
    (8, 'Construction Builders Co', 'contact@builders.com', '555-0108', '258 Construction Ave', 'Dallas', 'TX', '75201', '1992-08-03', 'Corporate'),
    (9, 'Retail Chain Stores', 'info@retailchain.com', '555-0109', '369 Shopping Plaza', 'Miami', 'FL', '33101', '1988-01-20', 'Corporate'),
    (10, 'Financial Services Group', 'contact@finservices.com', '555-0110', '741 Finance St', 'Boston', 'MA', '02101', '1995-06-11', 'Corporate'),
    (11, 'State University System', 'admin@stateuniv.edu', '555-0111', '852 Campus Dr', 'Austin', 'TX', '78701', '1970-02-28', 'Public'),
    (12, 'Regional Hospital Network', 'info@regionalhospital.com', '555-0112', '963 Healthcare Pkwy', 'Seattle', 'WA', '98101', '1982-09-17', 'Corporate'),
    (13, 'Energy Solutions Corp', 'contact@energysol.com', '555-0113', '159 Power Ave', 'Denver', 'CO', '80201', '1990-12-05', 'Corporate'),
    (14, 'Logistics International', 'info@logisticsintl.com', '555-0114', '357 Shipping Rd', 'Atlanta', 'GA', '30301', '1996-04-23', 'Corporate'),
    (15, 'County Government', 'admin@countygov.gov', '555-0115', '753 Government Plaza', 'Sacramento', 'CA', '95814', '1965-08-30', 'Public'),
    (16, 'Insurance Brokers LLC', 'contact@insbrokers.com', '555-0116', '951 Financial Center', 'Charlotte', 'NC', '28201', '2001-03-12', 'Corporate'),
    (17, 'Manufacturing Excellence', 'info@mfgexcel.com', '555-0117', '753 Factory Rd', 'Detroit', 'MI', '48201', '1987-11-22', 'Corporate'),
    (18, 'Public Library System', 'admin@publiclibrary.gov', '555-0118', '159 Knowledge Way', 'Portland', 'OR', '97201', '1968-05-15', 'Public'),
    (19, 'Tech Innovation Hub', 'contact@techhub.com', '555-0119', '357 Silicon Valley', 'San Jose', 'CA', '95101', '2005-07-08', 'Corporate'),
    (20, 'Transportation Department', 'info@transport.gov', '555-0120', '852 Transit Center', 'Washington', 'DC', '20001', '1960-01-10', 'Public')
]

cursor.executemany('INSERT INTO account VALUES (?,?,?,?,?,?,?,?,?,?)', accounts_data)
print(f"✓ Inserted {len(accounts_data)} accounts")

# Insert Agents
agents_data = [
    (1, 'Sarah Mitchell', 'sarah.mitchell@insurance.com', '555-1001', 'New York', 5.5, '2018-01-15', 'Active'),
    (2, 'Robert Chen', 'robert.chen@insurance.com', '555-1002', 'San Francisco', 6.0, '2019-03-20', 'Active'),
    (3, 'Maria Garcia', 'maria.garcia@insurance.com', '555-1003', 'Chicago', 5.0, '2020-06-10', 'Active'),
    (4, 'James Wilson', 'james.wilson@insurance.com', '555-1004', 'Houston', 5.5, '2017-11-05', 'Active'),
    (5, 'Jennifer Lee', 'jennifer.lee@insurance.com', '555-1005', 'Phoenix', 6.5, '2021-02-18', 'Active'),
    (6, 'Michael Brown', 'michael.brown@insurance.com', '555-1006', 'Philadelphia', 5.0, '2019-08-12', 'Active'),
    (7, 'Lisa Anderson', 'lisa.anderson@insurance.com', '555-1007', 'Seattle', 6.0, '2020-01-25', 'Active'),
    (8, 'David Martinez', 'david.martinez@insurance.com', '555-1008', 'Boston', 5.5, '2018-09-30', 'Active')
]

cursor.executemany('INSERT INTO agents VALUES (?,?,?,?,?,?,?,?)', agents_data)
print(f"✓ Inserted {len(agents_data)} agents")

# Insert Policies (UPDATED with new market types and policy types)
# Market Types: Middle Market, National Program, National Account, Public Sector
# Policy Types: GC (Guaranteed Cost), LS (Loss Sensitive)
policies_data = [
    (1, 1, 1, 'Middle Market', 'GC', 'POL-2023-001', '2023-01-15', '2024-01-15', 45000.00, 5000000.00, 'Active'),
    (2, 2, 2, 'National Program', 'LS', 'POL-2023-002', '2023-02-20', '2024-02-20', 78000.00, 8000000.00, 'Active'),
    (3, 3, 3, 'National Account', 'GC', 'POL-2023-003', '2023-03-10', '2024-03-10', 125000.00, 15000000.00, 'Active'),
    (4, 4, 1, 'Middle Market', 'LS', 'POL-2023-004', '2023-04-05', '2024-04-05', 56000.00, 6500000.00, 'Active'),
    (5, 5, 4, 'Public Sector', 'GC', 'POL-2023-005', '2023-05-12', '2024-05-12', 95000.00, 12000000.00, 'Active'),
    (6, 6, 4, 'Public Sector', 'GC', 'POL-2023-006', '2023-06-18', '2024-06-18', 87000.00, 10000000.00, 'Active'),
    (7, 7, 2, 'National Program', 'LS', 'POL-2023-007', '2023-07-22', '2024-07-22', 64000.00, 7500000.00, 'Active'),
    (8, 8, 3, 'Middle Market', 'GC', 'POL-2023-008', '2023-08-30', '2024-08-30', 52000.00, 6000000.00, 'Active'),
    (9, 9, 5, 'National Account', 'LS', 'POL-2023-009', '2023-09-15', '2024-09-15', 135000.00, 18000000.00, 'Active'),
    (10, 10, 5, 'Middle Market', 'GC', 'POL-2023-010', '2023-10-20', '2024-10-20', 48000.00, 5500000.00, 'Active'),
    (11, 11, 4, 'Public Sector', 'GC', 'POL-2023-011', '2023-11-05', '2024-11-05', 92000.00, 11000000.00, 'Active'),
    (12, 12, 6, 'National Program', 'LS', 'POL-2023-012', '2023-12-10', '2024-12-10', 71000.00, 8500000.00, 'Expired'),
    (13, 13, 7, 'National Account', 'GC', 'POL-2024-013', '2024-01-08', '2025-01-08', 142000.00, 20000000.00, 'Active'),
    (14, 14, 8, 'Middle Market', 'LS', 'POL-2024-014', '2024-01-15', '2025-01-15', 59000.00, 7000000.00, 'Active'),
    (15, 15, 4, 'Public Sector', 'GC', 'POL-2024-015', '2024-01-22', '2025-01-22', 88000.00, 9500000.00, 'Active'),
    (16, 16, 1, 'National Program', 'LS', 'POL-2024-016', '2024-02-01', '2025-02-01', 68000.00, 7800000.00, 'Active'),
    (17, 17, 2, 'Middle Market', 'GC', 'POL-2024-017', '2024-02-10', '2025-02-10', 54000.00, 6200000.00, 'Active'),
    (18, 18, 4, 'Public Sector', 'GC', 'POL-2024-018', '2024-02-15', '2025-02-15', 79000.00, 9000000.00, 'Active'),
    (19, 19, 3, 'National Account', 'LS', 'POL-2024-019', '2024-03-01', '2025-03-01', 155000.00, 22000000.00, 'Active'),
    (20, 20, 4, 'Public Sector', 'GC', 'POL-2024-020', '2024-03-12', '2025-03-12', 97000.00, 11500000.00, 'Active'),
    (21, 1, 6, 'Middle Market', 'LS', 'POL-2024-021', '2024-04-01', '2025-04-01', 47000.00, 5800000.00, 'Active'),
    (22, 3, 7, 'National Account', 'GC', 'POL-2024-022', '2024-04-10', '2025-04-10', 138000.00, 19000000.00, 'Active'),
    (23, 7, 8, 'National Program', 'LS', 'POL-2024-023', '2024-04-15', '2025-04-15', 72000.00, 8200000.00, 'Active'),
    (24, 9, 5, 'National Account', 'GC', 'POL-2024-024', '2024-05-01', '2025-05-01', 148000.00, 21000000.00, 'Active'),
    (25, 2, 1, 'National Program', 'LS', 'POL-2024-025', '2024-05-10', '2025-05-10', 76000.00, 8800000.00, 'Active')
]

cursor.executemany('INSERT INTO policies VALUES (?,?,?,?,?,?,?,?,?,?,?)', policies_data)
print(f"✓ Inserted {len(policies_data)} policies")

# Insert Claims
claims_data = [
    (1, 2, 2, 'CLM-2023-001', '2023-07-15', 125000.00, 112000.00, 'Property Damage', 'Approved', '2023-08-01'),
    (2, 3, 3, 'CLM-2023-002', '2023-08-20', 85000.00, 85000.00, 'Liability', 'Approved', '2023-09-05'),
    (3, 4, 4, 'CLM-2023-003', '2023-09-10', 245000.00, 198000.00, 'Workers Comp', 'Approved', '2023-10-15'),
    (4, 7, 7, 'CLM-2023-004', '2023-10-25', 95000.00, 95000.00, 'General Liability', 'Approved', '2023-11-10'),
    (5, 9, 9, 'CLM-2023-005', '2023-11-15', 385000.00, 325000.00, 'Property Damage', 'Approved', '2023-12-01'),
    (6, 13, 13, 'CLM-2024-006', '2024-01-20', 178000.00, 156000.00, 'Liability', 'Approved', '2024-02-10'),
    (7, 14, 14, 'CLM-2024-007', '2024-02-14', 67000.00, 0.00, 'Property Damage', 'Rejected', None),
    (8, 16, 16, 'CLM-2024-008', '2024-03-05', 128000.00, None, 'Workers Comp', 'Pending', None),
    (9, 19, 19, 'CLM-2024-009', '2024-03-18', 425000.00, 380000.00, 'General Liability', 'Approved', '2024-04-02'),
    (10, 21, 1, 'CLM-2024-010', '2024-04-10', 72000.00, None, 'Property Damage', 'Pending', None),
    (11, 22, 3, 'CLM-2024-011', '2024-04-25', 195000.00, 175000.00, 'Liability', 'Approved', '2024-05-15'),
    (12, 23, 7, 'CLM-2024-012', '2024-05-08', 88000.00, 88000.00, 'Workers Comp', 'Approved', '2024-05-22')
]

cursor.executemany('INSERT INTO claims VALUES (?,?,?,?,?,?,?,?,?,?)', claims_data)
print(f"✓ Inserted {len(claims_data)} claims")

# Insert Payments
payments_data = [
    (1, 1, 1, '2023-01-15', 45000.00, 'Wire Transfer', 'Completed'),
    (2, 2, 2, '2023-02-20', 78000.00, 'ACH', 'Completed'),
    (3, 3, 3, '2023-03-10', 125000.00, 'Wire Transfer', 'Completed'),
    (4, 4, 4, '2023-04-05', 56000.00, 'Check', 'Completed'),
    (5, 5, 5, '2023-05-12', 95000.00, 'Wire Transfer', 'Completed'),
    (6, 6, 6, '2023-06-18', 87000.00, 'ACH', 'Completed'),
    (7, 7, 7, '2023-07-22', 64000.00, 'Wire Transfer', 'Completed'),
    (8, 8, 8, '2023-08-30', 52000.00, 'ACH', 'Completed'),
    (9, 9, 9, '2023-09-15', 135000.00, 'Wire Transfer', 'Completed'),
    (10, 10, 10, '2023-10-20', 48000.00, 'Check', 'Completed'),
    (11, 1, 1, '2024-01-15', 45000.00, 'Wire Transfer', 'Completed'),
    (12, 2, 2, '2024-02-20', 78000.00, 'ACH', 'Failed'),
    (13, 3, 3, '2024-03-10', 125000.00, 'Wire Transfer', 'Pending'),
    (14, 13, 13, '2024-01-08', 142000.00, 'Wire Transfer', 'Completed'),
    (15, 14, 14, '2024-01-15', 59000.00, 'ACH', 'Completed'),
    (16, 15, 15, '2024-01-22', 88000.00, 'Wire Transfer', 'Completed'),
    (17, 16, 16, '2024-02-01', 68000.00, 'ACH', 'Completed'),
    (18, 17, 17, '2024-02-10', 54000.00, 'Wire Transfer', 'Completed'),
    (19, 18, 18, '2024-02-15', 79000.00, 'Wire Transfer', 'Completed'),
    (20, 19, 19, '2024-03-01', 155000.00, 'Wire Transfer', 'Completed'),
    (21, 20, 20, '2024-03-12', 97000.00, 'ACH', 'Completed'),
    (22, 21, 1, '2024-04-01', 47000.00, 'Wire Transfer', 'Completed'),
    (23, 22, 3, '2024-04-10', 138000.00, 'Wire Transfer', 'Pending')
]

cursor.executemany('INSERT INTO payments VALUES (?,?,?,?,?,?,?)', payments_data)
print(f"✓ Inserted {len(payments_data)} payments")

# Insert Ongoing Claims (NEW)
ongoing_claims_data = [
    (1, 16, 16, 'ONG-CLM-2024-001', '2024-03-05', 128000.00, 'Under Investigation', 'John Adjuster', '2024-05-15'),
    (2, 21, 1, 'ONG-CLM-2024-002', '2024-04-10', 72000.00, 'Awaiting Documentation', 'Sarah Claims', '2024-05-18'),
    (3, 24, 9, 'ONG-CLM-2024-003', '2024-05-01', 215000.00, 'In Review', 'Mike Inspector', '2024-05-20'),
    (4, 25, 2, 'ONG-CLM-2024-004', '2024-05-05', 94000.00, 'Awaiting Approval', 'Lisa Handler', '2024-05-21'),
    (5, 10, 10, 'ONG-CLM-2024-005', '2024-04-22', 156000.00, 'Under Investigation', 'Tom Adjuster', '2024-05-19'),
    (6, 15, 15, 'ONG-CLM-2024-006', '2024-05-10', 88000.00, 'Documentation Complete', 'Jane Claims', '2024-05-22'),
    (7, 17, 17, 'ONG-CLM-2024-007', '2024-05-12', 67000.00, 'In Review', 'Bob Inspector', '2024-05-23')
]

cursor.executemany('INSERT INTO ongoing_claims VALUES (?,?,?,?,?,?,?,?,?)', ongoing_claims_data)
print(f"✓ Inserted {len(ongoing_claims_data)} ongoing claims")

# Insert Quoted Policies (NEW)
quoted_policies_data = [
    (1, 4, 1, 'Middle Market', 'GC', 'QUO-2024-001', '2024-05-01', 51000.00, 6000000.00, 'Pending', '2024-06-01'),
    (2, 7, 2, 'National Program', 'LS', 'QUO-2024-002', '2024-05-03', 69000.00, 7800000.00, 'Pending', '2024-06-03'),
    (3, 12, 3, 'National Account', 'GC', 'QUO-2024-003', '2024-05-05', 148000.00, 19500000.00, 'Pending', '2024-06-05'),
    (4, 14, 4, 'Middle Market', 'LS', 'QUO-2024-004', '2024-05-07', 57000.00, 6800000.00, 'Accepted', '2024-06-07'),
    (5, 16, 5, 'Public Sector', 'GC', 'QUO-2024-005', '2024-05-08', 91000.00, 10500000.00, 'Pending', '2024-06-08'),
    (6, 1, 6, 'Middle Market', 'GC', 'QUO-2024-006', '2024-05-10', 46000.00, 5600000.00, 'Rejected', '2024-06-10'),
    (7, 8, 7, 'National Program', 'LS', 'QUO-2024-007', '2024-05-12', 73000.00, 8400000.00, 'Pending', '2024-06-12'),
    (8, 10, 8, 'National Account', 'GC', 'QUO-2024-008', '2024-05-13', 152000.00, 21000000.00, 'Accepted', '2024-06-13'),
    (9, 3, 1, 'Middle Market', 'LS', 'QUO-2024-009', '2024-05-15', 54000.00, 6400000.00, 'Pending', '2024-06-15'),
    (10, 5, 4, 'Public Sector', 'GC', 'QUO-2024-010', '2024-05-16', 93000.00, 11200000.00, 'Pending', '2024-06-16'),
    (11, 19, 3, 'National Account', 'LS', 'QUO-2024-011', '2024-05-18', 162000.00, 23000000.00, 'Accepted', '2024-06-18'),
    (12, 6, 4, 'Public Sector', 'GC', 'QUO-2024-012', '2024-05-20', 89000.00, 9800000.00, 'Pending', '2024-06-20')
]

cursor.executemany('INSERT INTO quoted_policies VALUES (?,?,?,?,?,?,?,?,?,?,?)', quoted_policies_data)
print(f"✓ Inserted {len(quoted_policies_data)} quoted policies")

# Insert Issued Policies (NEW)
issued_policies_data = [
    (1, 1, 1, '2023-01-15', 'Sarah Mitchell', 'Email', 'ISS-2023-001'),
    (2, 2, 2, '2023-02-20', 'Robert Chen', 'Portal', 'ISS-2023-002'),
    (3, 3, 3, '2023-03-10', 'Maria Garcia', 'Email', 'ISS-2023-003'),
    (4, 4, 4, '2023-04-05', 'Sarah Mitchell', 'Mail', 'ISS-2023-004'),
    (5, 5, 5, '2023-05-12', 'James Wilson', 'Email', 'ISS-2023-005'),
    (6, 6, 6, '2023-06-18', 'James Wilson', 'Portal', 'ISS-2023-006'),
    (7, 7, 7, '2023-07-22', 'Robert Chen', 'Email', 'ISS-2023-007'),
    (8, 8, 8, '2023-08-30', 'Maria Garcia', 'Email', 'ISS-2023-008'),
    (9, 9, 9, '2023-09-15', 'Jennifer Lee', 'Portal', 'ISS-2023-009'),
    (10, 10, 10, '2023-10-20', 'Jennifer Lee', 'Email', 'ISS-2023-010'),
    (11, 13, 13, '2024-01-08', 'Lisa Anderson', 'Email', 'ISS-2024-013'),
    (12, 14, 14, '2024-01-15', 'David Martinez', 'Portal', 'ISS-2024-014'),
    (13, 15, 15, '2024-01-22', 'James Wilson', 'Email', 'ISS-2024-015'),
    (14, 16, 16, '2024-02-01', 'Sarah Mitchell', 'Email', 'ISS-2024-016'),
    (15, 17, 17, '2024-02-10', 'Robert Chen', 'Portal', 'ISS-2024-017'),
    (16, 18, 18, '2024-02-15', 'James Wilson', 'Email', 'ISS-2024-018'),
    (17, 19, 19, '2024-03-01', 'Maria Garcia', 'Email', 'ISS-2024-019'),
    (18, 20, 20, '2024-03-12', 'James Wilson', 'Portal', 'ISS-2024-020'),
    (19, 21, 1, '2024-04-01', 'Michael Brown', 'Email', 'ISS-2024-021'),
    (20, 22, 3, '2024-04-10', 'Lisa Anderson', 'Email', 'ISS-2024-022')
]

cursor.executemany('INSERT INTO issued_policies VALUES (?,?,?,?,?,?,?)', issued_policies_data)
print(f"✓ Inserted {len(issued_policies_data)} issued policies")

## Commit changes
connection.commit()
print("\n[4/7] Committed all data to database")

## Generate and display statistics
print("\n[5/7] Generating database statistics...")
print("\n" + "="*70)
print("DATABASE SUMMARY")
print("="*70)

# Table counts
cursor.execute("SELECT COUNT(*) FROM account")
accounts_count = cursor.fetchone()[0]
print(f"📊 Total Accounts:           {accounts_count:>4}")

cursor.execute("SELECT COUNT(*) FROM agents")
agents_count = cursor.fetchone()[0]
print(f"👥 Total Agents:              {agents_count:>4}")

cursor.execute("SELECT COUNT(*) FROM policies")
policies_count = cursor.fetchone()[0]
print(f"📋 Total Policies:            {policies_count:>4}")

cursor.execute("SELECT COUNT(*) FROM claims")
claims_count = cursor.fetchone()[0]
print(f"📝 Total Claims:              {claims_count:>4}")

cursor.execute("SELECT COUNT(*) FROM payments")
payments_count = cursor.fetchone()[0]
print(f"💰 Total Payments:            {payments_count:>4}")

cursor.execute("SELECT COUNT(*) FROM ongoing_claims")
ongoing_count = cursor.fetchone()[0]
print(f"⏳ Ongoing Claims:            {ongoing_count:>4}")

cursor.execute("SELECT COUNT(*) FROM quoted_policies")
quoted_count = cursor.fetchone()[0]
print(f"📄 Quoted Policies:           {quoted_count:>4}")

cursor.execute("SELECT COUNT(*) FROM issued_policies")
issued_count = cursor.fetchone()[0]
print(f"✅ Issued Policies:           {issued_count:>4}")

print("\n" + "="*70)
print("MARKET DISTRIBUTION")
print("="*70)

# Market types distribution
print("\n📊 Policies by Market Type:")
cursor.execute("""
    SELECT market_type, COUNT(*) as count, SUM(premium_amount) as total_premium 
    FROM policies 
    WHERE status = 'Active'
    GROUP BY market_type 
    ORDER BY count DESC
""")
for row in cursor.fetchall():
    print(f"   {row[0]:<25} {row[1]:>2} policies  ${row[2]:>12,.2f}")

# Policy types distribution
print("\n📊 Policies by Policy Type:")
cursor.execute("""
    SELECT policy_type, COUNT(*) as count, SUM(premium_amount) as total_premium 
    FROM policies 
    WHERE status = 'Active'
    GROUP BY policy_type 
    ORDER BY count DESC
""")
for row in cursor.fetchall():
    type_name = 'Guaranteed Cost (GC)' if row[0] == 'GC' else 'Loss Sensitive (LS)'
    print(f"   {type_name:<25} {row[1]:>2} policies  ${row[2]:>12,.2f}")

print("\n" + "="*70)
print("CLAIMS & QUOTES STATUS")
print("="*70)

# Claims by status
print("\n📋 Claims Summary:")
cursor.execute("""
    SELECT status, COUNT(*) as count, SUM(claim_amount) as total_amount 
    FROM claims 
    GROUP BY status
""")
for row in cursor.fetchall():
    amount = row[2] if row[2] else 0
    print(f"   {row[0]:<12} {row[1]:>2} claims   ${amount:>12,.2f}")

# Ongoing claims status
print("\n⏳ Ongoing Claims Status:")
cursor.execute("""
    SELECT current_status, COUNT(*) as count, SUM(claim_amount) as total_amount 
    FROM ongoing_claims 
    GROUP BY current_status
    ORDER BY count DESC
""")
for row in cursor.fetchall():
    print(f"   {row[0]:<30} {row[1]:>2} claims   ${row[2]:>12,.2f}")

# Quoted policies status
print("\n📄 Quoted Policies Status:")
cursor.execute("""
    SELECT quote_status, COUNT(*) as count, SUM(quoted_premium) as total_premium 
    FROM quoted_policies 
    GROUP BY quote_status
    ORDER BY count DESC
""")
for row in cursor.fetchall():
    print(f"   {row[0]:<12} {row[1]:>2} quotes   ${row[2]:>12,.2f}")

print("\n" + "="*70)
print("TOP PERFORMERS")
print("="*70)

# Top agents
print("\n🏆 Top 5 Agents by Policy Count:")
cursor.execute("""
    SELECT a.name, COUNT(p.policy_id) as policy_count, SUM(p.premium_amount) as total_premium
    FROM agents a
    JOIN policies p ON a.agent_id = p.agent_id
    GROUP BY a.name
    ORDER BY policy_count DESC
    LIMIT 5
""")
for idx, row in enumerate(cursor.fetchall(), 1):
    print(f"   {idx}. {row[0]:<25} {row[1]:>2} policies  ${row[2]:>12,.2f}")

print("\n" + "="*70)
print("FINANCIAL OVERVIEW")
print("="*70)

cursor.execute("SELECT SUM(premium_amount) FROM policies WHERE status='Active'")
total_premium = cursor.fetchone()[0]
print(f"   Total Active Premium Revenue:    ${total_premium:>14,.2f}")

cursor.execute("SELECT SUM(approved_amount) FROM claims WHERE status='Approved'")
total_approved = cursor.fetchone()[0]
if total_approved:
    print(f"   Total Approved Claims:           ${total_approved:>14,.2f}")
    print(f"   Claims Ratio:                    {(total_approved/total_premium*100):>14.2f}%")

cursor.execute("SELECT SUM(amount) FROM payments WHERE status='Completed'")
total_payments = cursor.fetchone()[0]
print(f"   Total Payments Collected:        ${total_payments:>14,.2f}")

cursor.execute("SELECT SUM(claim_amount) FROM ongoing_claims")
ongoing_exposure = cursor.fetchone()[0]
print(f"   Ongoing Claims Exposure:         ${ongoing_exposure:>14,.2f}")

cursor.execute("SELECT SUM(quoted_premium) FROM quoted_policies WHERE quote_status='Pending'")
pending_quotes = cursor.fetchone()[0]
if pending_quotes:
    print(f"   Pending Quoted Premium:          ${pending_quotes:>14,.2f}")

connection.close()

print("\n" + "="*70)
print("✅ DATABASE CREATED SUCCESSFULLY!")
print("="*70)
print("\n📁 Database file: insurance.db")
print("🚀 Ready to use with the Streamlit application!")
print("\nNext steps:")
print("  1. Run: streamlit run app.py")
print("  2. Start querying your data!")
print("\n" + "="*70)