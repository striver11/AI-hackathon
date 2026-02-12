"""
SQL Generator Agent - Converts natural language to SQL using Gemini AI
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

EXAMPLE QUERIES:

Question: "How many customers are there?"
SQL: SELECT COUNT(*) as total_customers FROM customers

Question: "Show all active policies with customer names"
SQL: SELECT c.name, p.policy_type, p.premium_amount, p.coverage_amount FROM customers c JOIN policies p ON c.customer_id = p.customer_id WHERE p.status = 'Active'

Question: "Which agent has sold the most policies?"
SQL: SELECT a.name, COUNT(p.policy_id) as total_policies FROM agents a JOIN policies p ON a.agent_id = p.agent_id GROUP BY a.name ORDER BY total_policies DESC LIMIT 1

Question: "Show customers with total claim amounts"
SQL: SELECT c.name, SUM(cl.claim_amount) as total_claims FROM customers c JOIN claims cl ON c.customer_id = cl.customer_id GROUP BY c.name

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
        
        return sql_query