High-Level System Architecture
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE LAYER                        │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │ Dashboard  │  │   Query    │  │  Schema    │  │ Analytics  │   │
│  │   Page     │  │ Assistant  │  │  Explorer  │  │   Page     │   │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘   │
│                       (Streamlit Web App)                           │
└─────────────────────────────────────────────────────────────────────┘
                                  ↕
┌─────────────────────────────────────────────────────────────────────┐
│                      AGENT ORCHESTRATION LAYER                      │
│                                                                     │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │  SQL Generator   │  │   Schema Agent   │  │ Analytics Agent  │ │
│  │     Agent        │  │                  │  │                  │ │
│  │                  │  │  • Maps DB       │  │  • Calculates    │ │
│  │  • Converts      │  │    structure     │  │    KPIs          │ │
│  │    English to    │  │  • Identifies    │  │  • Generates     │ │
│  │    SQL           │  │    relationships │  │    reports       │ │
│  │  • Uses Gemini   │  │  • Provides      │  │  • Creates       │ │
│  │    AI            │  │    context       │  │    charts        │ │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘ │
│                                  ↓                                  │
│                      ┌──────────────────────┐                      │
│                      │   Database Agent     │                      │
│                      │                      │                      │
│                      │  • Connection mgmt   │                      │
│                      │  • Query execution   │                      │
│                      │  • Result handling   │                      │
│                      │  • DB abstraction    │                      │
│                      └──────────────────────┘                      │
└─────────────────────────────────────────────────────────────────────┘
                                  ↕
┌─────────────────────────────────────────────────────────────────────┐
│                           DATA LAYER                                │
│                                                                     │
│     ┌─────────────────┐              ┌─────────────────┐          │
│     │     SQLite      │      OR      │   Databricks    │          │
│     │  (Development)  │              │  (Production)   │          │
│     └─────────────────┘              └─────────────────┘          │
│                                                                     │
│     Switch via config.py - Zero code changes required!             │
└─────────────────────────────────────────────────────────────────────┘
                                  ↕
┌─────────────────────────────────────────────────────────────────────┐
│                       EXTERNAL AI SERVICE                           │
│                                                                     │
│                     ┌──────────────────────┐                       │
│                     │   Google Gemini AI   │                       │
│                     │    (2.5 Flash)       │                       │
│                     │                      │                       │
│                     │  Natural Language    │                       │
│                     │  Understanding       │                       │
│                     └──────────────────────┘                       │
└─────────────────────────────────────────────────────────────────────┘


Natural Language Query Flow

┌──────────────────────────────────────────────────────────────────────┐
│ STEP 1: USER INPUT                                                   │
└──────────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │  User types question:     │
                    │  "Show accounts from       │
                    │   California with claims  │
                    │   over $5000"             │
                    └─────────────┬─────────────┘
                                  │
┌──────────────────────────────────────────────────────────────────────┐
│ STEP 2: SCHEMA CONTEXT PREPARATION                                   │
└──────────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │   Schema Agent            │
                    │                           │
                    │   Provides:               │
                    │   • account(state)        │
                    │   • claims(claim_amount)  │
                    │   • Relationship via      │
                    │     account_id            │
                    └─────────────┬─────────────┘
                                  │
┌──────────────────────────────────────────────────────────────────────┐
│ STEP 3: AI PROCESSING                                                │
└──────────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │  SQL Generator Agent      │
                    │                           │
                    │  Sends to Gemini:         │
                    │  ┌─────────────────────┐  │
                    │  │ • User question     │  │
                    │  │ • Database schema   │  │
                    │  │ • Example queries   │  │
                    │  │ • Generation rules  │  │
                    │  └─────────────────────┘  │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │   Gemini AI Returns:      │
                    │                           │
                    │   SELECT c.name,          │
                    │          cl.claim_amount  │
                    │   FROM account c          │
                    │   JOIN claims cl          │
                    │   ON c.account_id =       │
                    │      cl.account_id        │
                    │   WHERE c.state = 'CA'    │
                    │   AND cl.claim_amount     │
                    │       > 5000              │
                    └─────────────┬─────────────┘
                                  │
┌──────────────────────────────────────────────────────────────────────┐
│ STEP 4: QUERY EXECUTION                                              │
└──────────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │   Database Agent          │
                    │                           │
                    │   1. Connect to DB        │
                    │   2. Execute SQL          │
                    │   3. Fetch results        │
                    │   4. Return data +        │
                    │      column names         │
                    └─────────────┬─────────────┘
                                  │
                                  │
                    ┌─────────────▼─────────────┐
                    │   Results:                │
                    │   [                       │
                    │     ('Sarah Johnson',     │
                    │      8000.00),            │
                    │     ('Mike Chen',         │
                    │      6500.00)             │
                    │   ]                       │
                    └─────────────┬─────────────┘
                                  │
