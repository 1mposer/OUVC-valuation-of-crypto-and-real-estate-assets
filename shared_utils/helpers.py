"""
Common Utility Functions
Shared utilities used across both crypto and property modules
"""

import json
import os
from datetime import datetime, timedelta
import hashlib
from typing import Dict, Any, Optional


def load_json(filepath: str) -> Dict:
    """
    Load JSON data from file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        dict: Loaded JSON data
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def save_json(data: Dict, filepath: str) -> bool:
    """
    Save data to JSON file.
    
    Args:
        data: Data to save
        filepath: Path to save file
        
    Returns:
        bool: Success status
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception:
        return False


def format_number(number: float, precision: int = 2) -> str:
    """
    Format large numbers with appropriate suffixes.
    
    Args:
        number: Number to format
        precision: Decimal precision
        
    Returns:
        str: Formatted number string
    """
    if number >= 1e12:
        return f"{number/1e12:.{precision}f}T"
    elif number >= 1e9:
        return f"{number/1e9:.{precision}f}B"
    elif number >= 1e6:
        return f"{number/1e6:.{precision}f}M"
    elif number >= 1e3:
        return f"{number/1e3:.{precision}f}K"
    else:
        return f"{number:.{precision}f}"


def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Format currency amounts.
    
    Args:
        amount: Amount to format
        currency: Currency code
        
    Returns:
        str: Formatted currency string
    """
    if currency == "AED":
        return f"AED {amount:,.0f}"
    elif currency == "USD":
        return f"${amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"


def is_cache_valid(filepath: str, max_age_minutes: int = 5) -> bool:
    """
    Check if cached file is still valid.
    
    Args:
        filepath: Path to cached file
        max_age_minutes: Maximum age in minutes
        
    Returns:
        bool: True if cache is valid
    """
    if not os.path.exists(filepath):
        return False
    
    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
    age = datetime.now() - file_time
    return age < timedelta(minutes=max_age_minutes)


def generate_cache_key(*args) -> str:
    """
    Generate a cache key from arguments.
    
    Args:
        *args: Arguments to hash
        
    Returns:
        str: Cache key
    """
    key_string = "_".join(str(arg) for arg in args)
    key_string += f"_{datetime.now().strftime('%Y%m%d_%H')}"
    return hashlib.md5(key_string.encode()).hexdigest()


def validate_api_response(response_data: Dict, required_fields: list) -> bool:
    """
    Validate API response contains required fields.
    
    Args:
        response_data: API response data
        required_fields: List of required field names
        
    Returns:
        bool: True if all required fields present
    """
    return all(field in response_data for field in required_fields)


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if division by zero.
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if division by zero
        
    Returns:
        float: Result of division or default
    """
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ZeroDivisionError):
        return default


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp a value between min and max bounds.
    
    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        float: Clamped value
    """
    return max(min_val, min(max_val, value))


def parse_user_input(user_input: str) -> str:
    """
    Parse and normalize user input.
    
    Args:
        user_input: Raw user input
        
    Returns:
        str: Normalized input
    """
    return user_input.lower().strip().replace(" ", "-")


class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, max_requests_per_minute: int = 10):
        self.max_requests = max_requests_per_minute
        self.requests = []
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        import time
        
        now = time.time()
        # Remove requests older than 1 minute
        self.requests = [r for r in self.requests if now - r < 60]
        
        if len(self.requests) >= self.max_requests:
            sleep_time = 60 - (now - self.requests[0]) + 0.1
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.requests.append(now)