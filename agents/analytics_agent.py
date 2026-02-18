"""
Analytics Agent - Generates insights and statistics from data
"""

import pandas as pd
from typing import Dict, Any
from agents.db_agent import DatabaseAgent

class AnalyticsAgent:
    def __init__(self):
        self.db_agent = DatabaseAgent()
    
    def get_quick_stats(self) -> Dict[str, Any]:
        """Generate quick statistics for dashboard"""
        stats = {}
        
        try:
            # Total accounts
            result, _ = self.db_agent.execute_query("SELECT COUNT(*) FROM account")
            stats['total_accounts'] = result[0][0]
            
            # Total active policies
            result, _ = self.db_agent.execute_query("SELECT COUNT(*) FROM policies WHERE status='Active'")
            stats['active_policies'] = result[0][0]
            
            # Total claims
            result, _ = self.db_agent.execute_query("SELECT COUNT(*) FROM claims")
            stats['total_claims'] = result[0][0]
            
            # Total approved claim amount
            result, _ = self.db_agent.execute_query("SELECT SUM(approved_amount) FROM claims WHERE status='Approved'")
            stats['total_approved_claims'] = result[0][0] if result[0][0] else 0
            
            # Total premium revenue
            result, _ = self.db_agent.execute_query("SELECT SUM(premium_amount) FROM policies WHERE status='Active'")
            stats['total_premium'] = result[0][0] if result[0][0] else 0
            
            # Pending claims
            result, _ = self.db_agent.execute_query("SELECT COUNT(*) FROM claims WHERE status='Pending'")
            stats['pending_claims'] = result[0][0]
            
        except Exception as e:
            print(f"Error generating stats: {e}")
        
        return stats
    
    def get_policy_distribution(self) -> pd.DataFrame:
        """Get distribution of policies by type"""
        query = """
        SELECT policy_type, COUNT(*) as count, SUM(premium_amount) as total_premium
        FROM policies
        WHERE status = 'Active'
        GROUP BY policy_type
        ORDER BY count DESC
        """
        results, columns = self.db_agent.execute_query(query)
        return pd.DataFrame(results, columns=columns)
    
    def get_top_agents(self, limit: int = 5) -> pd.DataFrame:
        """Get top performing agents"""
        query = f"""
        SELECT a.name, COUNT(p.policy_id) as total_policies, 
               SUM(p.premium_amount) as total_premium
        FROM agents a
        JOIN policies p ON a.agent_id = p.agent_id
        GROUP BY a.name
        ORDER BY total_premium DESC
        LIMIT {limit}
        """
        results, columns = self.db_agent.execute_query(query)
        return pd.DataFrame(results, columns=columns)
    
    def get_claims_summary(self) -> pd.DataFrame:
        """Get claims summary by status"""
        query = """
        SELECT status, COUNT(*) as count, 
               SUM(claim_amount) as total_requested,
               SUM(approved_amount) as total_approved
        FROM claims
        GROUP BY status
        """
        results, columns = self.db_agent.execute_query(query)
        return pd.DataFrame(results, columns=columns)