┌──────────────────────────────────────────────────────────────────────┐
│ STEP 5: DISPLAY RESULTS                                              │
└──────────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │   Streamlit UI Shows:     │
                    │                           │
                    │   ✅ Generated SQL        │
                    │   ✅ Results table        │
                    │   ✅ Download CSV         │
                    │   ✅ Row count            │
                    │                           │
                    │   Time: 3-5 seconds       │
                    └───────────────────────────┘


Multi-Agent Interaction Flow

                    ┌─────────────────────────┐
                    │      Main App           │
                    │   (Streamlit - app.py)  │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼────────────┐
                    │   Initialize Agents    │
                    └───────────┬────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
    ┌───────────▼──────┐ ┌─────▼─────┐ ┌──────▼────────┐
    │  Database Agent  │ │  Schema   │ │ SQL Generator │
    │                  │ │  Agent    │ │    Agent      │
    │ ┌──────────────┐ │ │           │ │               │
    │ │ • connect()  │ │ │ Uses DB   │ │  Uses Schema  │
    │ │ • execute()  │◄┼─┤  Agent    │◄┼─┤    Agent    │
    │ │ • get_tables │ │ │           │ │               │
    │ └──────────────┘ │ │ Generates │ │  Calls Gemini │
    └──────────────────┘ │ context   │ │      AI       │
                         └───────────┘ └───────────────┘
                                │
                    ┌───────────▼────────────┐
                    │  Analytics Agent       │
                    │                        │
                    │  Uses Database Agent   │
                    │  Generates KPIs        │
                    └────────────────────────┘


USER REQUEST FLOW:

User Question
      │
      ▼
┌─────────────┐
│ Which agent │
│ to call?    │
└─────┬───────┘
      │
      ├──► "Show schema" ────────────► Database Agent
      │                                      │
      │                                      ▼
      │                                 Direct Query
      │                                      │
      │                                      ▼
      │                                  Return Data
      │
      ├──► "Natural language" ──► Schema Agent
      │                                │
      │                                ▼
      │                          Get Context
      │                                │
      │                                ▼
      │                         SQL Generator Agent
      │                                │
      │                                ▼
      │                            Gemini AI
      │                                │
      │                                ▼
      │                         Database Agent
      │                                │
      │                                ▼
      │                           Execute SQL
      │
      └──► "Dashboard" ────────────► Analytics Agent
                                          │
                                          ▼
                                    Calculate KPIs
                                          │
                                          ▼
                                    Database Agent
                                          │
                                          ▼
                                     Return Metrics

                

 AI vs Non-AI Operations
┌──────────────────────────────────────────────────────────────┐
│                    OPERATION TYPES                           │
└──────────────────────────────────────────────────────────────┘

┌─────────────────────────────────┐  ┌─────────────────────────┐
│      AI-POWERED (Gemini)        │  │    NON-AI (Direct DB)   │
├─────────────────────────────────┤  ├─────────────────────────┤
│                                 │  │                         │
│  Natural Language Queries       │  │  Dashboard Metrics      │
│         │                       │  │         │               │
│         ▼                       │  │         ▼               │
│  User: "Show accounts           │  │  SELECT COUNT(*)        │
│         from Texas"             │  │  FROM account           │
│         │                       │  │         │               │
│         ▼                       │  │         ▼               │
│  Schema Context ───────┐        │  │  Direct Execution       │
│         │              │        │  │         │               │
│         ▼              │        │  │         ▼               │
│  Gemini AI ◄───────────┘        │  │  Return: 15             │
│         │                       │  │                         │
│         ▼                       │  │  Schema Explorer        │
│  SQL: SELECT * FROM             │  │         │               │
│       account                   │  │         ▼               │
│       WHERE state='TX'          │  │  PRAGMA table_info()    │
│         │                       │  │         │               │
│         ▼                       │  │         ▼               │
│  Database Agent                 │  │  Return structure       │
│         │                       │  │                         │
│         ▼                       │  │  Analytics Charts       │
│  Results                        │  │         │               │
│                                 │  │         ▼               │
│  Time: 3-5 seconds              │  │  Pre-written queries    │
│  Cost: ~$0.001 per query        │  │         │               │
│                                 │  │         ▼               │
│                                 │  │  Results                │
│                                 │  │                         │
│                                 │  │  Time: <1 second        │
│                                 │  │  Cost: $0               │
└─────────────────────────────────┘  └─────────────────────────┘

                WHEN TO USE EACH:

AI-Powered:                         Non-AI:
- Complex questions                 • Schema information
- Varying query patterns            • Pre-defined metrics
- User exploration                  • Standard reports
- Flexibility needed                • Speed critical