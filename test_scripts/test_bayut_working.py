#!/usr/bin/env python3
"""
Working Bayut API Test with simplified parameters
"""

import os
import sys
import json
import requests
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from shared_utils.secrets_manager import load_secrets

def test_bayut_working():
    """Test with working parameters"""
    
    load_secrets()
    api_key = os.getenv("BAYUT_API_KEY")
    
    print("=" * 70)
    print("BAYUT API TEST - WORKING VERSION")
    print("=" * 70)
    print()
    
    base_url = "https://bayut.p.rapidapi.com"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "bayut.p.rapidapi.com"
    }
    
    # Test different parameter combinations
    tests = [
        {
            "name": "Test 1: Simple search - Dubai Marina for rent",
            "params": {
                "locationExternalIDs": "5002",
                "purpose": "for-rent",
                "hitsPerPage": 5,
                "page": 0,
                "lang": "en",
                "rentFrequency": "monthly",
                "categoryExternalID": "4"
            }
        },
        {
            "name": "Test 2: Dubai Marina for sale",
            "params": {
                "locationExternalIDs": "5002",
                "purpose": "for-sale",
                "hitsPerPage": 5,
                "page": 0,
                "lang": "en"
            }
        },
        {
            "name": "Test 3: Price filtered search",
            "params": {
                "locationExternalIDs": "5002",
                "purpose": "for-sale",
                "priceMin": "1000000",
                "priceMax": "2000000",
                "hitsPerPage": 3,
                "page": 0,
                "lang": "en"
            }
        }
    ]
    
    for test in tests:
        print("-" * 70)
        print(test["name"])
        print("-" * 70)
        
        try:
            response = requests.get(
                f"{base_url}/properties/list",
                headers=headers,
                params=test["params"],
                timeout=15
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                hits = data.get('hits', [])
                print(f"✅ Success! Found {len(hits)} properties")
                
                if hits:
                    # Show first property details
                    prop = hits[0]
                    print()
                    print("Sample Property:")
                    print(f"  ID: {prop.get('id')}")
                    print(f"  Price: {prop.get('price', 'N/A')} AED")
                    print(f"  Area: {prop.get('area', 'N/A')} sqft")
                    print(f"  Rooms: {prop.get('rooms', 'N/A')}")
                    print(f"  Baths: {prop.get('baths', 'N/A')}")
                    print(f"  Purpose: {prop.get('purpose', 'N/A')}")
                    
                    # Show available fields
                    print()
                    print(f"  Available fields: {', '.join(list(prop.keys())[:15])}...")
                    
                    # Save full response for first successful test
                    if test == tests[0]:
                        with open('test_scripts/sample_bayut_response.json', 'w') as f:
                            json.dump(data, f, indent=2, default=str)
                        print()
                        print("  📝 Full response saved to: test_scripts/sample_bayut_response.json")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        print()
    
    print("=" * 70)
    print("TESTING COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    test_bayut_working()
