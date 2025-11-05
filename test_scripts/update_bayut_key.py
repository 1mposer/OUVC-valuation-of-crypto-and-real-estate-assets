#!/usr/bin/env python3
"""
Update Bayut API Key
Helps you update the API key in secure_config/api_keys.env
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from shared_utils.secrets_manager import secrets

print("=" * 60)
print("UPDATE BAYUT API KEY")
print("=" * 60)
print()
print("To get your API key:")
print("1. Go to: https://rapidapi.com/apidojo/api/bayut/")
print("2. Click on 'Code Snippets' or 'Endpoints'")
print("3. Look for 'X-RapidAPI-Key' in the code example")
print("4. Copy the key value")
print()
print("=" * 60)
print()

new_key = input("Paste your new Bayut API key here: ").strip()

if new_key and len(new_key) > 20:
    success = secrets.set_api_key("BAYUT_API_KEY", new_key)
    if success:
        print()
        print("✅ API key updated successfully!")
        print(f"   Key: {new_key[:20]}...")
        print()
        print("Now run: python3 test_scripts/test_bayut_api.py")
    else:
        print("❌ Failed to update API key")
else:
    print("❌ Invalid API key. Please try again.")
