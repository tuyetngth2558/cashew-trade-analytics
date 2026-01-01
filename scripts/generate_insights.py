"""
Generate Business Insights and Charts
Creates visualizations and analysis reports
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Create output directory
OUTPUT_DIR = 'assets/insights'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_data():
    """Load sample data"""
    df = pd.read_csv('data/sample/sample_data.csv')
    df['contract_date'] = pd.to_datetime(df['contract_date'])
    df['invoiced_on'] = pd.to_datetime(df['invoiced_on'], errors='coerce')
    return df


def generate_revenue_trends(df):
    """Generate revenue trends analysis"""
    print("\n📈 Generating Revenue Trends...")
    
    # Monthly revenue
    df['month'] = df['contract_date'].dt.to_period('M')
    monthly_revenue = df.groupby('month').agg({
        'trade_slip_net_price': 'sum',
        'contract_no.': 'count'
    }).reset_index()
    monthly_revenue['month'] = monthly_revenue['month'].astype(str)
    
    # Create interactive plot
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Monthly Revenue Trend', 'Number of Contracts'),
        vertical_spacing=0.15
    )
    
    # Revenue line
    fig.add_trace(
        go.Scatter(
            x=monthly_revenue['month'],
            y=monthly_revenue['trade_slip_net_price'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#2E86AB', width=3),
            marker=dict(size=8)
        ),
        row=1, col=1
    )
    
    # Contracts bar
    fig.add_trace(
        go.Bar(
            x=monthly_revenue['month'],
            y=monthly_revenue['contract_no.'],
            name='Contracts',
            marker_color='#A23B72'
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        height=700,
        title_text="Revenue Trends Over Time",
        showlegend=False
    )
    
    fig.write_html(f'{OUTPUT_DIR}/revenue_trends.html')
    print(f"   ✓ Saved: {OUTPUT_DIR}/revenue_trends.html")


def generate_customer_analysis(df):
    """Generate customer segmentation analysis"""
    print("\n👥 Generating Customer Analysis...")
    
    # Top customers
    customer_revenue = df.groupby('customer_name').agg({
        'trade_slip_net_price': 'sum',
        'contract_no.': 'count',
        'margin_percentage': 'mean'
    }).reset_index()
    customer_revenue.columns = ['customer_name', 'total_revenue', 'contracts', 'avg_margin']
    customer_revenue = customer_revenue.sort_values('total_revenue', ascending=False).head(10)
    
    # Create plot
    fig = px.bar(
        customer_revenue,
        x='total_revenue',
        y='customer_name',
        orientation='h',
        title='Top 10 Customers by Revenue',
        labels={'total_revenue': 'Total Revenue ($)', 'customer_name': 'Customer'},
        color='avg_margin',
        color_continuous_scale='RdYlGn',
        text='contracts'
    )
    
    fig.update_traces(texttemplate='%{text} contracts', textposition='outside')
    fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
    
    fig.write_html(f'{OUTPUT_DIR}/top_customers.html')
    print(f"   ✓ Saved: {OUTPUT_DIR}/top_customers.html")


def generate_product_analysis(df):
    """Generate product distribution analysis"""
    print("\n🥜 Generating Product Analysis...")
    
    # Product distribution
    product_stats = df.groupby('commodity').agg({
        'trade_slip_net_price': 'sum',
        'weight_mt': 'sum',
        'contract_no.': 'count'
    }).reset_index()
    product_stats.columns = ['commodity', 'revenue', 'weight', 'contracts']
    
    # Create pie chart
    fig = px.pie(
        product_stats,
        values='revenue',
        names='commodity',
        title='Revenue Distribution by Cashew Grade',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)
    
    fig.write_html(f'{OUTPUT_DIR}/product_distribution.html')
    print(f"   ✓ Saved: {OUTPUT_DIR}/product_distribution.html")


def generate_geographic_analysis(df):
    """Generate geographic distribution analysis"""
    print("\n🌍 Generating Geographic Analysis...")
    
    # Country distribution
    country_stats = df.groupby('destination_country').agg({
        'trade_slip_net_price': 'sum',
        'contract_no.': 'count'
    }).reset_index()
    country_stats.columns = ['country', 'revenue', 'contracts']
    country_stats = country_stats.sort_values('revenue', ascending=False).head(10)
    
    # Create map
    fig = px.bar(
        country_stats,
        x='country',
        y='revenue',
        title='Revenue by Destination Country',
        labels={'revenue': 'Total Revenue ($)', 'country': 'Country'},
        color='revenue',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(height=500, xaxis_tickangle=-45)
    
    fig.write_html(f'{OUTPUT_DIR}/geographic_distribution.html')
    print(f"   ✓ Saved: {OUTPUT_DIR}/geographic_distribution.html")


def generate_margin_analysis(df):
    """Generate margin analysis"""
    print("\n💰 Generating Margin Analysis...")
    
    # Margin distribution
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=df['margin_percentage'],
        nbinsx=30,
        name='Margin Distribution',
        marker_color='#06A77D'
    ))
    
    # Add average line
    avg_margin = df['margin_percentage'].mean()
    fig.add_vline(
        x=avg_margin,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Average: {avg_margin:.2f}%"
    )
    
    fig.update_layout(
        title='Profit Margin Distribution',
        xaxis_title='Margin Percentage (%)',
        yaxis_title='Number of Contracts',
        height=500
    )
    
    fig.write_html(f'{OUTPUT_DIR}/margin_distribution.html')
    print(f"   ✓ Saved: {OUTPUT_DIR}/margin_distribution.html")


def generate_summary_stats(df):
    """Generate summary statistics"""
    print("\n📊 Generating Summary Statistics...")
    
    stats = {
        'Total Contracts': len(df),
        'Total Revenue': f"${df['trade_slip_net_price'].sum():,.2f}",
        'Average Contract Value': f"${df['trade_slip_net_price'].mean():,.2f}",
        'Total Weight (MT)': f"{df['weight_mt'].sum():,.2f}",
        'Average Margin': f"{df['margin_percentage'].mean():.2f}%",
        'Number of Customers': df['customer_name'].nunique(),
        'Number of Countries': df['destination_country'].nunique(),
        'Invoiced Contracts': f"{df['is_invoiced'].sum()} ({df['is_invoiced'].mean()*100:.1f}%)",
        'Date Range': f"{df['contract_date'].min().strftime('%Y-%m-%d')} to {df['contract_date'].max().strftime('%Y-%m-%d')}"
    }
    
    # Save to file
    with open(f'{OUTPUT_DIR}/summary_stats.txt', 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("CASHEW TRADE ANALYTICS - SUMMARY STATISTICS\n")
        f.write("=" * 60 + "\n\n")
        for key, value in stats.items():
            f.write(f"{key:.<40} {value}\n")
        f.write("\n" + "=" * 60 + "\n")
    
    print(f"   ✓ Saved: {OUTPUT_DIR}/summary_stats.txt")
    
    return stats


def main():
    """Main execution"""
    print("=" * 60)
    print("📊 GENERATING BUSINESS INSIGHTS")
    print("=" * 60)
    
    # Load data
    print("\n📂 Loading data...")
    df = load_data()
    print(f"✅ Loaded {len(df)} records")
    
    # Generate all insights
    generate_revenue_trends(df)
    generate_customer_analysis(df)
    generate_product_analysis(df)
    generate_geographic_analysis(df)
    generate_margin_analysis(df)
    stats = generate_summary_stats(df)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📈 KEY INSIGHTS")
    print("=" * 60)
    print(f"Total Revenue: {stats['Total Revenue']}")
    print(f"Average Margin: {stats['Average Margin']}")
    print(f"Top Customer: {df.groupby('customer_name')['trade_slip_net_price'].sum().idxmax()}")
    print(f"Most Popular Product: {df.groupby('commodity')['contract_no.'].count().idxmax()}")
    
    print("\n" + "=" * 60)
    print("✅ INSIGHTS GENERATION COMPLETED!")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
