#!/usr/bin/env python3
"""
Bayut API Diagnostic Script
Helps diagnose subscription issues
"""

import os
import sys
import requests
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from shared_utils.secrets_manager import load_secrets

def diagnose():
    load_secrets()
    api_key = os.getenv("BAYUT_API_KEY")
    
    print("=" * 60)
    print("BAYUT API DIAGNOSTIC")
    print("=" * 60)
    print()
    print(f"API Key (first 30 chars): {api_key[:30]}...")
    print(f"API Key length: {len(api_key)}")
    print()
    
    # Try a simple endpoint with detailed headers
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "bayut-api1.p.rapidapi.com"
    }
    
    print("Testing connection...")
    print()
    
    try:
        # Try the auto-complete endpoint (usually simpler)
        response = requests.get(
            "https://bayut-api1.p.rapidapi.com/auto-complete",
            headers=headers,
            params={"query": "marina"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        print()
        
        if response.status_code == 403:
            print("❌ 403 Forbidden - Subscription Issue")
            print()
            print("Possible causes:")
            print("1. API key is from before you subscribed")
            print("2. Subscription hasn't fully activated yet (wait 5-10 min)")
            print("3. You're using a key from a different RapidAPI account")
            print()
            print("Solutions:")
            print("1. Go to: https://rapidapi.com/apidojo/api/bayut/")
            print("2. Make sure you're logged in")
            print("3. Click 'Subscribe to Test' if you see it")
            print("4. Copy the key from the code snippet on the right")
            print("5. Run: python3 test_scripts/update_bayut_key.py")
            
        elif response.status_code == 200:
            print("✅ Success! API is working")
            
        elif response.status_code == 429:
            print("⚠️  Rate limit - but subscription is working!")
            
        else:
            print(f"Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    diagnose()
