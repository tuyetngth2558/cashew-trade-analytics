"""
Generate Sample Cashew Trade Data
Creates synthetic data for demonstration purposes
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_RECORDS = 200
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2024, 12, 31)

# Sample data pools
CUSTOMERS = [
    'Global Trading Co.', 'Asia Pacific Imports', 'Euro Nuts Ltd.',
    'American Cashew Corp.', 'Middle East Trading', 'African Export Group',
    'Pacific Rim Foods', 'Continental Distributors', 'Ocean Trade Partners',
    'Mountain View Imports', 'Sunrise Trading LLC', 'Golden Harvest Co.',
    'Blue Ocean Exports', 'Green Valley Foods', 'Royal Nut Company'
]

CONSIGNEES = [
    'Warehouse Solutions Inc.', 'Port Logistics Ltd.', 'Global Storage Co.',
    'Express Freight Services', 'Maritime Shipping Corp.', 'Air Cargo International',
    'Land Transport Group', 'Coastal Distribution', 'Inland Warehousing',
    'Quick Ship Logistics'
]

COUNTRIES = [
    'United States', 'Germany', 'Netherlands', 'United Kingdom', 'France',
    'Japan', 'South Korea', 'Australia', 'Canada', 'Singapore',
    'UAE', 'Saudi Arabia', 'India', 'China', 'Brazil'
]

ORIGINS = ['Vietnam', 'India', 'Ivory Coast', 'Tanzania', 'Mozambique', 'Ghana', 'Nigeria']

COMMODITIES = [
    'Cashew Kernels W240', 'Cashew Kernels W320', 'Cashew Kernels W450',
    'Cashew Kernels SW', 'Cashew Kernels LWP', 'Cashew Kernels Splits',
    'Cashew Kernels Pieces', 'Cashew Kernels BB'
]

SALES_TERMS = ['FOB', 'CIF', 'CFR', 'EXW', 'FCA']
PAYMENT_TERMS = ['LC 30 days', 'LC 60 days', 'LC 90 days', 'TT Advance', 'TT 30 days', 'CAD']

CURRENCIES = ['USD', 'EUR', 'GBP']

def generate_contract_no(index, date):
    """Generate realistic contract number"""
    year = date.year
    month = date.month
    return f"CT{year}{month:02d}{index:04d}"

def generate_random_date(start, end):
    """Generate random date between start and end"""
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

def generate_sample_data():
    """Generate complete sample dataset"""
    
    data = []
    
    for i in range(NUM_RECORDS):
        # Basic contract info
        contract_date = generate_random_date(START_DATE, END_DATE)
        contract_no = generate_contract_no(i + 1, contract_date)
        
        # Parties
        customer = random.choice(CUSTOMERS)
        consignee = random.choice(CONSIGNEES)
        destination = random.choice(COUNTRIES)
        origin = random.choice(ORIGINS)
        
        # Product
        commodity = random.choice(COMMODITIES)
        
        # Quantity (in containers, typically 15-20 MT per container)
        quantity = random.randint(1, 5)  # 1-5 containers
        weight_mt = round(quantity * random.uniform(15.5, 19.5), 2)
        
        # Pricing (USD per MT)
        base_price = random.uniform(8000, 15000)  # Base price varies by grade
        contract_price = round(base_price, 2)
        
        # Costs
        total_cost = round(contract_price * 0.85, 2)  # Cost is ~85% of price
        net_price = round(weight_mt * contract_price, 2)
        
        # Margin
        anticipated_margin = round(net_price - (weight_mt * total_cost), 2)
        margin_percentage = round((anticipated_margin / net_price) * 100, 2) if net_price > 0 else 0
        
        # Terms
        sales_terms = random.choice(SALES_TERMS)
        payment_terms = random.choice(PAYMENT_TERMS)
        currency = random.choice(CURRENCIES)
        
        # Invoicing (70% are invoiced)
        is_invoiced = 1 if random.random() < 0.7 else 0
        invoiced_on = None
        invoiced_amount = 0
        
        if is_invoiced:
            # Invoice date is 15-60 days after contract
            days_after = random.randint(15, 60)
            invoiced_on = contract_date + timedelta(days=days_after)
            invoiced_amount = round(net_price * random.uniform(0.95, 1.0), 2)  # Slight variation
        
        # Created timestamp
        created_on = contract_date
        
        # Additional fields to match original schema
        sent_to_laserfiche_contract = random.choice([0, 1])
        sent_to_laserfiche_fixation = random.choice([0, 1])
        
        record = {
            'contract_date': contract_date.strftime('%Y-%m-%d'),
            'contract_no.': contract_no,
            'sent_to_laserfiche_contract': sent_to_laserfiche_contract,
            'sent_to_laserfiche_fixation': sent_to_laserfiche_fixation,
            'customer_name': customer,
            'consignee_name': consignee,
            'trade_slip_contract_price': contract_price,
            'trade_slip_total_cost': total_cost,
            'trade_slip_net_price': net_price,
            'country': destination,
            'agent_name': '',
            'vmi': '',
            'amendment': '',
            'commodity': commodity,
            'origin': origin,
            'contract_quality': '',
            'quality_type': '',
            'crop_year': contract_date.year,
            'local_quality_text': '',
            'sales_terms': sales_terms,
            'from': origin,
            'shipped_from_country': origin,
            'final_destination': destination,
            'destination_country': destination,
            'payment_terms': payment_terms,
            'delivery_shipment': 'Prompt',
            'delivery_or_shipment_period': f"{contract_date.strftime('%B %Y')}",
            'quantity': quantity,
            'quantity_unit': 'Containers',
            'weight_mt': weight_mt,
            'net_weight_in_lots__in_mt_': weight_mt,
            'gross_weight_in_lots__in_mt_': round(weight_mt * 1.02, 2),
            'unapplied_weight_mt': 0,
            'uninvoiced_weight_mt': 0 if is_invoiced else weight_mt,
            'washout_weight_in_mt': 0,
            'uninvoiced_quantity': 0 if is_invoiced else quantity,
            'l_c_numbers': '',
            '+__': '',
            'price': contract_price,
            'price_unit': 'USD/MT',
            'price_method': 'Fixed',
            'cover_month': '',
            'cover_year': '',
            'average_price': contract_price,
            'market_price': round(contract_price * random.uniform(0.95, 1.05), 2),
            'market_price_unit': 'USD/MT',
            'hypothetical_exchange': '',
            'hypothetical_cover_month': '',
            'hypothetical_cover_year': '',
            'hypothetical_on_off_ratio': '',
            'hypothetical_differential_ratio': '',
            'hypothetical_differential_price_unit': '',
            'sas_approved': random.choice([0, 1]),
            'posting_dates': '',
            'on_call_balance': 0,
            'total_weight_fixed': weight_mt if is_invoiced else 0,
            'number_of_lot_to_be_fixed': 0,
            'number_of_lot_fixed': quantity if is_invoiced else 0,
            'trade_slip_price': contract_price,
            'market_price2': '',
            'selling_commission': round(net_price * 0.01, 2),
            'buying_commission': round(net_price * 0.005, 2),
            'fob_nett': round(net_price * 0.98, 2),
            'anticipated_margin': anticipated_margin,
            'anticipated_purchase_price': total_cost,
            'costs_to_fob_new_trade_slip': round(total_cost * 0.1, 2),
            'freight_new_trade_slip': round(weight_mt * 50, 2),
            'insurance_new_trade_slip': round(net_price * 0.002, 2),
            'other_costs_new_trade_slip': round(net_price * 0.005, 2),
            'controlling_costs_new_trade_slip': 0,
            'bank_charges_costs_new_trade_slip': round(net_price * 0.001, 2),
            'weight_loss_costs_new_trade_slip': 0,
            'interest_costs_new_trade_slip': 0,
            'cost_hedge_costs_new_trade_slip': 0,
            'custom_charge_costs_new_trade_slip': 0,
            'custom_duties_costs_new_trade_slip': 0,
            'customer': customer,
            'commission_price_unit': 'USD/MT',
            'commission_on_amount_rate__%_': 1.0,
            'commission_on_quantity_sign': '',
            'commission_on_quantity_rate': 0,
            'commission_on_weight_sign': '',
            'commission_on_weight_rate': 0,
            'commission_on_price_unit_sign': '',
            'commission_on_price_unit_rate': 0,
            'agent_commission_price_unit': '',
            'agent_on_amount_rate__%_': 0,
            'agent_on_weight_sign': '',
            'agent_on_price_unit_rate': 0,
            'periods__begin_': contract_date.strftime('%Y-%m-%d'),
            'periods__end_': (contract_date + timedelta(days=30)).strftime('%Y-%m-%d'),
            'price__exchange_': '',
            'exchange_price_unit': '',
            's.i._no.': '',
            's.i._date': '',
            'advice_no.': '',
            'advice_date': '',
            'fixation_date': '',
            'created_on': created_on.strftime('%Y-%m-%d'),
            'created_by': 'System',
            'invoiced': is_invoiced,
            'invoiced_on': invoiced_on.strftime('%Y-%m-%d') if invoiced_on else '',
            'third_party_invoiced_amount': invoiced_amount,
            'third_party_currency': currency,
            'margin_percentage': margin_percentage,
            'is_invoiced': is_invoiced
        }
        
        data.append(record)
    
    return pd.DataFrame(data)

def main():
    """Main execution"""
    print("=" * 60)
    print("🌰 GENERATING SAMPLE CASHEW TRADE DATA")
    print("=" * 60)
    
    print(f"\n📊 Generating {NUM_RECORDS} sample records...")
    df = generate_sample_data()
    
    # Save to CSV
    output_path = 'data/sample/sample_data.csv'
    df.to_csv(output_path, index=False)
    print(f"✅ Saved to: {output_path}")
    
    # Display summary
    print("\n" + "=" * 60)
    print("📈 SUMMARY STATISTICS")
    print("=" * 60)
    print(f"Total Records: {len(df)}")
    print(f"Date Range: {df['contract_date'].min()} to {df['contract_date'].max()}")
    print(f"Total Customers: {df['customer_name'].nunique()}")
    print(f"Total Revenue: ${df['trade_slip_net_price'].sum():,.2f}")
    print(f"Average Margin: {df['margin_percentage'].mean():.2f}%")
    print(f"Invoiced Contracts: {df['is_invoiced'].sum()} ({df['is_invoiced'].mean()*100:.1f}%)")
    
    print("\n" + "=" * 60)
    print("✅ SAMPLE DATA GENERATION COMPLETED!")
    print("=" * 60)

if __name__ == "__main__":
    main()
