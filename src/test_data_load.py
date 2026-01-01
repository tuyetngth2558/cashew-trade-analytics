import pandas as pd

# Load data
df = pd.read_csv('data/raw/contracts_raw.txt', sep='\t')

print(f"✅ Data loaded successfully!")
print(f"📊 Shape: {df.shape}")
print(f"\n📋 Columns:\n{df.columns.tolist()}")
print(f"\n🔍 First 3 rows:\n{df.head(3)}")