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
        text-align: center;
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
    
    .metric-card-green {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    }
    
    .metric-card-blue {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .metric-card-orange {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    .metric-card-purple {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .metric-card-pink {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .metric-card-teal {
        background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
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
        color: black;
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
# In app.py, update the sidebar section:

with st.sidebar:
    # Add company logo
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <img src='https://img.icons8.com/clouds/200/analytics.png' width='120'/>
            <h2 style='color: #1f77b4; margin: 0.5rem 0; font-size: 2rem;'>InsightIQ</h2>
            <p style='color: #666; font-size: 0.9rem; margin: 0; font-size: 1.2rem'>Insurance Analytics</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎯 Navigation")
    
    page = st.radio(
        "",
        ["🏠 Dashboard", "💬 Query Assistant", "📈 Dynamic Analytics"],
        label_visibility="collapsed"
    )
    
    # ... rest of sidebar code
    
    st.markdown("---")
    st.markdown("### 📚 Quick Guide")
    st.markdown("""
    **Dashboard**: Overview and key metrics
    
    **Query Assistant**: Ask questions in plain English
    
    **Dynamic Analytics**: Generate custom charts and reports
    """)
    
    st.markdown("---")
    st.markdown("### 💼 Market Types")
    st.markdown("""
    • Middle Market
    • National Program
    • National Account
    • Public Sector
    """)
    
    st.markdown("### 📋 Policy Types")
    st.markdown("""
    • **GC**: Guaranteed Cost
    • **LS**: Loss Sensitive
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    st.info(f"**Database**: SQLite\n**Model**: Gemini 2.5 Flash")

# Main content
st.markdown('<p class="main-header">🔍 Smart Insurance Analytics</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Insurance Data Analytics Platform</p>', unsafe_allow_html=True)

# PAGE 1: DASHBOARD
if page == "🏠 Dashboard":
    st.markdown("## 📊 Executive Dashboard")
    
    # Get quick stats
    stats = agents['analytics'].get_quick_stats()
    
    # Display metrics in cards - Row 1
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card metric-card-purple">
            <h3>{stats.get('total_accounts', 0):,}</h3>
            <p>👥 Total Accounts</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card metric-card-blue">
            <h3>{stats.get('active_policies', 0):,}</h3>
            <p>📋 Active Policies</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card metric-card-green">
            <h3>${stats.get('total_premium', 0):,.0f}</h3>
            <p>💰 Total Premium Revenue</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display metrics in cards - Row 2
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card metric-card-orange">
            <h3>{stats.get('ongoing_claims', 0):,}</h3>
            <p>⏳ Ongoing Claims</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card metric-card-pink">
            <h3>{stats.get('total_quoted_policies', 0):,}</h3>
            <p>📄 Total Quoted Policies</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card metric-card-teal">
            <h3>{stats.get('total_issued_policies', 0):,}</h3>
            <p>✅ Total Issued Policies</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts - Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Distribution by Market Type")
        market_dist = agents['analytics'].get_market_distribution()
        if not market_dist.empty:
            fig = px.pie(
                market_dist, 
                values='count', 
                names='market_type',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No market data available")
    
    with col2:
        st.markdown("### 📋 Distribution by Policy Type")
        policy_dist = agents['analytics'].get_policy_type_distribution()
        if not policy_dist.empty:
            fig = px.bar(
                policy_dist,
                x='policy_type_name',
                y='total_premium',
                color='count',
                labels={'policy_type_name': 'Policy Type', 'total_premium': 'Total Premium ($)'},
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No policy type data available")
    
    # Charts - Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Top Performing Agents")
        top_agents = agents['analytics'].get_top_agents()
        if not top_agents.empty:
            fig = px.bar(
                top_agents,
                x='name',
                y='total_premium',
                color='total_policies',
                labels={'name': 'Agent', 'total_premium': 'Total Premium ($)'},
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=400, xaxis_title="Agent", yaxis_title="Total Premium ($)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No agent data available")
    
    with col2:
        st.markdown("### 📋 Claims Overview")
        claims_summary = agents['analytics'].get_claims_summary()
        if not claims_summary.empty:
            fig = go.Figure(data=[
                go.Bar(name='Requested', x=claims_summary['status'], y=claims_summary['total_requested']),
                go.Bar(name='Approved', x=claims_summary['status'], y=claims_summary['total_approved'])
            ])
            fig.update_layout(barmode='group', height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No claims data available")
    
    # Ongoing Claims Summary
    st.markdown("### ⏳ Ongoing Claims Status")
    ongoing_summary = agents['analytics'].get_ongoing_claims_summary()
    if not ongoing_summary.empty:
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = px.bar(
                ongoing_summary,
                x='current_status',
                y='total_amount',
                color='count',
                labels={'current_status': 'Status', 'total_amount': 'Total Amount ($)'},
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(ongoing_summary, use_container_width=True, height=350)
    else:
        st.info("No ongoing claims data available")
    
    # Quote Conversion Metrics
    st.markdown("### 📈 Quote Conversion Metrics")
    conversion = agents['analytics'].get_quote_conversion_metrics()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Quotes", conversion.get('total_quotes', 0))
    with col2:
        st.metric("Accepted Quotes", conversion.get('accepted_quotes', 0))
    with col3:
        st.metric("Conversion Rate", f"{conversion.get('conversion_rate', 0)}%")

# PAGE 2: QUERY ASSISTANT
elif page == "💬 Query Assistant":
    st.markdown("## 💬 Natural Language Query Assistant")
    
    # Example questions in expandable sections
    with st.expander("📚 See Example Questions", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Account & Policy Queries:**
            - How many accounts are in each state?
            - Show all Middle Market policies
            - List National Account accounts with premiums over $100k
            - Which accounts have both GC and LS policies?
            
            **Market Analysis:**
            - What is the total premium by market type?
            - Show average premium for Public Sector
            - Compare GC vs LS policy counts
            - Which market has the highest claim ratio?
            
            **Claims Queries:**
            - Show all ongoing claims with amounts over $100k
            - List pending claims by account
            - What's the total claim exposure?
            - Show claims by adjuster
            """)
        
        with col2:
            st.markdown("""
            **Agent Performance:**
            - Which agent has the most policies?
            - Show agents ranked by total premium
            - List agents handling Public Sector accounts
            
            **Quote & Issuance:**
            - Show all pending quotes
            - What's the quote acceptance rate by market?
            - List recently issued policies
            - Show quotes that expired without acceptance
            
            **Complex Queries:**
            - Show accounts with ongoing claims and their policies
            - Compare premium vs claims by market type
            - List agents with National Account clients
            - Show policy issuance trends by month
            """)
    
    # Query input
    st.markdown("### 🔍 Ask Your Question")
    question = st.text_area(
        "",
        placeholder="e.g., Show me all Middle Market policies with premiums over $50,000",
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

# PAGE 3: DYNAMIC ANALYTICS
elif page == "📈 Dynamic Analytics":
    st.markdown("## 📈 Dynamic Analytics Generator")
    
    st.markdown("""
    <div class="info-box">
        <strong>💡 How it works:</strong> Describe the analysis you want, and AI will generate 
        the SQL query, fetch the data, and create visualizations automatically!
    </div>
    """, unsafe_allow_html=True)
    
    # Analytics request input
    st.markdown("### 🎯 What analysis would you like to see?")
    
    # Quick options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Premium by Market Type", use_container_width=True):
            st.session_state.analytics_request = "Show total premium amount grouped by market type"
    
    with col2:
        if st.button("📋 Policy Distribution", use_container_width=True):
            st.session_state.analytics_request = "Show count of policies by market type and policy type"
    
    with col3:
        if st.button("⚠️ Claim Risk Assessment", use_container_width=True):
            st.session_state.analytics_request = "Show total claim amount vs total premium by market type to assess risk"
    
    # More options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏆 Agent Performance", use_container_width=True):
            st.session_state.analytics_request = "Show agents with their total policies and premium amount ranked by premium"
    
    with col2:
        if st.button("📈 Quote Conversion", use_container_width=True):
            st.session_state.analytics_request = "Show quote conversion rate by market type with counts and percentages"
    
    with col3:
        if st.button("⏳ Ongoing Claims Analysis", use_container_width=True):
            st.session_state.analytics_request = "Show ongoing claims grouped by status with total amounts"
    
    st.markdown("---")
    
    # Custom request
    analytics_request = st.text_area(
        "Or describe your custom analysis:",
        value=st.session_state.get('analytics_request', ''),
        placeholder="e.g., Show me the average premium amount by policy type for each market segment",
        height=100
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        generate = st.button("🎨 Generate Analytics", use_container_width=True)
    
    if generate and analytics_request:
        with st.spinner("🔮 Generating analytics..."):
            try:
                # Generate SQL for analytics
                sql_query = agents['sql'].generate_analytics_sql(analytics_request)
                
                # Display generated SQL
                with st.expander("📝 View Generated SQL Query"):
                    st.code(sql_query, language="sql")
                
                # Execute query
                with st.spinner("⚙️ Fetching data..."):
                    results, columns = agents['db'].execute_query(sql_query)
                
                if results and len(results) > 0:
                    df = pd.DataFrame(results, columns=columns)
                    
                    st.markdown("### 📊 Analysis Results")
                    
                    # Display data table
                    st.dataframe(df, use_container_width=True)
                    
                    # Auto-generate appropriate visualization
                    st.markdown("### 📈 Visualization")
                    
                    # Determine chart type based on data structure
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                    
                    if len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
                        # Create appropriate chart
                        if len(df) <= 10:  # Bar chart for small datasets
                            fig = px.bar(
                                df,
                                x=categorical_cols[0],
                                y=numeric_cols[0],
                                color=numeric_cols[0] if len(numeric_cols) == 1 else numeric_cols[1],
                                title=analytics_request,
                                color_continuous_scale='Viridis'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Add pie chart if only one numeric column
                            if len(numeric_cols) == 1:
                                fig2 = px.pie(
                                    df,
                                    values=numeric_cols[0],
                                    names=categorical_cols[0],
                                    title=f"Distribution of {numeric_cols[0]}"
                                )
                                st.plotly_chart(fig2, use_container_width=True)
                        
                        elif len(numeric_cols) >= 2:  # Grouped bar for multiple metrics
                            # Melt dataframe for grouped bars
                            fig = go.Figure()
                            for col in numeric_cols:
                                fig.add_trace(go.Bar(
                                    x=df[categorical_cols[0]],
                                    y=df[col],
                                    name=col
                                ))
                            fig.update_layout(
                                barmode='group',
                                title=analytics_request,
                                height=500
                            )
                            st.plotly_chart(fig, use_container_width=True)
                    
                    elif len(numeric_cols) >= 2:  # Scatter plot for numeric comparisons
                        fig = px.scatter(
                            df,
                            x=numeric_cols[0],
                            y=numeric_cols[1],
                            size=numeric_cols[1] if len(numeric_cols) > 1 else None,
                            title=analytics_request,
                            labels={numeric_cols[0]: numeric_cols[0].replace('_', ' ').title(),
                                   numeric_cols[1]: numeric_cols[1].replace('_', ' ').title()}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Download option
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Analysis as CSV",
                        data=csv,
                        file_name="analytics_results.csv",
                        mime="text/csv"
                    )
                    
                    st.success(f"✅ Analysis complete! Generated insights from {len(results)} data points")
                
                else:
                    st.warning("⚠️ No data found for this analysis. Try a different query.")
                    
            except Exception as e:
                st.error(f"❌ Error generating analytics: {str(e)}")
                st.info("💡 Try rephrasing your request or use one of the quick options above.")
    
    elif generate:
        st.warning("⚠️ Please describe the analysis you want!")
    
    # Clear session state if needed
    if 'analytics_request' in st.session_state and not analytics_request:
        del st.session_state.analytics_request

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