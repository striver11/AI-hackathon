"""
Database Agent - Handles all database operations
"""

import sqlite3
import pandas as pd
from typing import List, Dict, Any, Tuple
from config import DB_CONFIG

class DatabaseAgent:
    def __init__(self):
        self.db_type = DB_CONFIG["type"]
        self.connection = None
        
    def connect(self):
        """Establish database connection based on config"""
        if self.db_type == "sqlite":
            self.connection = sqlite3.connect(DB_CONFIG["sqlite"]["database"])
        elif self.db_type == "databricks":
            from databricks import sql
            self.connection = sql.connect(
                server_hostname=DB_CONFIG["databricks"]["server_hostname"],
                http_path=DB_CONFIG["databricks"]["http_path"],
                access_token=DB_CONFIG["databricks"]["access_token"]
            )
        return self.connection
    
    def execute_query(self, query: str) -> Tuple[List[Tuple], List[str]]:
        """Execute SQL query and return results with column names"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            column_names = [description[0] for description in cursor.description] if cursor.description else []
            conn.close()
            return results, column_names
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
    
    def get_tables(self) -> List[str]:
        """Get list of all tables in the database"""
        if self.db_type == "sqlite":
            query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        elif self.db_type == "databricks":
            catalog = DB_CONFIG["databricks"]["catalog"]
            schema = DB_CONFIG["databricks"]["schema"]
            query = f"SHOW TABLES IN {catalog}.{schema}"
        
        results, _ = self.execute_query(query)
        return [row[0] for row in results]
    
    def get_table_schema(self, table_name: str) -> pd.DataFrame:
        """Get schema information for a specific table"""
        if self.db_type == "sqlite":
            query = f"PRAGMA table_info({table_name});"
            results, columns = self.execute_query(query)
            df = pd.DataFrame(results, columns=columns)
            return df[['name', 'type', 'notnull', 'pk']]
        elif self.db_type == "databricks":
            query = f"DESCRIBE TABLE {table_name}"
            results, columns = self.execute_query(query)
            return pd.DataFrame(results, columns=columns)
    
    def get_row_count(self, table_name: str) -> int:
        """Get total row count for a table"""
        query = f"SELECT COUNT(*) FROM {table_name}"
        results, _ = self.execute_query(query)
        return results[0][0]
    
    def get_sample_data(self, table_name: str, limit: int = 5) -> pd.DataFrame:
        """Get sample data from a table"""
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        results, columns = self.execute_query(query)
        return pd.DataFrame(results, columns=columns)
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get overall database statistics"""
        tables = self.get_tables()
        stats = {
            "total_tables": len(tables),
            "tables": []
        }
        
        for table in tables:
            table_stats = {
                "name": table,
                "row_count": self.get_row_count(table)
            }
            stats["tables"].append(table_stats)
        
        return stats