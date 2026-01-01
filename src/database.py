"""
Database Module
Chức năng: Quản lý SQLite database
"""

import sqlite3
import pandas as pd
from sqlalchemy import create_engine
import os

class Database:
    """
    SQLite database manager
    
    Attributes:
        db_path (str): Path to database file
        engine: SQLAlchemy engine
    """
    
    def __init__(self, db_path='data/database/contracts.db'):
        """Initialize database connection"""
        self.db_path = db_path
        
        # Create directory if not exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.engine = create_engine(f'sqlite:///{db_path}')
        print(f"📚 Database initialized: {db_path}")
    
    def create_tables(self):
        """Tạo database schema"""
        print("\n🔨 Creating tables...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main contracts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contracts (
                contract_no TEXT PRIMARY KEY,
                contract_date DATE,
                customer_name TEXT,
                consignee_name TEXT,
                destination_country TEXT,
                origin TEXT,
                commodity TEXT,
                quantity REAL,
                weight_mt REAL,
                contract_price REAL,
                total_cost REAL,
                net_price REAL,
                anticipated_margin REAL,
                margin_percentage REAL,
                currency TEXT,
                sales_terms TEXT,
                payment_terms TEXT,
                invoiced INTEGER,
                invoiced_on DATE,
                invoiced_amount REAL,
                created_on DATE
            )
        ''')
        print("   ✓ Table 'contracts' created")
        
        # Customer summary table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer_summary (
                customer_name TEXT PRIMARY KEY,
                total_contracts INTEGER,
                total_revenue REAL,
                avg_margin REAL,
                first_order_date DATE,
                last_order_date DATE
            )
        ''')
        print("   ✓ Table 'customer_summary' created")
        
        # Monthly revenue table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_revenue (
                month DATE,
                total_revenue REAL,
                total_contracts INTEGER,
                avg_contract_value REAL,
                PRIMARY KEY (month)
            )
        ''')
        print("   ✓ Table 'monthly_revenue' created")
        
        conn.commit()
        conn.close()
        
        print("✅ All tables created successfully!")
    
    def load_data(self, df, table_name='contracts'):
        """
        Load DataFrame vào database
        
        Args:
            df (pd.DataFrame): Data to load
            table_name (str): Target table name
        """
        print(f"\n📥 Loading data into '{table_name}'...")
        
        # Select relevant columns
        if table_name == 'contracts':
            columns = [
                'contract_no.', 'contract_date', 'customer_name', 'consignee_name',
                'destination_country', 'origin', 'commodity', 'quantity', 'weight_mt',
                'trade_slip_contract_price', 'trade_slip_total_cost', 'trade_slip_net_price',
                'anticipated_margin', 'margin_percentage', 'third_party_currency', 'sales_terms',
                'payment_terms', 'is_invoiced', 'invoiced_on', 'third_party_invoiced_amount',
                'created_on'
            ]
            
            # Rename to match table schema
            df_load = df[columns].copy()
            df_load.columns = [
                'contract_no', 'contract_date', 'customer_name', 'consignee_name',
                'destination_country', 'origin', 'commodity', 'quantity', 'weight_mt',
                'contract_price', 'total_cost', 'net_price', 'anticipated_margin',
                'margin_percentage', 'currency', 'sales_terms', 'payment_terms',
                'invoiced', 'invoiced_on', 'invoiced_amount', 'created_on'
            ]
        else:
            df_load = df
        
        # Load to database
        df_load.to_sql(table_name, self.engine, if_exists='replace', index=False)
        
        print(f"✅ Loaded {len(df_load)} rows into '{table_name}'")
    
    def create_aggregated_tables(self):
        """Tạo aggregated tables cho faster queries"""
        print("\n📊 Creating aggregated tables...")
        
        # Customer summary
        query_customer = """
        INSERT OR REPLACE INTO customer_summary
        SELECT 
            customer_name,
            COUNT(*) as total_contracts,
            SUM(net_price) as total_revenue,
            AVG(margin_percentage) as avg_margin,
            MIN(contract_date) as first_order_date,
            MAX(contract_date) as last_order_date
        FROM contracts
        GROUP BY customer_name
        """
        
        conn = sqlite3.connect(self.db_path)
        conn.execute(query_customer)
        print("   ✓ customer_summary updated")
        
        # Monthly revenue
        query_monthly = """
        INSERT OR REPLACE INTO monthly_revenue
        SELECT 
            DATE(contract_date, 'start of month') as month,
            SUM(net_price) as total_revenue,
            COUNT(*) as total_contracts,
            AVG(net_price) as avg_contract_value
        FROM contracts
        GROUP BY DATE(contract_date, 'start of month')
        """
        
        conn.execute(query_monthly)
        print("   ✓ monthly_revenue updated")
        
        conn.commit()
        conn.close()
        
        print("✅ Aggregated tables created!")
    
    def query(self, sql):
        """
        Execute SQL query và return DataFrame
        
        Args:
            sql (str): SQL query
            
        Returns:
            pd.DataFrame: Query results
        """
        return pd.read_sql(sql, self.engine)
    
    def get_summary(self):
        """Get database summary"""
        print("\n" + "=" * 60)
        print("📊 DATABASE SUMMARY")
        print("=" * 60)
        
        # Table counts
        tables = ['contracts', 'customer_summary', 'monthly_revenue']
        for table in tables:
            count = self.query(f"SELECT COUNT(*) as cnt FROM {table}")['cnt'].iloc[0]
            print(f"   - {table}: {count:,} rows")
        
        # Date range
        date_range = self.query("""
            SELECT 
                MIN(contract_date) as first_date,
                MAX(contract_date) as last_date
            FROM contracts
        """)
        print(f"\n📅 Date range: {date_range['first_date'].iloc[0]} to {date_range['last_date'].iloc[0]}")
        
        # Top customers
        top_customers = self.query("""
            SELECT customer_name, total_revenue
            FROM customer_summary
            ORDER BY total_revenue DESC
            LIMIT 5
        """)
        print(f"\n🏆 Top 5 customers:")
        for _, row in top_customers.iterrows():
            print(f"   - {row['customer_name']}: ${row['total_revenue']:,.2f}")


def main():
    """Main execution function"""
    print("=" * 60)
    print("🗄️  DATABASE SETUP")
    print("=" * 60)
    
    # Initialize database
    db = Database()
    
    # Create tables
    db.create_tables()
    
    # Load clean data
    print("\n📂 Loading clean data...")
    try:
        df = pd.read_csv('data/processed/contracts_clean.csv')
        print(f"✅ Loaded {len(df)} rows")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return
    
    # Load to database
    db.load_data(df, 'contracts')
    
    # Create aggregated tables
    db.create_aggregated_tables()
    
    # Show summary
    db.get_summary()
    
    print("\n" + "=" * 60)
    print("✅ DATABASE SETUP COMPLETED!")
    print("=" * 60)


if __name__ == "__main__":
    main()