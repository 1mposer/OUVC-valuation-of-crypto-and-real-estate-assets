"""
60-Second Undervalued Test
Core algorithm for quick cryptocurrency valuation
"""

from typing import Dict


def run_undervalued_test(coin_data: Dict, whitepaper_data: Dict) -> Dict:
    """
    Performs the signature 60-second undervalued test
    
    Args:
        coin_data: Market data from data_fetcher
        whitepaper_data: Manual input data (inflation, value locked)
        
    Returns:
        dict: Analysis results with verdict
    """
    
    price = coin_data["price"]
    circulating = coin_data["circulating"]
    max_supply = coin_data.get("max_supply") or coin_data.get("total_supply")
    
    # Get whitepaper metrics
    new_coins_per_year = whitepaper_data.get("new_coins_per_year", 0)
    value_locked_usd = whitepaper_data.get("value_locked_usd", 0)
    
    # 1. Calculate Inflation Rate
    inflation_rate = (new_coins_per_year / circulating) * 100 if circulating > 0 else 0
    
    # 2. Calculate Fully Diluted Market Cap
    fdmc = price * max_supply if max_supply else None
    
    # 3. Calculate Value Locked Ratio
    value_ratio = fdmc / value_locked_usd if fdmc and value_locked_usd > 0 else None
    
    # 4. Generate Signals
    inflation_signal = get_inflation_signal(inflation_rate)
    valuation_signal = get_valuation_signal(value_ratio) if value_ratio else "insufficient_data"
    
    # 5. Overall Verdict
    verdict = determine_verdict(inflation_signal, valuation_signal)
    
    return {
        "coin_name": coin_data["name"],
        "price": price,
        "circulating_supply": circulating,
        "max_supply": max_supply,
        "inflation_rate": round(inflation_rate, 2),
        "fdmc": fdmc,
        "value_locked": value_locked_usd,
        "value_ratio": round(value_ratio, 2) if value_ratio else None,
        "inflation_signal": inflation_signal,
        "valuation_signal": valuation_signal,
        "overall_verdict": verdict,
        "key_metrics": {
            "price_usd": price,
            "inflation_pct": round(inflation_rate, 2),
            "fdmc_to_value_ratio": round(value_ratio, 2) if value_ratio else "N/A"
        },
        "reasoning": generate_reasoning(inflation_signal, valuation_signal, inflation_rate, value_ratio)
    }


def get_inflation_signal(inflation_rate: float) -> str:
    """Classify inflation rate"""
    if inflation_rate > 10:
        return "high_inflation"  # AVOID
    elif inflation_rate > 3:
        return "medium_inflation"  # CAUTION
    else:
        return "low_inflation"  # GOOD


def get_valuation_signal(value_ratio: float) -> str:
    """Classify valuation based on FDMC/Value Locked ratio"""
    if value_ratio < 3:
        return "undervalued"  # BUY
    elif value_ratio < 10:
        return "fair_value"  # HOLD
    else:
        return "overvalued"  # AVOID


def determine_verdict(inflation_signal: str, valuation_signal: str) -> str:
    """Determine overall investment verdict"""
    
    if inflation_signal == "high_inflation":
        return "AVOID - High Inflation"
    
    if valuation_signal == "insufficient_data":
        return "INSUFFICIENT DATA"
    
    if valuation_signal == "undervalued" and inflation_signal == "low_inflation":
        return "STRONG BUY"
    elif valuation_signal == "undervalued":
        return "BUY"
    elif valuation_signal == "fair_value" and inflation_signal == "low_inflation":
        return "HOLD"
    elif valuation_signal == "overvalued":
        return "AVOID - Overvalued"
    else:
        return "HOLD - Monitor"


def generate_reasoning(inflation_signal: str, valuation_signal: str, inflation_rate: float, value_ratio: float) -> list:
    """Generate human-readable reasoning"""
    reasons = []
    
    # Inflation reasoning
    if inflation_signal == "low_inflation":
        reasons.append(f"Low inflation rate ({inflation_rate:.1f}%) indicates scarcity")
    elif inflation_signal == "medium_inflation":
        reasons.append(f"Moderate inflation rate ({inflation_rate:.1f}%) - acceptable but monitor")
    else:
        reasons.append(f"High inflation rate ({inflation_rate:.1f}%) reduces scarcity value")
    
    # Valuation reasoning
    if valuation_signal == "undervalued" and value_ratio:
        reasons.append(f"FDMC/Value ratio of {value_ratio:.1f}x suggests undervaluation")
    elif valuation_signal == "fair_value" and value_ratio:
        reasons.append(f"FDMC/Value ratio of {value_ratio:.1f}x indicates fair pricing")
    elif valuation_signal == "overvalued" and value_ratio:
        reasons.append(f"FDMC/Value ratio of {value_ratio:.1f}x suggests overvaluation")
    
    return reasons


# Helper function for automated TVL calculation
def get_auto_tvl(coin_name: str, price: float) -> int:
    """
    Automatic TVL estimation for major cryptocurrencies
    """
    coin = coin_name.lower()
    
    # Major TVL estimates (simplified)
    tvl_multipliers = {
        "zcash": 0.8,  # Shielded pool percentage
        "monero": 1.0,  # Full circulating supply
        "ethereum": 0.15,  # Staked + DeFi locked
        "bitcoin": 0.5,  # Long-term holders estimate
        "cardano": 0.7,  # Staked percentage
        "solana": 0.6,  # Staked percentage
    }
    
    multiplier = tvl_multipliers.get(coin, 0.3)  # Default 30%
    
    # Rough estimation - in production, use real APIs
    estimated_coins_locked = 10000000 * multiplier  # Placeholder
    return int(estimated_coins_locked * price)