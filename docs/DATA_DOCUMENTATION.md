# Cashew Trade Data Documentation

## Overview

This document describes the data schema and structure for the Cashew Trade Analytics platform.

## Data Schema

### Main Contracts Table

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| `contract_no.` | TEXT | Unique contract identifier (format: CTYYYYMMXXXX) |
| `contract_date` | DATE | Date when contract was signed |
| `customer_name` | TEXT | Name of the purchasing customer |
| `consignee_name` | TEXT | Name of the receiving party |
| `destination_country` | TEXT | Final destination country |
| `origin` | TEXT | Country of origin for cashews |
| `commodity` | TEXT | Type of cashew product (e.g., W240, W320, W450) |
| `quantity` | INTEGER | Number of containers |
| `weight_mt` | REAL | Total weight in metric tons |
| `trade_slip_contract_price` | REAL | Contract price per MT (USD) |
| `trade_slip_total_cost` | REAL | Total cost per MT (USD) |
| `trade_slip_net_price` | REAL | Net price for entire contract (USD) |
| `anticipated_margin` | REAL | Expected profit margin (USD) |
| `margin_percentage` | REAL | Margin as percentage of net price |
| `third_party_currency` | TEXT | Currency code (USD, EUR, GBP) |
| `sales_terms` | TEXT | Incoterms (FOB, CIF, CFR, etc.) |
| `payment_terms` | TEXT | Payment conditions (LC, TT, etc.) |
| `is_invoiced` | INTEGER | Whether contract has been invoiced (0/1) |
| `invoiced_on` | DATE | Date of invoice |
| `third_party_invoiced_amount` | REAL | Invoiced amount (USD) |
| `created_on` | DATE | Record creation timestamp |

## Cashew Grades

Common cashew kernel grades in the dataset:

- **W240**: Whole kernels, 220-240 kernels per pound (premium grade)
- **W320**: Whole kernels, 300-320 kernels per pound (most common)
- **W450**: Whole kernels, 400-450 kernels per pound (smaller size)
- **SW**: Scorched Wholes
- **LWP**: Large White Pieces
- **Splits**: Split kernels
- **Pieces**: Broken pieces
- **BB**: Baby Bits (smallest pieces)

## Incoterms

- **FOB** (Free On Board): Seller delivers goods on board vessel
- **CIF** (Cost, Insurance & Freight): Seller pays for shipping and insurance
- **CFR** (Cost & Freight): Seller pays for shipping only
- **EXW** (Ex Works): Buyer handles all shipping
- **FCA** (Free Carrier): Seller delivers to carrier

## Payment Terms

- **LC** (Letter of Credit): Bank-guaranteed payment
  - LC 30/60/90 days: Payment due 30/60/90 days after shipment
- **TT** (Telegraphic Transfer): Direct bank transfer
  - TT Advance: Payment before shipment
  - TT 30 days: Payment 30 days after shipment
- **CAD** (Cash Against Documents): Payment upon document presentation

## Business Logic

### Margin Calculation

```
anticipated_margin = net_price - (weight_mt × total_cost)
margin_percentage = (anticipated_margin / net_price) × 100
```

### Typical Margins

- **Healthy margin**: 10-15%
- **Acceptable margin**: 5-10%
- **Low margin**: <5%
- **Loss**: Negative margin

### Pricing Factors

Contract prices vary based on:
- Cashew grade (W240 > W320 > W450)
- Origin country (quality variations)
- Market conditions
- Order volume
- Payment terms
- Delivery terms

## Sample Data

The sample dataset (`data/sample/sample_data.csv`) contains 200 synthetic records with:
- Date range: 2022-2024
- 15 unique customers
- 7 origin countries
- 15 destination countries
- 8 cashew grades
- ~70% invoiced contracts

## Data Quality Notes

### Required Fields
- `contract_no.`
- `contract_date`
- `customer_name`
- `commodity`
- `weight_mt`
- `trade_slip_contract_price`

### Optional Fields
- Many cost breakdown fields may be empty
- Agent/commission fields often null
- Fixation fields used only for price-to-be-fixed contracts

## Usage Examples

### Load Sample Data

```python
import pandas as pd

# Load sample data
df = pd.read_csv('data/sample/sample_data.csv')

# Convert dates
df['contract_date'] = pd.to_datetime(df['contract_date'])
df['invoiced_on'] = pd.to_datetime(df['invoiced_on'])

# Basic statistics
print(f"Total contracts: {len(df)}")
print(f"Total revenue: ${df['trade_slip_net_price'].sum():,.2f}")
print(f"Average margin: {df['margin_percentage'].mean():.2f}%")
```

### Query by Customer

```python
# Top customers by revenue
top_customers = df.groupby('customer_name').agg({
    'trade_slip_net_price': 'sum',
    'contract_no.': 'count'
}).sort_values('trade_slip_net_price', ascending=False)
```

### Monthly Revenue Trend

```python
# Revenue by month
df['month'] = df['contract_date'].dt.to_period('M')
monthly_revenue = df.groupby('month')['trade_slip_net_price'].sum()
```

## Database Schema

See `src/database.py` for the SQLite schema implementation. The database includes:

1. **contracts**: Main transaction table
2. **customer_summary**: Aggregated customer metrics
3. **monthly_revenue**: Time-series revenue data

## Updates & Maintenance

- Sample data is regenerated using `scripts/generate_sample_data.py`
- Real data should follow the same schema structure
- Additional fields can be added as needed
- Maintain backward compatibility when modifying schema
