#!/bin/bash

# Bayut API Test Script
# This script tests various Bayut API endpoints to understand the data structure

# Load API key from environment
source secure_config/api_keys.env

API_KEY="${BAYUT_API_KEY}"
API_HOST="bayut-api1.p.rapidapi.com"
BASE_URL="https://${API_HOST}"

echo "======================================"
echo "Bayut API Testing Script"
echo "======================================"
echo ""

# Check if jq is installed for pretty JSON output
if ! command -v jq &> /dev/null; then
    echo "⚠️  jq not found. Installing for better JSON formatting..."
    echo "   Run: brew install jq"
    echo ""
    JSON_FORMATTER="cat"
else
    JSON_FORMATTER="jq '.'"
fi

echo "API Key: ${API_KEY:0:20}..."
echo ""

# Test 1: List properties in Dubai Marina (for sale)
echo "======================================"
echo "TEST 1: Property Listings - Dubai Marina (For Sale)"
echo "======================================"
curl -X GET "${BASE_URL}/properties/list?location=dubai-marina&purpose=for-sale&hitsPerPage=3&sort=date-desc" \
  -H "X-RapidAPI-Key: ${API_KEY}" \
  -H "X-RapidAPI-Host: ${API_HOST}" \
  -s | eval $JSON_FORMATTER
echo ""
echo ""

# Test 2: List properties for rent
echo "======================================"
echo "TEST 2: Property Listings - Business Bay (For Rent)"
echo "======================================"
curl -X GET "${BASE_URL}/properties/list?location=business-bay&purpose=for-rent&hitsPerPage=3" \
  -H "X-RapidAPI-Key: ${API_KEY}" \
  -H "X-RapidAPI-Host: ${API_HOST}" \
  -s | eval $JSON_FORMATTER
echo ""
echo ""

# Test 3: Filter by price range
echo "======================================"
echo "TEST 3: Filtered Search - 2BR, 1-2M AED"
echo "======================================"
curl -X GET "${BASE_URL}/properties/list?location=dubai-marina&purpose=for-sale&rooms=2&priceMin=1000000&priceMax=2000000&hitsPerPage=3" \
  -H "X-RapidAPI-Key: ${API_KEY}" \
  -H "X-RapidAPI-Host: ${API_HOST}" \
  -s | eval $JSON_FORMATTER
echo ""
echo ""

# Test 4: Get property details by ID (example ID - replace with actual)
echo "======================================"
echo "TEST 4: Property Details (by ID)"
echo "======================================"
echo "Note: Replace PROPERTY_ID with actual property ID from listings"
# curl -X GET "${BASE_URL}/properties/detail?externalID=PROPERTY_ID" \
#   -H "X-RapidAPI-Key: ${API_KEY}" \
#   -H "X-RapidAPI-Host: ${API_HOST}" \
#   -s | eval $JSON_FORMATTER
echo "Skipped - Requires valid property ID"
echo ""
echo ""

# Test 5: Auto-complete locations
echo "======================================"
echo "TEST 5: Location Auto-Complete"
echo "======================================"
curl -X GET "${BASE_URL}/auto-complete?query=dubai%20marina" \
  -H "X-RapidAPI-Key: ${API_KEY}" \
  -H "X-RapidAPI-Host: ${API_HOST}" \
  -s | eval $JSON_FORMATTER
echo ""
echo ""

# Test 6: Get agencies
echo "======================================"
echo "TEST 6: Agency Listings"
echo "======================================"
curl -X GET "${BASE_URL}/agencies/list?page=0&hitsPerPage=3" \
  -H "X-RapidAPI-Key: ${API_KEY}" \
  -H "X-RapidAPI-Host: ${API_HOST}" \
  -s | eval $JSON_FORMATTER
echo ""
echo ""

echo "======================================"
echo "Testing Complete!"
echo "======================================"
echo ""
echo "Next Steps:"
echo "1. Check if you need to subscribe to the Bayut API on RapidAPI"
echo "2. Verify your API key is active: https://rapidapi.com/apidojo/api/bayut/"
echo "3. Review the response structures above"
echo "4. Update the property_analyzer.py _parse_properties() method if needed"
echo ""
