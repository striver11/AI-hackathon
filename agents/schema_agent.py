"""
Schema Agent - Generates and manages database schema information
"""

from agents.db_agent import DatabaseAgent
from typing import Dict, List

class SchemaAgent:
    def __init__(self):
        self.db_agent = DatabaseAgent()
    
    def generate_schema_context(self) -> str:
        """Generate comprehensive schema context for AI"""
        tables = self.db_agent.get_tables()
        schema_context = "DATABASE SCHEMA INFORMATION:\n\n"
        
        for table in tables:
            schema_df = self.db_agent.get_table_schema(table)
            row_count = self.db_agent.get_row_count(table)
            
            schema_context += f"Table: {table.upper()} ({row_count} rows)\n"
            schema_context += "Columns:\n"
            
            for _, row in schema_df.iterrows():
                if 'name' in schema_df.columns:
                    col_name = row['name']
                    col_type = row.get('type', 'unknown')
                    is_pk = row.get('pk', 0)
                    pk_indicator = " (PRIMARY KEY)" if is_pk else ""
                    schema_context += f"  - {col_name}: {col_type}{pk_indicator}\n"
            
            schema_context += "\n"
        
        return schema_context
    
    def get_table_relationships(self) -> str:
        """Identify and describe table relationships"""
        # For SQLite, we need to parse foreign keys manually
        # This is a simplified version
        relationships = """
TABLE RELATIONSHIPS:

customers ← policies (customer_id)
agents ← policies (agent_id)
policies ← claims (policy_id)
customers ← claims (customer_id)
policies ← payments (policy_id)
customers ← payments (customer_id)
"""
        return relationships
    
    def get_full_schema_prompt(self) -> str:
        """Get complete schema information for AI prompt"""
        schema = self.generate_schema_context()
        relationships = self.get_table_relationships()
        
        return f"{schema}\n{relationships}"