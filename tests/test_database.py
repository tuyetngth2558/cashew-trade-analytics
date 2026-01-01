"""
Unit tests for database module
"""

import pytest
import pandas as pd
import sqlite3
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import Database


class TestDatabase:
    """Test suite for Database class"""
    
    @pytest.fixture
    def test_db_path(self, tmp_path):
        """Create temporary database path"""
        return str(tmp_path / "test_contracts.db")
    
    @pytest.fixture
    def db(self, test_db_path):
        """Create Database instance with test database"""
        return Database(test_db_path)
    
    @pytest.fixture
    def sample_df(self):
        """Create sample DataFrame for testing"""
        data = {
            'contract_no.': ['CT001', 'CT002', 'CT003'],
            'contract_date': ['2024-01-15', '2024-02-20', '2024-03-10'],
            'customer_name': ['Customer A', 'Customer B', 'Customer C'],
            'consignee_name': ['Consignee A', 'Consignee B', 'Consignee C'],
            'destination_country': ['USA', 'Germany', 'Japan'],
            'origin': ['Vietnam', 'India', 'Vietnam'],
            'commodity': ['W320', 'W240', 'W450'],
            'quantity': [2, 3, 1],
            'weight_mt': [18.5, 27.3, 16.2],
            'trade_slip_contract_price': [12000, 15000, 10000],
            'trade_slip_total_cost': [10000, 12500, 8500],
            'trade_slip_net_price': [222000, 409500, 162000],
            'anticipated_margin': [37000, 68250, 24300],
            'margin_percentage': [16.67, 16.67, 15.0],
            'third_party_currency': ['USD', 'EUR', 'USD'],
            'sales_terms': ['FOB', 'CIF', 'FOB'],
            'payment_terms': ['LC 30 days', 'LC 60 days', 'TT Advance'],
            'is_invoiced': [1, 1, 0],
            'invoiced_on': ['2024-02-01', '2024-03-15', ''],
            'third_party_invoiced_amount': [220000, 405000, 0],
            'created_on': ['2024-01-15', '2024-02-20', '2024-03-10']
        }
        return pd.DataFrame(data)
    
    def test_database_initialization(self, db, test_db_path):
        """Test database initializes correctly"""
        assert db is not None
        assert db.db_path == test_db_path
        assert os.path.exists(os.path.dirname(test_db_path))
    
    @pytest.mark.database
    def test_create_tables(self, db):
        """Test table creation"""
        db.create_tables()
        
        # Check tables exist
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        assert 'contracts' in tables
        assert 'customer_summary' in tables
        assert 'monthly_revenue' in tables
        
        conn.close()
    
    @pytest.mark.database
    def test_load_data(self, db, sample_df):
        """Test loading data into database"""
        db.create_tables()
        db.load_data(sample_df, 'contracts')
        
        # Query data back
        result = db.query("SELECT COUNT(*) as cnt FROM contracts")
        assert result['cnt'].iloc[0] == 3
    
    @pytest.mark.database
    def test_query_execution(self, db, sample_df):
        """Test SQL query execution"""
        db.create_tables()
        db.load_data(sample_df, 'contracts')
        
        # Test simple query
        result = db.query("SELECT * FROM contracts WHERE customer_name = 'Customer A'")
        assert len(result) == 1
        assert result['customer_name'].iloc[0] == 'Customer A'
    
    @pytest.mark.database
    def test_aggregated_tables(self, db, sample_df):
        """Test creation of aggregated tables"""
        db.create_tables()
        db.load_data(sample_df, 'contracts')
        db.create_aggregated_tables()
        
        # Check customer_summary
        result = db.query("SELECT COUNT(*) as cnt FROM customer_summary")
        assert result['cnt'].iloc[0] == 3
        
        # Check monthly_revenue
        result = db.query("SELECT COUNT(*) as cnt FROM monthly_revenue")
        assert result['cnt'].iloc[0] > 0
    
    @pytest.mark.database
    def test_customer_summary_accuracy(self, db, sample_df):
        """Test customer summary calculations are accurate"""
        db.create_tables()
        db.load_data(sample_df, 'contracts')
        db.create_aggregated_tables()
        
        # Get customer A summary
        result = db.query("""
            SELECT * FROM customer_summary 
            WHERE customer_name = 'Customer A'
        """)
        
        assert result['total_contracts'].iloc[0] == 1
        assert result['total_revenue'].iloc[0] == 222000
    
    @pytest.mark.database
    def test_monthly_revenue_aggregation(self, db, sample_df):
        """Test monthly revenue aggregation"""
        db.create_tables()
        db.load_data(sample_df, 'contracts')
        db.create_aggregated_tables()
        
        result = db.query("SELECT * FROM monthly_revenue ORDER BY month")
        
        # Should have entries for each month
        assert len(result) > 0
        assert 'total_revenue' in result.columns
        assert 'total_contracts' in result.columns


