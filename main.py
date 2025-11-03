#!/usr/bin/env python3
"""
OUVC - Over/Under Value Checker
Main launcher for crypto and property analysis
"""

import sys
import os
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

from shared_utils.secrets_manager import load_secrets, get_secret
from crypto_module.data_fetcher import CryptoDataFetcher, get_coin_id
from crypto_module.undervalued_test import run_undervalued_test
from dubai_property_module.property_analyzer import analyze_dubai_property


def main():
    print("=" * 50)
    print("🚀 OUVC - Over/Under Value Checker")
    print("=" * 50)
    
    # Load API keys
    print("🔐 Loading API keys...")
    api_keys = load_secrets()
    if api_keys:
        print(f"✅ Loaded {len(api_keys)} API keys from secrets")
    else:
        print("⚠️ No API keys loaded - using environment variables or demo mode")
    
    print("=" * 50)
    print("1. 📊 Crypto Analysis")
    print("2. 🏢 Dubai Property Analysis")
    print("3. 🧪 Demo Mode")
    print("=" * 50)
    
    choice = input("Select option (1/2/3): ").strip()
    
    if choice == "1":
        run_crypto_analysis()
    elif choice == "2":
        run_property_analysis()
    elif choice == "3":
        run_demo_mode()
    else:
        print("Invalid choice. Please select 1, 2, or 3.")


def run_crypto_analysis():
    """Run cryptocurrency analysis"""
    print("\n📊 Crypto Analysis")
    print("-" * 30)
    
    crypto_name = input("Enter cryptocurrency name (e.g., bitcoin, zcash): ").strip()
    if not crypto_name:
        print("❌ No cryptocurrency specified")
        return
    
    # Get coin ID
    coin_id = get_coin_id(crypto_name)
    
    try:
        # Fetch market data
        print(f"🔍 Fetching data for {crypto_name}...")
        fetcher = CryptoDataFetcher()
        coin_data = fetcher.get_coin_data(coin_id)
        
        print(f"✅ Data fetched for {coin_data['name']}")
        print(f"   Price: ${coin_data['price']:,.2f}")
        print(f"   Market Cap: ${coin_data['market_cap']:,.0f}")
        
        # Get whitepaper data from user
        print("\n📋 Whitepaper Analysis")
        print("Enter the following metrics:")
        
        try:
            new_coins = float(input("New coins per year (inflation): "))
            value_locked = float(input("Value locked in USD: "))
        except ValueError:
            print("❌ Invalid input. Please enter numbers only.")
            return
        
        whitepaper_data = {
            "new_coins_per_year": new_coins,
            "value_locked_usd": value_locked
        }
        
        # Run analysis
        print("\n🧮 Running 60-second undervalued test...")
        result = run_undervalued_test(coin_data, whitepaper_data)
        
        # Display results
        print_crypto_results(result)
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")


def run_property_analysis():
    """Run Dubai property analysis"""
    print("\n🏢 Dubai Property Analysis")
    print("-" * 30)
    
    # Check API key
    bayut_key = get_secret("BAYUT_API_KEY", "demo_mode")
    if bayut_key == "demo_mode":
        print("⚠️ Running in demo mode - using sample data")
    
    try:
        # Get property details
        area = input("Area (e.g., dubai-marina, downtown-dubai): ").strip()
        property_type = input("Property type (apartment/villa/townhouse): ").strip()
        bedrooms = int(input("Number of bedrooms: "))
        size_sqft = int(input("Size in square feet: "))
        asking_price = float(input("Asking price in AED: "))
        
        print(f"\n🔍 Analyzing property in {area}...")
        
        # Run analysis
        result = analyze_dubai_property(
            area=area,
            property_type=property_type,
            bedrooms=bedrooms,
            size_sqft=size_sqft,
            asking_price_aed=asking_price
        )
        
        if "error" in result:
            print(f"❌ {result['error']}")
            if "suggestion" in result:
                print(f"💡 {result['suggestion']}")
        else:
            print_property_results(result)
            
    except ValueError:
        print("❌ Invalid input. Please enter valid numbers.")
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")


def run_demo_mode():
    """Run demo analysis with pre-configured data"""
    print("\n🧪 Demo Mode")
    print("-" * 30)
    print("1. Crypto Demo (Zcash)")
    print("2. Property Demo (Dubai Marina)")
    
    choice = input("Select demo (1/2): ").strip()
    
    if choice == "1":
        print("\n📊 Demo: Zcash Analysis")
        
        # Demo data for Zcash
        demo_coin_data = {
            "name": "Zcash",
            "symbol": "ZEC",
            "price": 45.0,
            "circulating": 15000000,
            "max_supply": 21000000,
            "market_cap": 675000000,
            "volume_24h": 50000000
        }
        
        demo_whitepaper_data = {
            "new_coins_per_year": 657000,  # ~4.4% inflation
            "value_locked_usd": 1600000000  # Shielded pool value
        }
        
        result = run_undervalued_test(demo_coin_data, demo_whitepaper_data)
        print_crypto_results(result)
        
    elif choice == "2":
        print("\n🏢 Demo: Dubai Marina Property")
        
        result = analyze_dubai_property(
            area="dubai-marina",
            property_type="apartment",
            bedrooms=2,
            size_sqft=1200,
            asking_price_aed=1800000
        )
        
        if "error" not in result:
            print_property_results(result)


def print_crypto_results(result):
    """Print formatted crypto analysis results"""
    print("\n" + "=" * 60)
    print(f"CRYPTO ANALYSIS: {result['coin_name'].upper()}")
    print("=" * 60)
    print(f"Current Price: ${result['price']:,.2f}")
    print(f"Circulating Supply: {result['circulating_supply']:,.0f}")
    print(f"Max Supply: {result['max_supply']:,.0f}" if result['max_supply'] else "No max supply")
    print(f"Inflation Rate: {result['inflation_rate']:.2f}%")
    if result['fdmc']:
        print(f"FDMC: ${result['fdmc']:,.0f}")
    print(f"Value Locked: ${result['value_locked']:,.0f}")
    if result['value_ratio']:
        print(f"FDMC/Value Ratio: {result['value_ratio']:.2f}x")
    
    print("\n" + "-" * 60)
    print(f"VERDICT: {result['overall_verdict']}")
    print("-" * 60)
    
    print("\nKey Reasoning:")
    for reason in result['reasoning']:
        print(f"  • {reason}")
    
    print("=" * 60)


def print_property_results(result):
    """Print formatted property analysis results"""
    print("\n" + "=" * 60)
    print("DUBAI PROPERTY ANALYSIS")
    print("=" * 60)
    print(f"Estimated Value: AED {result['estimated_value']:,.0f}")
    print(f"Confidence Range: AED {result['confidence_interval']['low']:,.0f} - {result['confidence_interval']['high']:,.0f}")
    print(f"Price vs Estimate: {result['price_to_estimate_ratio']:.2f}x")
    print(f"Expected Rental Yield: {result['estimated_rental_yield']:.2f}%")
    print(f"Comparable Properties: {result['comparable_properties']}")
    
    print("\n" + "-" * 60)
    print(f"VERDICT: {result['valuation_signals']['overall_verdict']}")
    print(f"Confidence: {result['valuation_signals']['confidence'].upper()}")
    print("-" * 60)
    
    if result['valuation_signals']['key_factors']:
        print("\nKey Factors:")
        for factor in result['valuation_signals']['key_factors']:
            print(f"  • {factor}")
    
    print("=" * 60)


if __name__ == "__main__":
    main()