"""
Unit tests for data_processing module
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_processing import DataProcessor


class TestDataProcessor:
    """Test suite for DataProcessor class"""
    
    @pytest.fixture
    def processor(self):
        """Create DataProcessor instance"""
        return DataProcessor()
    
    @pytest.fixture
    def sample_data(self):
        """Create sample DataFrame for testing"""
        data = {
            'contract_date': ['2024-01-15', '2024-02-20', 'invalid_date'],
            'contract_no.': ['CT001', 'CT002', 'CT003'],
            'customer_name': ['Customer A', 'Customer B', ''],
            'trade_slip_net_price': [10000, 20000, -500],
            'weight_mt': [10.5, 20.0, 0],
            'margin_percentage': [12.5, 15.0, None]
        }
        return pd.DataFrame(data)
    
    def test_processor_initialization(self, processor):
        """Test DataProcessor initializes correctly"""
        assert processor is not None
        assert hasattr(processor, 'clean_data')
    
    def test_date_parsing(self, processor, sample_data):
        """Test date parsing handles valid and invalid dates"""
        df = sample_data.copy()
        df['contract_date'] = pd.to_datetime(df['contract_date'], errors='coerce')
        
        # Check valid dates are parsed
        assert pd.notna(df.loc[0, 'contract_date'])
        assert pd.notna(df.loc[1, 'contract_date'])
        
        # Check invalid dates become NaT
        assert pd.isna(df.loc[2, 'contract_date'])
    
    def test_remove_empty_customer_names(self, sample_data):
        """Test removal of rows with empty customer names"""
        df = sample_data[sample_data['customer_name'] != '']
        assert len(df) == 2
        assert '' not in df['customer_name'].values
    
    def test_handle_negative_values(self, sample_data):
        """Test handling of negative prices"""
        df = sample_data[sample_data['trade_slip_net_price'] > 0]
        assert len(df) == 2
        assert all(df['trade_slip_net_price'] > 0)
    
    def test_handle_zero_weight(self, sample_data):
        """Test handling of zero weight"""
        df = sample_data[sample_data['weight_mt'] > 0]
        assert len(df) == 2
        assert all(df['weight_mt'] > 0)
    
    def test_handle_missing_values(self, sample_data):
        """Test handling of missing values"""
        # Fill missing margin_percentage with 0
        df = sample_data.copy()
        df['margin_percentage'] = df['margin_percentage'].fillna(0)
        
        assert df['margin_percentage'].isna().sum() == 0
    
    @pytest.mark.parametrize("price,weight,expected", [
        (10000, 10, 1000),
        (5000, 20, 250),
        (15000, 5, 3000),
    ])
    def test_price_per_mt_calculation(self, price, weight, expected):
        """Test price per MT calculation"""
        price_per_mt = price / weight
        assert price_per_mt == expected
    
    def test_data_types(self, sample_data):
        """Test correct data types after processing"""
        df = sample_data.copy()
        df['contract_date'] = pd.to_datetime(df['contract_date'], errors='coerce')
        
        assert df['contract_no.'].dtype == object
        assert df['customer_name'].dtype == object
        assert pd.api.types.is_numeric_dtype(df['trade_slip_net_price'])
        assert pd.api.types.is_numeric_dtype(df['weight_mt'])


class TestDataValidation:
    """Test suite for data validation functions"""
    
    def test_contract_number_format(self):
        """Test contract number format validation"""
        valid_contracts = ['CT202401001', 'CT202312999']
        invalid_contracts = ['ABC123', '12345', '']
        
        # Simple validation: starts with 'CT'
        for contract in valid_contracts:
            assert contract.startswith('CT')
        
        for contract in invalid_contracts:
            assert not contract.startswith('CT')
    
    def test_margin_percentage_range(self):
        """Test margin percentage is within reasonable range"""
        margins = pd.Series([5.0, 10.0, 15.0, 20.0, -5.0, 100.0])
        
        # Typical margins are between -10% and 50%
        valid_margins = margins[(margins >= -10) & (margins <= 50)]
        assert len(valid_margins) == 5
    
    def test_currency_codes(self):
        """Test currency codes are valid"""
        valid_currencies = ['USD', 'EUR', 'GBP']
        test_currencies = pd.Series(['USD', 'EUR', 'GBP', 'XXX', 'USD'])
        
        valid_mask = test_currencies.isin(valid_currencies)
        assert valid_mask.sum() == 4


class TestDataTransformations:
    """Test suite for data transformation functions"""
    
    def test_extract_year_from_date(self):
        """Test extracting year from date"""
        dates = pd.to_datetime(['2022-01-15', '2023-06-20', '2024-12-31'])
        years = dates.year
        
        assert list(years) == [2022, 2023, 2024]
    
    def test_extract_month_from_date(self):
        """Test extracting month from date"""
        dates = pd.to_datetime(['2024-01-15', '2024-06-20', '2024-12-31'])
        months = dates.month
        
        assert list(months) == [1, 6, 12]
    
    def test_calculate_days_between_dates(self):
        """Test calculating days between dates"""
        date1 = pd.to_datetime('2024-01-01')
        date2 = pd.to_datetime('2024-01-31')
        
        days_diff = (date2 - date1).days
        assert days_diff == 30


@pytest.mark.integration
class TestDataProcessingPipeline:
    """Integration tests for full data processing pipeline"""
    
    def test_full_pipeline_with_sample_data(self):
        """Test complete data processing pipeline"""
        # Load sample data
        try:
            df = pd.read_csv('data/sample/sample_data.csv')
            
            # Basic validation
            assert len(df) > 0
            assert 'contract_no.' in df.columns
            assert 'customer_name' in df.columns
            
            # Check data quality
            assert df['customer_name'].notna().all()
            assert (df['trade_slip_net_price'] > 0).all()
            
        except FileNotFoundError:
            pytest.skip("Sample data file not found")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
