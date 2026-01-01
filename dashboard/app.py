"""
Streamlit Dashboard
Simple version for beginners
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.database import Database

# Page config
st.set_page_config(
    page_title="Cashew Trade Analytics",
    page_icon="🥜",
    layout="wide"
)

# Title
st.title("🥜 Cashew Trade Analytics Dashboard")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    """Load data from database"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'database', 'contracts.db')
    db = Database(db_path)
    df = db.query("SELECT * FROM contracts")
    df['contract_date'] = pd.to_datetime(df['contract_date'])
    return df

try:
    df = load_data()
    st.success(f"✅ Loaded {len(df)} contracts")
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.stop()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Date range
min_date = df['contract_date'].min().date()
max_date = df['contract_date'].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Customer filter
customers = ['All'] + sorted(df['customer_name'].dropna().unique().tolist())
selected_customer = st.sidebar.selectbox("Select Customer", customers)

# Apply filters
mask = (df['contract_date'].dt.date >= date_range[0]) & \
       (df['contract_date'].dt.date <= date_range[1])

if selected_customer != 'All':
    mask &= (df['customer_name'] == selected_customer)

filtered_df = df[mask]

# KPIs
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = filtered_df['net_price'].sum()
    st.metric("💰 Total Revenue", f"${total_revenue:,.0f}")

with col2:
    avg_margin = filtered_df['margin_percentage'].mean()
    st.metric("📈 Avg Margin", f"{avg_margin:.1f}%")

with col3:
    total_quantity = filtered_df['quantity'].sum()
    st.metric("📦 Total Quantity", f"{total_quantity:,.0f}")

with col4:
    unique_customers = filtered_df['customer_name'].nunique()
    st.metric("👥 Customers", unique_customers)

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Monthly Revenue Trend")
    
    monthly = filtered_df.groupby(
        filtered_df['contract_date'].dt.to_period('M')
    )['net_price'].sum().reset_index()
    monthly['contract_date'] = monthly['contract_date'].astype(str)
    
    fig1 = px.line(
        monthly, 
        x='contract_date', 
        y='net_price',
        labels={'contract_date': 'Month', 'net_price': 'Revenue ($)'}
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🏆 Top 10 Customers")
    
    top_customers = filtered_df.groupby('customer_name')['net_price'].sum().nlargest(10)
    
    fig2 = px.bar(
        x=top_customers.values,
        y=top_customers.index,
        orientation='h',
        labels={'x': 'Revenue ($)', 'y': 'Customer'}
    )
    st.plotly_chart(fig2, use_container_width=True)

# Data table
st.subheader("📋 Recent Contracts")
st.dataframe(
    filtered_df[['contract_no', 'contract_date', 'customer_name', 'net_price', 'margin_percentage']]
    .sort_values('contract_date', ascending=False)
    .head(10),
    use_container_width=True
)

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit | Data updated: " + str(df['contract_date'].max().date()) + "*")