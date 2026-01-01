"""
Integration tests for full data pipeline
"""

import pytest
import pandas as pd
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import Database


@pytest.mark.integration
class TestDataPipeline:
    """Integration tests for complete data pipeline"""
    
    def test_sample_data_exists(self):
        """Test that sample data file exists"""
        sample_path = 'data/sample/sample_data.csv'
        assert os.path.exists(sample_path), "Sample data file not found"
    
    def test_load_sample_data(self):
        """Test loading sample data"""
        df = pd.read_csv('data/sample/sample_data.csv')
        
        assert len(df) > 0, "Sample data is empty"
        assert 'contract_no.' in df.columns
        assert 'customer_name' in df.columns
        assert 'trade_slip_net_price' in df.columns
    
    def test_sample_data_quality(self):
        """Test sample data quality"""
        df = pd.read_csv('data/sample/sample_data.csv')
        
        # Check no empty customer names
        assert df['customer_name'].notna().all()
        assert (df['customer_name'] != '').all()
        
        # Check positive prices
        assert (df['trade_slip_net_price'] > 0).all()
        
        # Check positive weights
        assert (df['weight_mt'] > 0).all()
    
    def test_end_to_end_pipeline(self, tmp_path):
        """Test complete pipeline from CSV to database"""
        # Load sample data
        df = pd.read_csv('data/sample/sample_data.csv')
        
        # Create test database
        db_path = str(tmp_path / "pipeline_test.db")
        db = Database(db_path)
        
        # Create tables
        db.create_tables()
        
        # Load data
        db.load_data(df, 'contracts')
        
        # Create aggregations
        db.create_aggregated_tables()
        
        # Verify data loaded
        result = db.query("SELECT COUNT(*) as cnt FROM contracts")
        assert result['cnt'].iloc[0] == len(df)
        
        # Verify customer summary created
        customers = db.query("SELECT COUNT(*) as cnt FROM customer_summary")
        assert customers['cnt'].iloc[0] > 0
        
        # Verify monthly revenue created
        monthly = db.query("SELECT COUNT(*) as cnt FROM monthly_revenue")
        assert monthly['cnt'].iloc[0] > 0
    
    def test_data_consistency(self, tmp_path):
        """Test data consistency across pipeline"""
        df = pd.read_csv('data/sample/sample_data.csv')
        
        # Calculate expected totals
        expected_total_revenue = df['trade_slip_net_price'].sum()
        expected_customers = df['customer_name'].nunique()
        
        # Load to database
        db_path = str(tmp_path / "consistency_test.db")
        db = Database(db_path)
        db.create_tables()
        db.load_data(df, 'contracts')
        db.create_aggregated_tables()
        
        # Verify totals match
        total_revenue = db.query("SELECT SUM(net_price) as total FROM contracts")
        assert abs(total_revenue['total'].iloc[0] - expected_total_revenue) < 1
        
        # Verify customer count
        customer_count = db.query("SELECT COUNT(DISTINCT customer_name) as cnt FROM contracts")
        assert customer_count['cnt'].iloc[0] == expected_customers


@pytest.mark.integration
class TestDashboardData:
    """Integration tests for dashboard data requirements"""
    
    @pytest.fixture
    def test_db(self, tmp_path):
        """Create populated test database"""
        df = pd.read_csv('data/sample/sample_data.csv')
        db_path = str(tmp_path / "dashboard_test.db")
        db = Database(db_path)
        db.create_tables()
        db.load_data(df, 'contracts')
        db.create_aggregated_tables()
        return db
    
    def test_dashboard_metrics_query(self, test_db):
        """Test queries for dashboard metrics"""
        # Total revenue
        revenue = test_db.query("SELECT SUM(net_price) as total FROM contracts")
        assert revenue['total'].iloc[0] > 0
        
        # Total contracts
        contracts = test_db.query("SELECT COUNT(*) as cnt FROM contracts")
        assert contracts['cnt'].iloc[0] > 0
        
        # Average margin
        margin = test_db.query("SELECT AVG(margin_percentage) as avg_margin FROM contracts")
        assert margin['avg_margin'].iloc[0] is not None
    
    def test_top_customers_data(self, test_db):
        """Test top customers query for dashboard"""
        top_customers = test_db.query("""
            SELECT customer_name, total_revenue, total_contracts
            FROM customer_summary
            ORDER BY total_revenue DESC
            LIMIT 10
        """)
        
        assert len(top_customers) > 0
        assert 'customer_name' in top_customers.columns
        assert 'total_revenue' in top_customers.columns
    
    def test_revenue_trends_data(self, test_db):
        """Test revenue trends query for dashboard"""
        trends = test_db.query("""
            SELECT month, total_revenue, total_contracts
            FROM monthly_revenue
            ORDER BY month
        """)
        
        assert len(trends) > 0
        assert 'month' in trends.columns
        assert 'total_revenue' in trends.columns
    
    def test_product_distribution(self, test_db):
        """Test product distribution query"""
        products = test_db.query("""
            SELECT commodity, COUNT(*) as cnt, SUM(net_price) as revenue
            FROM contracts
            GROUP BY commodity
            ORDER BY revenue DESC
        """)
        
        assert len(products) > 0
        assert 'commodity' in products.columns


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
