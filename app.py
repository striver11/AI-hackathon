from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from agents.db_agent import DatabaseAgent
from agents.schema_agent import SchemaAgent
from agents.sql_agent import SQLGeneratorAgent
from agents.analytics_agent import AnalyticsAgent
from config import APP_CONFIG

# Page Configuration
st.set_page_config(
    page_title=APP_CONFIG["title"],
    page_icon=APP_CONFIG["icon"],
    layout=APP_CONFIG["layout"]
)

# Custom CSS
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(120deg, #1f77b4, #17becf);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .metric-card h3 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .metric-card p {
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(120deg, #1f77b4, #17becf);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(31,119,180,0.3);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: 600;
        padding: 1rem 2rem;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #e3f2fd;
        border-left: 5px solid #1f77b4;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* SQL code block */
    .sql-block {
        background-color: #282c34;
        color: #61dafb;
        padding: 1rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize agents
@st.cache_resource
def init_agents():
    return {
        'db': DatabaseAgent(),
        'schema': SchemaAgent(),
        'sql': SQLGeneratorAgent(),
        'analytics': AnalyticsAgent()
    }

agents = init_agents()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/database.png", width=150)
    st.markdown("### 🎯 Navigation")
    
    page = st.radio(
        "",
        ["🏠 Dashboard", "💬 Query Assistant", "📊 Database Schema", "📈 Analytics"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📚 Quick Guide")
    st.markdown("""
    **Dashboard**: Overview and key metrics
    
    **Query Assistant**: Ask questions in plain English
    
    **Database Schema**: View table structures
    
    **Analytics**: Pre-built reports and insights
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    st.info(f"**Database**: SQLite\n**Model**: Gemini 2.5 Flash")

# Main content
st.markdown('<p class="main-header">🔍 Smart Data Analytics Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Query your insurance database using natural language - No SQL required!</p>', unsafe_allow_html=True)

# PAGE 1: DASHBOARD
if page == "🏠 Dashboard":
    st.markdown("## 📊 Executive Dashboard")
    
    # Get quick stats
    stats = agents['analytics'].get_quick_stats()
    
    # Display metrics in cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <h3>{stats.get('total_accounts', 0):,}</h3>
            <p>👥 Total Accounts</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h3>{stats.get('active_policies', 0):,}</h3>
            <p>📋 Active Policies</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <h3>${stats.get('total_premium', 0):,.2f}</h3>
            <p>💰 Total Premium Revenue</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <h3>{stats.get('total_claims', 0):,}</h3>
            <p>📝 Total Claims</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Policy Distribution")
        policy_dist = agents['analytics'].get_policy_distribution()
        if not policy_dist.empty:
            fig = px.pie(
                policy_dist, 
                values='count', 
                names='policy_type',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🏆 Top Performing Agents")
        top_agents = agents['analytics'].get_top_agents()
        if not top_agents.empty:
            fig = px.bar(
                top_agents,
                x='name',
                y='total_premium',
                color='total_policies',
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=400, xaxis_title="Agent", yaxis_title="Total Premium ($)")
            st.plotly_chart(fig, use_container_width=True)
    
    # Claims summary
    st.markdown("### 📋 Claims Overview")
    claims_summary = agents['analytics'].get_claims_summary()
    if not claims_summary.empty:
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = go.Figure(data=[
                go.Bar(name='Requested', x=claims_summary['status'], y=claims_summary['total_requested']),
                go.Bar(name='Approved', x=claims_summary['status'], y=claims_summary['total_approved'])
            ])
            fig.update_layout(barmode='group', height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(claims_summary, use_container_width=True, height=350)

# PAGE 2: QUERY ASSISTANT
elif page == "💬 Query Assistant":
    st.markdown("## 💬 Natural Language Query Assistant")
    
    # Example questions in expandable sections
    with st.expander("📚 See Example Questions", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Account Queries:**
            - How many accounts are from California?
            - Show all accounts with their emails
            - List accounts who are over 40 years old
            
            **Policy Queries:**
            - Show all active life insurance policies
            - What is the average premium amount?
            - List policies expiring in 2024
            
            **Claims Queries:**
            - Show all pending claims
            - What is the total approved claim amount?
            - List accounts with claims over $5000
            """)
        
        with col2:
            st.markdown("""
            **Agent Queries:**
            - Which agent has sold the most policies?
            - Show all active agents
            - List agents with commission rates above 5%
            
            **Complex Queries:**
            - Show accounts who have filed claims
            - List agents with their total policy count
            - Display accounts with multiple policy types
            - Which accounts have both auto and health insurance?
            """)
    
    # Query input
    st.markdown("### 🔍 Ask Your Question")
    question = st.text_area(
        "",
        placeholder="e.g., Show me all accounts from Texas who have life insurance policies",
        height=100,
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        submit = st.button("🚀 Generate & Execute Query", use_container_width=True)
    
    if submit and question:
        with st.spinner("🤔 Analyzing your question..."):
            try:
                # Generate SQL
                sql_query = agents['sql'].generate_sql(question)
                
                # Display generated SQL
                st.markdown("### 📝 Generated SQL Query")
                st.code(sql_query, language="sql")
                
                # Execute query
                with st.spinner("⚙️ Executing query..."):
                    results, columns = agents['db'].execute_query(sql_query)
                
                # Display results
                st.markdown("### 📊 Query Results")
                
                if results:
                    df = pd.DataFrame(results, columns=columns)
                    
                    # Show metrics if single value
                    if len(df) == 1 and len(df.columns) == 1:
                        value = df.iloc[0, 0]
                        st.markdown(f"""
                        <div class="metric-card" style="max-width: 300px; margin: 2rem auto;">
                            <h3>{value:,}</h3>
                            <p>{columns[0].replace('_', ' ').title()}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.dataframe(df, use_container_width=True)
                        
                        # Download button
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results as CSV",
                            data=csv,
                            file_name="query_results.csv",
                            mime="text/csv"
                        )
                    
                    st.success(f"✅ Query executed successfully! Found {len(results)} record(s)")
                else:
                    st.info("ℹ️ No records found for this query.")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Try rephrasing your question or check the example questions above.")
    
    elif submit:
        st.warning("⚠️ Please enter a question first!")

# PAGE 3: DATABASE SCHEMA
elif page == "📊 Database Schema":
    st.markdown("## 📊 Database Schema Explorer")
    
    tables = agents['db'].get_tables()
    
    # Table selector
    selected_table = st.selectbox("🔍 Select a table to explore", tables)
    
    if selected_table:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### 📋 Schema: {selected_table.upper()}")
            schema_df = agents['db'].get_table_schema(selected_table)
            st.dataframe(schema_df, use_container_width=True)
        
        with col2:
            row_count = agents['db'].get_row_count(selected_table)
            st.markdown(f"""
            <div class="metric-card">
                <h3>{row_count:,}</h3>
                <p>Total Rows</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"### 👀 Sample Data from {selected_table.upper()}")
        sample_data = agents['db'].get_sample_data(selected_table, limit=10)
        st.dataframe(sample_data, use_container_width=True)
    
    # Database statistics
    st.markdown("### 📈 Database Statistics")
    db_stats = agents['db'].get_database_stats()
    
    stats_df = pd.DataFrame(db_stats['tables'])
    fig = px.bar(
        stats_df,
        x='name',
        y='row_count',
        title='Records per Table',
        color='row_count',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)

# PAGE 4: ANALYTICS
elif page == "📈 Analytics":
    st.markdown("## 📈 Advanced Analytics & Reports")
    
    tab1, tab2, tab3 = st.tabs(["💰 Revenue Analysis", "📋 Policy Insights", "⚠️ Risk Assessment"])
    
    with tab1:
        st.markdown("### 💰 Revenue & Premium Analysis")
        
        query = """
        SELECT 
            p.policy_type,
            COUNT(*) as policy_count,
            SUM(p.premium_amount) as total_premium,
            AVG(p.premium_amount) as avg_premium,
            SUM(p.coverage_amount) as total_coverage
        FROM policies p
        WHERE p.status = 'Active'
        GROUP BY p.policy_type
        ORDER BY total_premium DESC
        """
        
        results, columns = agents['db'].execute_query(query)
        df = pd.DataFrame(results, columns=columns)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                df,
                x='policy_type',
                y='total_premium',
                title='Total Premium by Policy Type',
                color='total_premium',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(
                df,
                x='policy_count',
                y='avg_premium',
                size='total_coverage',
                color='policy_type',
                title='Policy Count vs Average Premium'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.markdown("### 📋 Policy Distribution & Trends")
        
        query = """
        SELECT 
            c.state,
            COUNT(p.policy_id) as total_policies,
            SUM(p.premium_amount) as total_premium
        FROM account c
        JOIN policies p ON c.account_id = p.account_id
        WHERE p.status = 'Active'
        GROUP BY c.state
        ORDER BY total_policies DESC
        LIMIT 10
        """
        
        results, columns = agents['db'].execute_query(query)
        df = pd.DataFrame(results, columns=columns)
        
        fig = px.treemap(
            df,
            path=['state'],
            values='total_policies',
            color='total_premium',
            title='Policies by State'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### ⚠️ Claims Risk Assessment")
        
        query = """
        SELECT 
            p.policy_type,
            COUNT(cl.claim_id) as total_claims,
            SUM(cl.claim_amount) as total_claim_amount,
            SUM(cl.approved_amount) as total_approved,
            ROUND(100.0 * SUM(cl.approved_amount) / SUM(cl.claim_amount), 2) as approval_rate
        FROM policies p
        LEFT JOIN claims cl ON p.policy_id = cl.policy_id
        WHERE cl.claim_id IS NOT NULL
        GROUP BY p.policy_type
        """
        
        results, columns = agents['db'].execute_query(query)
        df = pd.DataFrame(results, columns=columns)
        
        fig = go.Figure(data=[
            go.Bar(name='Claimed', x=df['policy_type'], y=df['total_claim_amount']),
            go.Bar(name='Approved', x=df['policy_type'], y=df['total_approved'])
        ])
        fig.update_layout(barmode='group', title='Claim Amount vs Approved Amount by Policy Type')
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p style='font-size: 0.9rem;'>
        🤖 Powered by <strong>Google Gemini AI</strong> | 
        💾 Portable to <strong>Databricks</strong> | 
        Built with ❤️ using <strong>Streamlit</strong>
    </p>
</div>
""", unsafe_allow_html=True)