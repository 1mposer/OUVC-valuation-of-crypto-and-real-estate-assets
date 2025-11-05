"""
Test script for DeFiLlama integration
Tests the new TVL fetching functionality
"""

from crypto_module.data_fetcher import CryptoDataFetcher
from crypto_module.undervalued_test import run_undervalued_test


def test_tvl_fetching():
    """Test TVL data fetching"""
    print("=" * 60)
    print("Testing DeFiLlama TVL Integration")
    print("=" * 60)

    fetcher = CryptoDataFetcher()

    # Test protocols with known TVL
    test_cases = [
        ("ethereum", "Ethereum"),
        ("bitcoin", "Bitcoin"),
        ("solana", "Solana"),
        ("aave", "Aave"),
        ("uniswap", "Uniswap"),
    ]

    print("\n1. Testing Direct TVL Fetching:")
    print("-" * 60)
    for protocol, display_name in test_cases:
        tvl = fetcher.get_tvl_data(protocol)
        if tvl:
            print(f"✓ {display_name:15} TVL: ${tvl:,.2f}")
        else:
            print(f"✗ {display_name:15} TVL: Not found")

    print("\n2. Testing Protocol Info:")
    print("-" * 60)
    info = fetcher.get_protocol_info("ethereum")
    if info:
        print(f"✓ Protocol: {info.get('name')}")
        print(f"  Category: {info.get('category')}")
        print(f"  TVL: ${info.get('tvl', 0):,.2f}")
        print(f"  Chains: {', '.join(info.get('chains', [])[:5])}")
    else:
        print("✗ Could not fetch protocol info")

    print("\n3. Testing Full Coin Data with TVL:")
    print("-" * 60)
    try:
        # Use proper CoinGecko coin IDs
        from crypto_module.data_fetcher import get_coin_id
        coin_id = get_coin_id("ethereum")
        coin_data = fetcher.get_coin_data(coin_id)
        print(f"✓ Coin: {coin_data['name']}")
        print(f"  Price: ${coin_data['price']:,.2f}")
        print(f"  Market Cap: ${coin_data['market_cap']:,.2f}")
        print(f"  Value Locked: ${coin_data.get('value_locked', 0):,.2f}")

        # Test with undervalued test
        print("\n4. Testing Undervalued Test with API Data:")
        print("-" * 60)
        result = run_undervalued_test(
            crypto_name="Ethereum",
            coin_data=coin_data
        )
        print(f"✓ Analysis Complete!")
        print(f"  Verdict: {result['verdict']}")
        print(f"  Inflation Rate: {result['inflation_rate']}%")
        print(f"  TVL: ${result['value_locked']:,.2f}")
        if result.get('fdmc_to_value_locked'):
            print(f"  FDMC/TVL Ratio: {result['fdmc_to_value_locked']}x")
        print(f"  Reasoning:")
        for reason in result['reasoning']:
            print(f"    - {reason}")

    except Exception as e:
        print(f"✗ Error: {str(e)}")

    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_tvl_fetching()
