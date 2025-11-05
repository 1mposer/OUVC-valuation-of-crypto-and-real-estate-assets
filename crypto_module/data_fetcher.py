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
        self.defillama_base = "https://pro-api.llama.fi"
        self.headers = {"Content-Type": "application/json"}

        # Load CoinGecko API key if available
        self.coingecko_api_key = os.getenv("COINGECKO_API_KEY")
        if self.coingecko_api_key:
            # CoinGecko uses x-cg-demo-api-key header for free tier
            # and x-cg-pro-api-key for pro tier
            self.headers["x-cg-demo-api-key"] = self.coingecko_api_key
    
    def get_coin_data(self, coin_id: str) -> Dict:
        """
        Pulls price, supply, volume from CoinGecko and TVL from DeFiLlama

        Args:
            coin_id: 'zcash', 'bitcoin', 'ethereum', etc. (case-insensitive)

        Returns:
            dict: Market data for the cryptocurrency including TVL
        """
        # Normalize the coin_id to match CoinGecko's expected format
        normalized_coin_id = get_coin_id(coin_id)
        url = f"{self.coingecko_base}/coins/{normalized_coin_id}"

        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            if resp.status_code == 403:
                raise ValueError(
                    f"CoinGecko API access denied. "
                    f"Please set up your COINGECKO_API_KEY in secure_config/api_keys.env. "
                    f"Get a free API key at: https://www.coingecko.com/en/api"
                )
            elif resp.status_code == 404:
                raise ValueError(f"Coin '{normalized_coin_id}' not found!")
            elif resp.status_code != 200:
                raise ValueError(
                    f"CoinGecko API error (status {resp.status_code}): {resp.text[:200]}"
                )

            data = resp.json()
            coin_data = {
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

            # Try to fetch TVL data from DeFiLlama
            tvl = self.get_tvl_data(coin_id)
            if tvl:
                coin_data["value_locked"] = tvl
            else:
                # If no TVL found, estimate based on market cap for certain coins
                coin_data["value_locked"] = self._estimate_tvl(coin_data)

            return coin_data

        except Exception as e:
            raise Exception(f"Failed to fetch data for {normalized_coin_id}: {str(e)}")

    def _estimate_tvl(self, coin_data: Dict) -> float:
        """
        Estimate TVL for coins without direct DeFi protocols
        Uses conservative multipliers based on typical lock-up rates

        Args:
            coin_data: Coin market data

        Returns:
            float: Estimated TVL in USD
        """
        name = coin_data.get("name", "").lower()
        symbol = coin_data.get("symbol", "").upper()
        market_cap = coin_data.get("market_cap", 0)

        # TVL estimation multipliers (% of market cap typically locked)
        tvl_multipliers = {
            # Privacy coins - based on shielded pool usage
            'zcash': 0.05,  # ~5% in shielded pools
            'monero': 0.80,  # Most XMR is private by default

            # Smart contract platforms with staking
            'ethereum': 0.25,  # Staked + DeFi locked
            'cardano': 0.65,  # High staking rate
            'solana': 0.70,   # High staking rate
            'polkadot': 0.55, # High staking rate
            'avalanche': 0.60,
            'algorand': 0.65,
            'tezos': 0.70,
            'cosmos': 0.65,
            'near': 0.60,
            'fantom': 0.50,
            'harmony': 0.45,
            'elrond': 0.60,
            'zilliqa': 0.50,

            # Layer 2s (use parent chain TVL)
            'polygon': 0.30,
            'arbitrum': 0.20,
            'optimism': 0.20,

            # Bitcoin - conservative (long-term holders)
            'bitcoin': 0.50,

            # Oracles & infrastructure
            'chainlink': 0.40,
            'theta': 0.45,
            'vechain': 0.35,
            'hedera': 0.40,
        }

        # Try to match by name or symbol
        for key, multiplier in tvl_multipliers.items():
            if key in name or key == symbol.lower():
                return market_cap * multiplier

        # Default: 10% for unknown coins
        return market_cap * 0.10

    def get_tvl_data(self, protocol_name: str) -> Optional[float]:
        """
        Fetches Total Value Locked (TVL) data from DeFiLlama API

        Args:
            protocol_name: Protocol name (e.g., 'aave', 'uniswap', 'compound')

        Returns:
            float: TVL in USD, or None if not found
        """
        try:
            # First, try to get the protocol slug
            protocol_slug = self._get_protocol_slug(protocol_name)

            if not protocol_slug:
                return None

            # Get TVL from DeFiLlama
            url = f"{self.defillama_base}/api/tvl/{protocol_slug}"
            resp = requests.get(url, timeout=10)

            if resp.status_code == 200:
                # Response is just a number
                tvl = float(resp.text)
                return tvl
            else:
                return None

        except Exception:
            return None

    def get_protocol_info(self, protocol_name: str) -> Optional[Dict]:
        """
        Fetches detailed protocol information from DeFiLlama

        Args:
            protocol_name: Protocol name

        Returns:
            dict: Protocol data including TVL, category, chains, etc.
        """
        try:
            protocol_slug = self._get_protocol_slug(protocol_name)

            if not protocol_slug:
                return None

            url = f"{self.defillama_base}/api/protocol/{protocol_slug}"
            resp = requests.get(url, timeout=10)

            if resp.status_code == 200:
                data = resp.json()
                return {
                    'name': data.get('name'),
                    'symbol': data.get('symbol'),
                    'tvl': data.get('tvl'),
                    'category': data.get('category'),
                    'chains': data.get('chains', []),
                    'mcap': data.get('mcap'),
                    'description': data.get('description'),
                    'url': data.get('url')
                }
            else:
                return None

        except Exception:
            return None

    def _get_protocol_slug(self, protocol_name: str) -> Optional[str]:
        """
        Convert user-friendly protocol name to DeFiLlama slug

        Args:
            protocol_name: User input protocol name

        Returns:
            str: DeFiLlama protocol slug, or None if not found
        """
        # Mapping of common crypto names to their DeFi protocol slugs
        protocol_map = {
            # Layer 1s with DeFi ecosystems
            'ethereum': 'ethereum',
            'eth': 'ethereum',
            'bitcoin': 'bitcoin',
            'btc': 'bitcoin',
            'solana': 'solana',
            'sol': 'solana',
            'cardano': 'cardano',
            'ada': 'cardano',
            'avalanche': 'avalanche',
            'avax': 'avalanche',
            'polkadot': 'polkadot',
            'dot': 'polkadot',
            'polygon': 'polygon',
            'matic': 'polygon',
            'cosmos': 'cosmos',
            'atom': 'cosmos',
            'algorand': 'algorand',
            'algo': 'algorand',
            'tezos': 'tezos',
            'xtz': 'tezos',
            'near protocol': 'near',
            'near': 'near',
            'fantom': 'fantom',
            'ftm': 'fantom',
            'harmony': 'harmony',
            'one': 'harmony',
            'elrond': 'multiversx',
            'egld': 'multiversx',
            'multiversx': 'multiversx',
            'zilliqa': 'zilliqa',
            'zil': 'zilliqa',

            # Major DeFi Protocols
            'aave': 'aave',
            'uniswap': 'uniswap',
            'compound': 'compound',
            'makerdao': 'makerdao',
            'maker': 'makerdao',
            'curve': 'curve',
            'lido': 'lido',
            'pancakeswap': 'pancakeswap',
            'sushiswap': 'sushi',
            'balancer': 'balancer',
            'yearn': 'yearn-finance',
            'synthetix': 'synthetix',
            'convex': 'convex-finance',
            'rocket pool': 'rocket-pool',
            'frax': 'frax',

            # Layer 2s
            'arbitrum': 'arbitrum',
            'optimism': 'optimism',
            'base': 'base',

            # Privacy coins (note: these may not have TVL)
            'zcash': 'zcash',
            'zec': 'zcash',
            'monero': 'monero',
            'xmr': 'monero',

            # Oracles
            'chainlink': 'chainlink',
            'link': 'chainlink',

            # Other popular protocols
            'gmx': 'gmx',
            'thorchain': 'thorchain',
            'osmosis': 'osmosis',
            'jito': 'jito',
            'kamino': 'kamino',
        }

        normalized = protocol_name.lower().strip()
        return protocol_map.get(normalized, normalized)


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