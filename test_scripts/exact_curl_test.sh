#!/bin/bash

# Test with exact curl from RapidAPI screenshot
# Replace YOUR_ACTUAL_KEY with the full key from RapidAPI

source secure_config/api_keys.env

echo "Testing Bayut API with exact curl from RapidAPI..."
echo ""

curl --request GET \
  --url 'https://bayut.p.rapidapi.com/properties/list?locationExternalIDs=5002%2C6020&purpose=for-rent&hitsPerPage=25&page=0&lang=en&sort=tuned-ranking&categoryExternalID=4&rentFrequency=monthly' \
  --header 'x-rapidapi-host: bayut.p.rapidapi.com' \
  --header "x-rapidapi-key: ${BAYUT_API_KEY}" | python3 -m json.tool

echo ""
echo "Key used: ${BAYUT_API_KEY:0:40}..."
