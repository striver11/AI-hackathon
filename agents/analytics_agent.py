"""
Analytics Agent - Generates insights and statistics from data
Updated with dynamic chart generation capabilities
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
            # Total customers
            result, _ = self.db_agent.execute_query("SELECT COUNT(*) FROM customers")
            stats['total_customers'] = result[0][0]
            
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
            
            # NEW: Ongoing claims
            result, _ = self.db_agent.execute_query("SELECT COUNT(*) FROM ongoing_claims")
            stats['ongoing_claims'] = result[0][0]
            
            # NEW: Total quoted policies
            result, _ = self.db_agent.execute_query("SELECT COUNT(*) FROM quoted_policies")
            stats['total_quoted_policies'] = result[0][0]
            
            # NEW: Total issued policies
            result, _ = self.db_agent.execute_query("SELECT COUNT(*) FROM issued_policies")
            stats['total_issued_policies'] = result[0][0]
            
        except Exception as e:
            print(f"Error generating stats: {e}")
        
        return stats
    
    def get_market_distribution(self) -> pd.DataFrame:
        """Get distribution of policies by market type"""
        query = """
        SELECT market_type, COUNT(*) as count, SUM(premium_amount) as total_premium
        FROM policies
        WHERE status = 'Active'
        GROUP BY market_type
        ORDER BY count DESC
        """
        results, columns = self.db_agent.execute_query(query)
        return pd.DataFrame(results, columns=columns)
    
    def get_policy_type_distribution(self) -> pd.DataFrame:
        """Get distribution by policy type (GC/LS)"""
        query = """
        SELECT 
            CASE 
                WHEN policy_type = 'GC' THEN 'Guaranteed Cost'
                WHEN policy_type = 'LS' THEN 'Loss Sensitive'
                ELSE policy_type
            END as policy_type_name,
            COUNT(*) as count, 
            SUM(premium_amount) as total_premium
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
    
    def get_ongoing_claims_summary(self) -> pd.DataFrame:
        """Get ongoing claims summary"""
        query = """
        SELECT current_status, COUNT(*) as count, 
               SUM(claim_amount) as total_amount
        FROM ongoing_claims
        GROUP BY current_status
        ORDER BY count DESC
        """
        results, columns = self.db_agent.execute_query(query)
        return pd.DataFrame(results, columns=columns)
    
    def get_quote_conversion_metrics(self) -> Dict[str, Any]:
        """Get quote to policy conversion metrics"""
        metrics = {}
        
        try:
            # Total quotes
            result, _ = self.db_agent.execute_query("SELECT COUNT(*) FROM quoted_policies")
            total_quotes = result[0][0]
            
            # Accepted quotes
            result, _ = self.db_agent.execute_query(
                "SELECT COUNT(*) FROM quoted_policies WHERE quote_status='Accepted'"
            )
            accepted_quotes = result[0][0]
            
            # Conversion rate
            conversion_rate = (accepted_quotes / total_quotes * 100) if total_quotes > 0 else 0
            
            metrics['total_quotes'] = total_quotes
            metrics['accepted_quotes'] = accepted_quotes
            metrics['conversion_rate'] = round(conversion_rate, 2)
            
        except Exception as e:
            print(f"Error calculating conversion metrics: {e}")
        
        return metrics
    
    def generate_dynamic_analysis(self, query: str) -> pd.DataFrame:
        """
        Execute a custom analytical query
        This is used by the dynamic analytics generation
        """
        try:
            results, columns = self.db_agent.execute_query(query)
            return pd.DataFrame(results, columns=columns)
        except Exception as e:
            raise Exception(f"Analytics query failed: {str(e)}")