class TestDatabaseQueries:
    """Test suite for database query functions"""
    
    @pytest.fixture
    def populated_db(self, tmp_path):
        """Create and populate a test database"""
        db_path = str(tmp_path / "test.db")
        db = Database(db_path)
        db.create_tables()
        
        # Create sample data
        data = {
            'contract_no.': [f'CT{i:03d}' for i in range(1, 11)],
            'contract_date': ['2024-01-15'] * 5 + ['2024-02-15'] * 5,
            'customer_name': ['Customer A'] * 3 + ['Customer B'] * 3 + ['Customer C'] * 4,
            'consignee_name': ['Consignee X'] * 10,
            'destination_country': ['USA'] * 10,
            'origin': ['Vietnam'] * 10,
            'commodity': ['W320'] * 10,
            'quantity': [2] * 10,
            'weight_mt': [18.5] * 10,
            'trade_slip_contract_price': [12000] * 10,
            'trade_slip_total_cost': [10000] * 10,
            'trade_slip_net_price': [222000] * 10,
            'anticipated_margin': [37000] * 10,
            'margin_percentage': [16.67] * 10,
            'third_party_currency': ['USD'] * 10,
            'sales_terms': ['FOB'] * 10,
            'payment_terms': ['LC 30 days'] * 10,
            'is_invoiced': [1] * 10,
            'invoiced_on': ['2024-02-01'] * 10,
            'third_party_invoiced_amount': [220000] * 10,
            'created_on': ['2024-01-15'] * 10
        }
        df = pd.DataFrame(data)
        db.load_data(df, 'contracts')
        db.create_aggregated_tables()
        
        return db
    
    @pytest.mark.database
    def test_top_customers_query(self, populated_db):
        """Test querying top customers"""
        result = populated_db.query("""
            SELECT customer_name, total_revenue
            FROM customer_summary
            ORDER BY total_revenue DESC
            LIMIT 3
        """)
        
        assert len(result) == 3
        assert 'Customer C' in result['customer_name'].values
    
    @pytest.mark.database
    def test_date_range_query(self, populated_db):
        """Test querying by date range"""
        result = populated_db.query("""
            SELECT COUNT(*) as cnt
            FROM contracts
            WHERE contract_date >= '2024-02-01'
        """)
        
        assert result['cnt'].iloc[0] == 5
    
    @pytest.mark.database
    def test_revenue_by_month(self, populated_db):
        """Test monthly revenue query"""
        result = populated_db.query("""
            SELECT month, total_revenue
            FROM monthly_revenue
            ORDER BY month
        """)
        
        assert len(result) > 0
        assert result['total_revenue'].sum() > 0


@pytest.mark.slow
@pytest.mark.database
class TestDatabasePerformance:
    """Test suite for database performance"""
    
    def test_large_dataset_load(self, tmp_path):
        """Test loading large dataset"""
        db_path = str(tmp_path / "large_test.db")
        db = Database(db_path)
        db.create_tables()
        
        # Create large dataset (1000 rows)
        n = 1000
        data = {
            'contract_no.': [f'CT{i:05d}' for i in range(n)],
            'contract_date': ['2024-01-15'] * n,
            'customer_name': [f'Customer {i % 50}' for i in range(n)],
            'consignee_name': ['Consignee X'] * n,
            'destination_country': ['USA'] * n,
            'origin': ['Vietnam'] * n,
            'commodity': ['W320'] * n,
            'quantity': [2] * n,
            'weight_mt': [18.5] * n,
            'trade_slip_contract_price': [12000] * n,
            'trade_slip_total_cost': [10000] * n,
            'trade_slip_net_price': [222000] * n,
            'anticipated_margin': [37000] * n,
            'margin_percentage': [16.67] * n,
            'third_party_currency': ['USD'] * n,
            'sales_terms': ['FOB'] * n,
            'payment_terms': ['LC 30 days'] * n,
            'is_invoiced': [1] * n,
            'invoiced_on': ['2024-02-01'] * n,
            'third_party_invoiced_amount': [220000] * n,
            'created_on': ['2024-01-15'] * n
        }
        df = pd.DataFrame(data)
        
        # Load and verify
        db.load_data(df, 'contracts')
        result = db.query("SELECT COUNT(*) as cnt FROM contracts")
        assert result['cnt'].iloc[0] == n


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
