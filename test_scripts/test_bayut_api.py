#!/usr/bin/env python3
"""
Simple Bayut API Test Script
Tests the Bayut API and displays the JSON response structure
"""

import os
import sys
import json
import requests
from pathlib import Path

# Add parent directory to path to import shared utils
sys.path.append(str(Path(__file__).parent.parent))
from shared_utils.secrets_manager import load_secrets

def test_bayut_api():
    """Test Bayut API and show response structure"""
    
    # Load API key
    load_secrets()
    api_key = os.getenv("BAYUT_API_KEY")
    
    if not api_key or api_key == "demo_mode":
        print("❌ Error: BAYUT_API_KEY not found in environment")
        print("Please check secure_config/api_keys.env")
        return
    
    print("=" * 60)
    print("BAYUT API TEST")
    print("=" * 60)
    print(f"API Key: {api_key[:20]}...")
    print()
    
    # API configuration
    base_url = "https://bayut-api1.p.rapidapi.com"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "bayut-api1.p.rapidapi.com"
    }
    
    # Test 1: Search properties in Dubai Marina - Using exact parameters from RapidAPI
    print("TEST 1: Property Listings - Dubai Marina (For Rent)")
    print("-" * 60)
    
    params = {
        "locationExternalIDs": "5002,6020",
        "purpose": "for-rent",
        "hitsPerPage": 25,
        "page": 0,
        "lang": "en",
        "sort": "tuned-ranking",
        "categoryExternalID": "4",
        "rentFrequency": "monthly"
    }
    
    try:
        response = requests.get(
            f"{base_url}/properties/list",
            headers=headers,
            params=params,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print()
        
        if response.status_code == 200:
            data = response.json()
            
            # Display summary
            print(f"✅ Success! Found {len(data.get('hits', []))} properties")
            print()
            
            # Display structure
            print("Response Structure:")
            print(json.dumps(data, indent=2, default=str)[:2000])  # First 2000 chars
            print("\n... (truncated)")
            print()
            
            # Display key fields from first property
            if data.get('hits') and len(data['hits']) > 0:
                prop = data['hits'][0]
                print("=" * 60)
                print("SAMPLE PROPERTY DATA:")
                print("=" * 60)
                print(f"ID: {prop.get('id', 'N/A')}")
                print(f"Price: {prop.get('price', 'N/A')} AED")
                print(f"Area: {prop.get('area', 'N/A')} sqft")
                print(f"Rooms: {prop.get('rooms', 'N/A')}")
                print(f"Baths: {prop.get('baths', 'N/A')}")
                print(f"Type: {prop.get('category', [{}])[0].get('name', 'N/A') if prop.get('category') else 'N/A'}")
                print(f"Location: {prop.get('location', [{}])[0].get('name', 'N/A') if prop.get('location') else 'N/A'}")
                print(f"Title: {prop.get('title', 'N/A')}")
                print()
                
                # Show all available fields
                print("Available Fields in Response:")
                print(", ".join(prop.keys()))
                print()
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
            if "not subscribed" in response.text.lower():
                print("\n⚠️  You need to subscribe to the Bayut API:")
                print("   https://rapidapi.com/apidojo/api/bayut/pricing")
            elif "too many requests" in response.text.lower():
                print("\n⚠️  Rate limit exceeded. Wait a moment and try again.")
    
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The API might be slow or unavailable.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print()
    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    test_bayut_api()
