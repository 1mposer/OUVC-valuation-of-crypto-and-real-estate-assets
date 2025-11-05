#!/bin/bash

# Simple Bayut API Test
source secure_config/api_keys.env

echo "Testing Bayut API..."
echo "API Key: ${BAYUT_API_KEY:0:20}..."
echo ""

curl -X GET "https://bayut-api1.p.rapidapi.com/properties/list?location=dubai-marina&purpose=for-sale&hitsPerPage=2" \
  -H "X-RapidAPI-Key: ${BAYUT_API_KEY}" \
  -H "X-RapidAPI-Host: bayut-api1.p.rapidapi.com" \
  -w "\n\nHTTP Status: %{http_code}\n" \
  -s | python3 -m json.tool 2>/dev/null || cat

echo ""
echo "If you see 'You are not subscribed', visit:"
echo "https://rapidapi.com/apidojo/api/bayut/pricing"
