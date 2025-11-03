"""
Crypto Data Fetcher Module
Handles API connections and data retrieval for cryptocurrency analysis
"""

import requests
from typing import Dict, Optional
import os


class CryptoDataFetcher:
    """Fetches cryptocurrency data from various APIs"""
    
    def __init__(self):
        self.coingecko_base = "https://api.coingecko.com/api/v3"
        self.headers = {"Content-Type": "application/json"}
    
    def get_coin_data(self, coin_id: str) -> Dict:
        """
        Pulls price, supply, volume from CoinGecko
        
        Args:
            coin_id: 'zcash', 'bitcoin', 'ethereum', etc.
            
        Returns:
            dict: Market data for the cryptocurrency
        """
        url = f"{self.coingecko_base}/coins/{coin_id}"
        
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            if resp.status_code != 200:
                raise ValueError(f"Coin '{coin_id}' not found!")
            
            data = resp.json()
            return {
                "name": data["name"],
                "symbol": data["symbol"].upper(),
                "price": data["market_data"]["current_price"]["usd"],
                "circulating": data["market_data"]["circulating_supply"],
                "max_supply": data["market_data"].get("max_supply"),
                "total_supply": data["market_data"]["total_supply"],
                "volume_24h": data["market_data"]["total_volume"]["usd"],
                "market_cap": data["market_data"]["market_cap"]["usd"],
                "price_change_24h": data["market_data"]["price_change_percentage_24h"],
                "last_updated": data["last_updated"]
            }
        except Exception as e:
            raise Exception(f"Failed to fetch data for {coin_id}: {str(e)}")


# Coin mapping for user-friendly input
COIN_MAP = {
    # Bitcoin & Forks
    "btc": "bitcoin", "bitcoin": "bitcoin",
    "bch": "bitcoin-cash", "bitcoincash": "bitcoin-cash",
    
    # Ethereum & L2s
    "eth": "ethereum", "ethereum": "ethereum",
    "matic": "polygon", "polygon": "polygon",
    
    # Major Altcoins
    "ada": "cardano", "cardano": "cardano",
    "sol": "solana", "solana": "solana",
    "dot": "polkadot", "polkadot": "polkadot",
    
    # Privacy Coins
    "zec": "zcash", "zcash": "zcash",
    "xmr": "monero", "monero": "monero",
    
    # Stablecoins
    "usdt": "tether", "tether": "tether",
    "usdc": "usd-coin", "usdcoin": "usd-coin",
    
    # Exchange Tokens
    "bnb": "binancecoin", "binancecoin": "binancecoin",
    
    # DeFi
    "uni": "uniswap", "uniswap": "uniswap",
    "aave": "aave", "aave": "aave",
    
    # Meme Coins
    "doge": "dogecoin", "dogecoin": "dogecoin",
    "shib": "shiba-inu", "shibainu": "shiba-inu",
    
    # Payments
    "xrp": "ripple", "ripple": "ripple",
    "ltc": "litecoin", "litecoin": "litecoin",
}


def get_coin_id(user_input: str) -> str:
    """Convert user input to CoinGecko ID"""
    normalized = user_input.lower().strip()
    return COIN_MAP.get(normalized, normalized)