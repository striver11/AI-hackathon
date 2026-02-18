"""
Insurance Database Creation Script
Creates a comprehensive insurance database with 5 related tables and sample data
"""

import sqlite3
from datetime import datetime, timedelta
import random

print("="*70)
print("Creating Insurance Database...")
print("="*70)

## Connect to SQLite
connection = sqlite3.connect("insurance.db")
cursor = connection.cursor()

## Drop existing tables if they exist
print("\n[1/6] Dropping existing tables (if any)...")
cursor.execute('DROP TABLE IF EXISTS claims')
cursor.execute('DROP TABLE IF EXISTS payments')
cursor.execute('DROP TABLE IF EXISTS policies')
cursor.execute('DROP TABLE IF EXISTS account')
cursor.execute('DROP TABLE IF EXISTS agents')
print("✓ Existing tables dropped")

## Create Tables
print("\n[2/6] Creating database schema...")

# 1. ACCOUNTS table
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

# 3. POLICIES table
cursor.execute('''
CREATE TABLE policies (
    policy_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    agent_id INTEGER,
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

## Insert Sample Data
print("\n[3/6] Inserting sample data...")

# Insert Accounts
accounts_data = [
    (1, 'John Smith', 'john.smith@email.com', '555-0101', '123 Main St', 'New York', 'NY', '10001', '1985-03-15', 'Male'),
    (2, 'Sarah Johnson', 'sarah.j@email.com', '555-0102', '456 Oak Ave', 'Los Angeles', 'CA', '90001', '1990-07-22', 'Female'),
    (3, 'Michael Brown', 'michael.b@email.com', '555-0103', '789 Pine Rd', 'Chicago', 'IL', '60601', '1978-11-30', 'Male'),
    (4, 'Emily Davis', 'emily.d@email.com', '555-0104', '321 Elm St', 'Houston', 'TX', '77001', '1988-05-18', 'Female'),
    (5, 'David Wilson', 'david.w@email.com', '555-0105', '654 Maple Dr', 'Phoenix', 'AZ', '85001', '1975-09-25', 'Male'),
    (6, 'Lisa Anderson', 'lisa.a@email.com', '555-0106', '987 Cedar Ln', 'Philadelphia', 'PA', '19101', '1992-12-08', 'Female'),
    (7, 'James Taylor', 'james.t@email.com', '555-0107', '147 Birch Way', 'San Antonio', 'TX', '78201', '1983-04-14', 'Male'),
    (8, 'Jennifer Martinez', 'jennifer.m@email.com', '555-0108', '258 Spruce Ct', 'San Diego', 'CA', '92101', '1995-08-03', 'Female'),
    (9, 'Robert Garcia', 'robert.g@email.com', '555-0109', '369 Willow St', 'Dallas', 'TX', '75201', '1980-01-20', 'Male'),
    (10, 'Maria Rodriguez', 'maria.r@email.com', '555-0110', '741 Ash Blvd', 'San Jose', 'CA', '95101', '1987-06-11', 'Female'),
    (11, 'Christopher Lee', 'chris.lee@email.com', '555-0111', '852 Oak Park', 'Austin', 'TX', '78701', '1991-02-28', 'Male'),
    (12, 'Amanda White', 'amanda.w@email.com', '555-0112', '963 Pine Valley', 'Jacksonville', 'FL', '32099', '1986-09-17', 'Female'),
    (13, 'Daniel Harris', 'daniel.h@email.com', '555-0113', '159 Maple Grove', 'San Francisco', 'CA', '94102', '1979-12-05', 'Male'),
    (14, 'Jessica Clark', 'jessica.c@email.com', '555-0114', '357 Cedar Ridge', 'Columbus', 'OH', '43085', '1993-04-23', 'Female'),
    (15, 'Matthew Lewis', 'matthew.l@email.com', '555-0115', '753 Birch Lane', 'Indianapolis', 'IN', '46201', '1984-08-30', 'Male')
]

cursor.executemany('INSERT INTO account VALUES (?,?,?,?,?,?,?,?,?,?)', accounts_data)
print(f"✓ Inserted {len(accounts_data)} accounts")

# Insert Agents
agents_data = [
    (1, 'Alice Cooper', 'alice.cooper@insurance.com', '555-1001', 'New York', 5.5, '2018-01-15', 'Active'),
    (2, 'Bob Miller', 'bob.miller@insurance.com', '555-1002', 'Los Angeles', 6.0, '2019-03-20', 'Active'),
    (3, 'Carol White', 'carol.white@insurance.com', '555-1003', 'Chicago', 5.0, '2020-06-10', 'Active'),
    (4, 'Daniel Lee', 'daniel.lee@insurance.com', '555-1004', 'Houston', 5.5, '2017-11-05', 'Active'),
    (5, 'Eva Martinez', 'eva.martinez@insurance.com', '555-1005', 'Phoenix', 6.5, '2021-02-18', 'Active'),
    (6, 'Frank Thompson', 'frank.t@insurance.com', '555-1006', 'Philadelphia', 5.0, '2019-08-12', 'Active'),
    (7, 'Grace Kim', 'grace.kim@insurance.com', '555-1007', 'San Diego', 6.0, '2020-01-25', 'Active')
]

cursor.executemany('INSERT INTO agents VALUES (?,?,?,?,?,?,?,?)', agents_data)
print(f"✓ Inserted {len(agents_data)} agents")

# Insert Policies
policies_data = [
    (1, 1, 1, 'Life Insurance', 'POL-2023-001', '2023-01-15', '2033-01-15', 1200.00, 500000.00, 'Active'),
    (2, 2, 2, 'Auto Insurance', 'POL-2023-002', '2023-02-20', '2024-02-20', 800.00, 50000.00, 'Active'),
    (3, 3, 3, 'Health Insurance', 'POL-2023-003', '2023-03-10', '2024-03-10', 450.00, 100000.00, 'Active'),
    (4, 4, 4, 'Home Insurance', 'POL-2023-004', '2023-04-05', '2024-04-05', 1500.00, 300000.00, 'Active'),
    (5, 5, 5, 'Life Insurance', 'POL-2023-005', '2023-05-12', '2033-05-12', 1000.00, 400000.00, 'Active'),
    (6, 6, 1, 'Auto Insurance', 'POL-2023-006', '2023-06-18', '2024-06-18', 900.00, 60000.00, 'Active'),
    (7, 7, 2, 'Health Insurance', 'POL-2023-007', '2023-07-22', '2024-07-22', 500.00, 120000.00, 'Active'),
    (8, 8, 3, 'Home Insurance', 'POL-2023-008', '2023-08-30', '2024-08-30', 1600.00, 350000.00, 'Active'),
    (9, 9, 4, 'Life Insurance', 'POL-2023-009', '2023-09-15', '2033-09-15', 1100.00, 450000.00, 'Active'),
    (10, 10, 5, 'Auto Insurance', 'POL-2023-010', '2023-10-20', '2024-10-20', 850.00, 55000.00, 'Active'),
    (11, 1, 2, 'Health Insurance', 'POL-2023-011', '2023-11-05', '2024-11-05', 400.00, 90000.00, 'Active'),
    (12, 3, 1, 'Auto Insurance', 'POL-2023-012', '2023-12-10', '2024-12-10', 750.00, 45000.00, 'Expired'),
    (13, 11, 6, 'Life Insurance', 'POL-2024-013', '2024-01-08', '2034-01-08', 1150.00, 425000.00, 'Active'),
    (14, 12, 7, 'Auto Insurance', 'POL-2024-014', '2024-01-15', '2025-01-15', 825.00, 52000.00, 'Active'),
    (15, 13, 1, 'Home Insurance', 'POL-2024-015', '2024-01-22', '2025-01-22', 1550.00, 325000.00, 'Active'),
    (16, 14, 2, 'Health Insurance', 'POL-2024-016', '2024-02-01', '2025-02-01', 475.00, 110000.00, 'Active'),
    (17, 15, 3, 'Life Insurance', 'POL-2024-017', '2024-02-10', '2034-02-10', 1075.00, 475000.00, 'Active'),
    (18, 2, 4, 'Home Insurance', 'POL-2024-018', '2024-02-15', '2025-02-15', 1450.00, 280000.00, 'Active'),
    (19, 5, 5, 'Auto Insurance', 'POL-2024-019', '2024-03-01', '2025-03-01', 875.00, 58000.00, 'Active'),
    (20, 8, 6, 'Health Insurance', 'POL-2024-020', '2024-03-12', '2025-03-12', 525.00, 125000.00, 'Active')
]

cursor.executemany('INSERT INTO policies VALUES (?,?,?,?,?,?,?,?,?,?)', policies_data)
print(f"✓ Inserted {len(policies_data)} policies")

# Insert Claims
claims_data = [
    (1, 2, 2, 'CLM-2023-001', '2023-07-15', 5000.00, 4500.00, 'Auto Accident', 'Approved', '2023-08-01'),
    (2, 3, 3, 'CLM-2023-002', '2023-08-20', 2500.00, 2500.00, 'Medical', 'Approved', '2023-09-05'),
    (3, 4, 4, 'CLM-2023-003', '2023-09-10', 15000.00, 12000.00, 'Fire Damage', 'Approved', '2023-10-15'),
    (4, 6, 6, 'CLM-2023-004', '2023-10-25', 3000.00, 3000.00, 'Auto Theft', 'Approved', '2023-11-10'),
    (5, 7, 7, 'CLM-2023-005', '2023-11-15', 1800.00, 1800.00, 'Medical', 'Approved', '2023-12-01'),
    (6, 8, 8, 'CLM-2024-006', '2024-01-20', 8000.00, 6500.00, 'Water Damage', 'Approved', '2024-02-10'),
    (7, 10, 10, 'CLM-2024-007', '2024-02-14', 4200.00, 0.00, 'Auto Accident', 'Rejected', None),
    (8, 11, 1, 'CLM-2024-008', '2024-03-05', 3500.00, None, 'Medical', 'Pending', None),
    (9, 14, 12, 'CLM-2024-009', '2024-03-18', 2800.00, 2800.00, 'Auto Collision', 'Approved', '2024-04-02'),
    (10, 16, 14, 'CLM-2024-010', '2024-04-10', 1500.00, None, 'Medical', 'Pending', None),
    (11, 18, 2, 'CLM-2024-011', '2024-04-25', 9500.00, 8000.00, 'Storm Damage', 'Approved', '2024-05-15'),
    (12, 20, 8, 'CLM-2024-012', '2024-05-08', 2200.00, 2200.00, 'Medical', 'Approved', '2024-05-22')
]

cursor.executemany('INSERT INTO claims VALUES (?,?,?,?,?,?,?,?,?,?)', claims_data)
print(f"✓ Inserted {len(claims_data)} claims")

# Insert Payments
payments_data = [
    (1, 1, 1, '2023-01-15', 1200.00, 'Credit Card', 'Completed'),
    (2, 2, 2, '2023-02-20', 800.00, 'Bank Transfer', 'Completed'),
    (3, 3, 3, '2023-03-10', 450.00, 'Debit Card', 'Completed'),
    (4, 4, 4, '2023-04-05', 1500.00, 'Check', 'Completed'),
    (5, 5, 5, '2023-05-12', 1000.00, 'Credit Card', 'Completed'),
    (6, 6, 6, '2023-06-18', 900.00, 'Bank Transfer', 'Completed'),
    (7, 7, 7, '2023-07-22', 500.00, 'Credit Card', 'Completed'),
    (8, 8, 8, '2023-08-30', 1600.00, 'Debit Card', 'Completed'),
    (9, 9, 9, '2023-09-15', 1100.00, 'Bank Transfer', 'Completed'),
    (10, 10, 10, '2023-10-20', 850.00, 'Credit Card', 'Completed'),
    (11, 1, 1, '2024-01-15', 1200.00, 'Credit Card', 'Completed'),
    (12, 2, 2, '2024-02-20', 800.00, 'Bank Transfer', 'Failed'),
    (13, 3, 3, '2024-03-10', 450.00, 'Debit Card', 'Pending'),
    (14, 13, 11, '2024-01-08', 1150.00, 'Credit Card', 'Completed'),
    (15, 14, 12, '2024-01-15', 825.00, 'Bank Transfer', 'Completed'),
    (16, 15, 13, '2024-01-22', 1550.00, 'Credit Card', 'Completed'),
    (17, 16, 14, '2024-02-01', 475.00, 'Debit Card', 'Completed'),
    (18, 17, 15, '2024-02-10', 1075.00, 'Bank Transfer', 'Completed'),
    (19, 18, 2, '2024-02-15', 1450.00, 'Credit Card', 'Completed'),
    (20, 19, 5, '2024-03-01', 875.00, 'Check', 'Completed'),
    (21, 20, 8, '2024-03-12', 525.00, 'Credit Card', 'Completed'),
    (22, 11, 1, '2024-04-05', 400.00, 'Credit Card', 'Failed'),
    (23, 13, 11, '2024-05-08', 1150.00, 'Bank Transfer', 'Pending')
]

cursor.executemany('INSERT INTO payments VALUES (?,?,?,?,?,?,?)', payments_data)
print(f"✓ Inserted {len(payments_data)} payments")

## Commit changes
connection.commit()
print("\n[4/6] Committed all data to database")

## Generate and display statistics
print("\n[5/6] Generating database statistics...")
print("\n" + "="*70)
print("DATABASE SUMMARY")
print("="*70)

# Table counts
cursor.execute("SELECT COUNT(*) FROM account")
accounts_count = cursor.fetchone()[0]
print(f"📊 Total Accounts:       {accounts_count:>4}")

cursor.execute("SELECT COUNT(*) FROM agents")
agents_count = cursor.fetchone()[0]
print(f"👥 Total Agents:          {agents_count:>4}")

cursor.execute("SELECT COUNT(*) FROM policies")
policies_count = cursor.fetchone()[0]
print(f"📋 Total Policies:        {policies_count:>4}")

cursor.execute("SELECT COUNT(*) FROM claims")
claims_count = cursor.fetchone()[0]
print(f"📝 Total Claims:          {claims_count:>4}")

cursor.execute("SELECT COUNT(*) FROM payments")
payments_count = cursor.fetchone()[0]
print(f"💰 Total Payments:        {payments_count:>4}")

print("\n" + "="*70)
print("SAMPLE DATA PREVIEW")
print("="*70)

# Accounts by state
print("\n📍 Accounts by State:")
cursor.execute("""
    SELECT state, COUNT(*) as count 
    FROM account 
    GROUP BY state 
    ORDER BY count DESC 
    LIMIT 5
""")
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[1]} accounts")

# Policy types distribution
print("\n📊 Policy Distribution:")
cursor.execute("""
    SELECT policy_type, COUNT(*) as count, SUM(premium_amount) as total_premium 
    FROM policies 
    WHERE status = 'Active'
    GROUP BY policy_type 
    ORDER BY count DESC
""")
for row in cursor.fetchall():
    print(f"   {row[0]:<20} {row[1]:>2} policies  ${row[2]:>8,.2f}")

# Claims by status
print("\n📋 Claims Summary:")
cursor.execute("""
    SELECT status, COUNT(*) as count, SUM(claim_amount) as total_amount 
    FROM claims 
    GROUP BY status
""")
for row in cursor.fetchall():
    amount = row[2] if row[2] else 0
    print(f"   {row[0]:<12} {row[1]:>2} claims   ${amount:>9,.2f}")

# Top agents
print("\n🏆 Top 3 Agents by Policy Count:")
cursor.execute("""
    SELECT a.name, COUNT(p.policy_id) as policy_count, SUM(p.premium_amount) as total_premium
    FROM agents a
    JOIN policies p ON a.agent_id = p.agent_id
    GROUP BY a.name
    ORDER BY policy_count DESC
    LIMIT 3
""")
for idx, row in enumerate(cursor.fetchall(), 1):
    print(f"   {idx}. {row[0]:<20} {row[1]:>2} policies  ${row[2]:>8,.2f}")

# Financial summary
print("\n💵 Financial Overview:")
cursor.execute("SELECT SUM(premium_amount) FROM policies WHERE status='Active'")
total_premium = cursor.fetchone()[0]
print(f"   Total Active Premium Revenue:  ${total_premium:>10,.2f}")

cursor.execute("SELECT SUM(approved_amount) FROM claims WHERE status='Approved'")
result = cursor.fetchone()
total_approved = result[0] if result and result[0] is not None else 0
if total_approved:
    print(f"   Total Approved Claims:         ${total_approved:>10,.2f}")
    print(f"   Claims Ratio:                  {(total_approved/total_premium*100):>10.2f}%")

cursor.execute("SELECT SUM(amount) FROM payments WHERE status='Completed'")
total_payments = cursor.fetchone()[0]
print(f"   Total Payments Collected:      ${total_payments:>10,.2f}")

print("\n" + "="*70)
print("[6/6] Verification Queries")
print("="*70)

# Sample complex query
print("\n🔍 Sample Query - Accounts with Active Policies and Claims:")
cursor.execute("""
    SELECT 
        c.name, 
        p.policy_type, 
        p.premium_amount,
        COUNT(cl.claim_id) as claim_count
    FROM account c
    JOIN policies p ON c.account_id = p.account_id
    LEFT JOIN claims cl ON p.policy_id = cl.policy_id
    WHERE p.status = 'Active'
    GROUP BY c.name, p.policy_type, p.premium_amount
    HAVING claim_count > 0
    LIMIT 5
""")
results = cursor.fetchall()
if results:
    print(f"\n{'Account Name':<20} {'Policy Type':<20} {'Premium':<12} {'Claims'}")
    print("-" * 70)
    for row in results:
        print(f"{row[0]:<20} {row[1]:<20} ${row[2]:<11,.2f} {row[3]}")

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