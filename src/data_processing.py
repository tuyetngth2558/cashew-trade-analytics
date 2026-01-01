"""
Data Processing Module
Chức năng: Clean và chuẩn hóa raw data
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DataCleaner:
    """
    Class để clean và chuẩn hóa dữ liệu hợp đồng
    
    Attributes:
        df (pd.DataFrame): Raw dataframe
    """
    
    def __init__(self, df):
        """Initialize với raw dataframe"""
        self.df = df.copy()
        print(f"📊 Loaded {len(self.df)} rows, {len(self.df.columns)} columns")
    
    def clean_column_names(self):
        """
        Chuẩn hóa tên cột:
        - Chuyển lowercase
        - Thay thế space bằng underscore
        - Loại bỏ ký tự đặc biệt
        """
        print("\n🔧 Cleaning column names...")
        
        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(' ', '_')
            .str.replace('(', '')
            .str.replace(')', '')
            .str.replace('/', '_')
            .str.replace('-', '_')
        )
        
        print(f"✅ Cleaned {len(self.df.columns)} column names")
        return self
    
    def parse_dates(self):
        """
        Chuyển đổi các cột date sang datetime
        Xử lý cả Excel date format (serial numbers)
        """
        print("\n📅 Parsing date columns...")
        
        date_columns = [
            'contract_date', 
            'created_on', 
            'invoiced_on', 
            'fixation_date',
            's.i._date',
            'advice_date'
        ]
        
        for col in date_columns:
            if col in self.df.columns:
                try:
                    # Thử parse multiple formats
                    self.df[col] = pd.to_datetime(
                        self.df[col], 
                        errors='coerce',
                        format='mixed'
                    )
                    
                    # Nếu có giá trị dạng số (Excel serial date)
                    numeric_mask = pd.to_numeric(self.df[col], errors='coerce').notna()
                    if numeric_mask.any():
                        self.df.loc[numeric_mask, col] = pd.to_datetime(
                            self.df.loc[numeric_mask, col].astype(float),
                            origin='1899-12-30',
                            unit='D',
                            errors='coerce'
                        )
                    
                    print(f"   ✓ {col}: {self.df[col].notna().sum()} valid dates")
                    
                except Exception as e:
                    print(f"   ⚠️  {col}: Parsing failed - {str(e)}")
        
        return self
    
    def clean_numeric_columns(self):
        """
        Clean các cột numeric:
        - Remove commas, quotes
        - Convert to float
        """
        print("\n🔢 Cleaning numeric columns...")
        
        numeric_cols = [
            'trade_slip_contract_price',
            'trade_slip_total_cost', 
            'trade_slip_net_price',
            'quantity',
            'weight_mt',
            'anticipated_margin',
            'price',
            'market_price',
            'third_party_invoiced_amount'
        ]
        
        for col in numeric_cols:
            if col in self.df.columns:
                try:
                    # Remove formatting characters
                    self.df[col] = (
                        self.df[col]
                        .astype(str)
                        .str.replace(',', '')
                        .str.replace('"', '')
                        .str.strip()
                    )
                    
                    # Convert to numeric
                    self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                    
                    print(f"   ✓ {col}: {self.df[col].notna().sum()} valid values")
                    
                except Exception as e:
                    print(f"   ⚠️  {col}: Conversion failed - {str(e)}")
        
        return self
    
    def handle_missing_values(self):
        """
        Xử lý missing values:
        - Categorical: Fill 'Unknown'
        - Numeric: Fill 0 hoặc giữ NaN
        """
        print("\n🔍 Handling missing values...")
        
        # Categorical columns
        categorical_cols = [
            'customer_name', 
            'consignee_name',
            'destination_country',
            'origin',
            'sales_terms',
            'commodity'
        ]
        
        for col in categorical_cols:
            if col in self.df.columns:
                missing_count = self.df[col].isna().sum()
                if missing_count > 0:
                    self.df[col] = self.df[col].fillna('Unknown')
                    print(f"   ✓ {col}: Filled {missing_count} missing values")
        
        # Numeric - keep NaN for now (sẽ handle khi train model)
        print(f"\n📊 Remaining missing values:\n{self.df.isnull().sum()[self.df.isnull().sum() > 0]}")
        
        return self
    
    def add_calculated_columns(self):
        """Thêm các cột tính toán"""
        print("\n➕ Adding calculated columns...")
        
        # Margin percentage
        if all(col in self.df.columns for col in ['trade_slip_net_price', 'trade_slip_total_cost', 'trade_slip_contract_price']):
            self.df['margin_percentage'] = (
                (self.df['trade_slip_net_price'] - self.df['trade_slip_total_cost']) / 
                self.df['trade_slip_contract_price'] * 100
            )
            print(f"   ✓ margin_percentage")
        
        # Is invoiced (boolean)
        if 'invoiced' in self.df.columns:
            self.df['is_invoiced'] = (self.df['invoiced'] == 'Yes').astype(int)
            print(f"   ✓ is_invoiced")
        
        return self
    
    def remove_duplicates(self):
        """Remove duplicate contracts"""
        print("\n🗑️  Checking duplicates...")
        
        if 'contract_no' in self.df.columns:
            duplicates = self.df['contract_no'].duplicated().sum()
            if duplicates > 0:
                print(f"   ⚠️  Found {duplicates} duplicate contracts")
                self.df = self.df.drop_duplicates(subset='contract_no', keep='first')
                print(f"   ✓ Removed duplicates, {len(self.df)} rows remaining")
            else:
                print(f"   ✓ No duplicates found")
        
        return self
    
    def get_clean_data(self):
        """Return cleaned dataframe"""
        return self.df
    
    def save_clean_data(self, path='data/processed/contracts_clean.csv'):
        """Save cleaned data to CSV"""
        self.df.to_csv(path, index=False)
        print(f"\n💾 Saved clean data to: {path}")
        print(f"   📊 Final shape: {self.df.shape}")


def main():
    """Main execution function"""
    print("=" * 60)
    print("🚀 DATA CLEANING PIPELINE")
    print("=" * 60)
    
    # Load raw data
    print("\n📂 Loading raw data...")
    try:
        df_raw = pd.read_csv('data/raw/contracts_raw.txt', sep='\t', low_memory=False)
        print(f"✅ Loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        return
    
    # Clean data
    cleaner = DataCleaner(df_raw)
    df_clean = (
        cleaner
        .clean_column_names()
        .parse_dates()
        .clean_numeric_columns()
        .handle_missing_values()
        .add_calculated_columns()
        .remove_duplicates()
        .get_clean_data()
    )
    
    # Save
    cleaner.save_clean_data()
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ DATA CLEANING COMPLETED!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"   - Total rows: {len(df_clean)}")
    print(f"   - Total columns: {len(df_clean.columns)}")
    print(f"   - Date range: {df_clean['contract_date'].min()} to {df_clean['contract_date'].max()}")
    print(f"   - Unique customers: {df_clean['customer_name'].nunique()}")
    print(f"   - Total revenue: ${df_clean['trade_slip_net_price'].sum():,.2f}")


if __name__ == "__main__":
    main()