"""
SQL Generator Agent - Converts natural language to SQL using Gemini AI
Updated with new schema information
"""

from google import genai
from config import GEMINI_CONFIG
from agents.schema_agent import SchemaAgent

class SQLGeneratorAgent:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_CONFIG["api_key"])
        self.schema_agent = SchemaAgent()
        self.schema_context = self.schema_agent.get_full_schema_prompt()
    
    def generate_sql(self, question: str) -> str:
        """Convert natural language question to SQL query"""
        
        prompt = f"""
You are an expert SQL query generator for an Insurance Company Database.

{self.schema_context}

IMPORTANT RULES:
1. Return ONLY the SQL query without any markdown, backticks, or explanations
2. Do NOT include "```sql" or "```" or the word "sql" in your response
3. Use proper JOINs when data from multiple tables is needed
4. Use aggregate functions (COUNT, SUM, AVG, MAX, MIN) appropriately
5. Always use table aliases for clarity
6. For date comparisons, use proper date functions
7. Use LIMIT clause for queries that might return many rows

MARKET TYPES: Middle Market, National Program, National Account, Public Sector
POLICY TYPES: GC (Guaranteed Cost), LS (Loss Sensitive)

EXAMPLE QUERIES:

Question: "How many accounts are there?"
SQL: SELECT COUNT(*) as total_accounts FROM account

Question: "Show all active policies for Middle Market"
SQL: SELECT c.name, p.market_type, p.policy_type, p.premium_amount FROM account c JOIN policies p ON c.account_id = p.account_id WHERE p.status = 'Active' AND p.market_type = 'Middle Market'

Question: "Which market type generates the most premium?"
SQL: SELECT market_type, SUM(premium_amount) as total_premium FROM policies WHERE status='Active' GROUP BY market_type ORDER BY total_premium DESC LIMIT 1

Question: "Show ongoing claims with account names"
SQL: SELECT c.name, oc.claim_number, oc.claim_amount, oc.current_status FROM account c JOIN ongoing_claims oc ON c.account_id = oc.account_id

Question: "What's the quote conversion rate by market type?"
SQL: SELECT market_type, COUNT(*) as total_quotes, SUM(CASE WHEN quote_status='Accepted' THEN 1 ELSE 0 END) as accepted, ROUND(SUM(CASE WHEN quote_status='Accepted' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as conversion_rate FROM quoted_policies GROUP BY market_type

Now convert this question to SQL:
Question: "{question}"
SQL:"""

        response = self.client.models.generate_content(
            model=GEMINI_CONFIG["model"],
            contents=prompt
        )
        
        sql_query = response.text.strip()
        
        # Clean up any remaining markdown or sql keywords
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        if sql_query.lower().startswith("sql"):
            sql_query = sql_query[3:].strip()
        if sql_query.startswith(":"):
            sql_query = sql_query[1:].strip()
        
        return sql_query
    
    def generate_analytics_sql(self, analytical_request: str) -> str:
        """
        Generate SQL specifically for analytics/charting purposes
        Returns SQL that produces data ready for visualization
        """
        
        prompt = f"""
You are generating SQL for data visualization and analytics.

{self.schema_context}

Generate SQL that returns data suitable for charts and dashboards.

Rules:
- Include descriptive column names
- Use GROUP BY for aggregations
- Include totals, averages, counts as needed
- Order results logically
- Return ONLY the SQL query

Analytical Request: "{analytical_request}"

SQL:"""

        response = self.client.models.generate_content(
            model=GEMINI_CONFIG["model"],
            contents=prompt
        )
        
        sql_query = response.text.strip()
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        if sql_query.lower().startswith("sql"):
            sql_query = sql_query[3:].strip()
        if sql_query.startswith(":"):
            sql_query = sql_query[1:].strip()
        
        return sql_query