# BAYUT API - COMPREHENSIVE DATA STRUCTURE DOCUMENTATION
## For Algorithm Development with Claude Opus

---

## OVERVIEW

The Bayut API returns property listings for Dubai real estate. The response contains detailed information about properties including pricing, location, features, amenities, agent details, photos, and market metrics.

---

## TOP-LEVEL RESPONSE STRUCTURE

```json
{
  "hits": [],           // Array of property objects (main data)
  "nbHits": 8381,       // Total number of results found
  "page": 0,            // Current page number
  "nbPages": 1677,      // Total pages available
  "hitsPerPage": 5,     // Results per page
  "query": "",          // Search query used
  "params": "...",      // Full query parameters
  "processingTimeMS": 5 // API processing time
}
```

**Algorithm Use Cases:**
- **Pagination**: Use `nbHits`, `page`, `nbPages` to implement bulk data collection
- **Performance Monitoring**: Track `processingTimeMS` for API health
- **Data Volume**: Calculate total available properties for market analysis

---

## PROPERTY OBJECT STRUCTURE (hits[])

### **CORE IDENTIFIERS**

| Field | Type | Description | Algorithm Use |
|-------|------|-------------|---------------|
| `id` | integer | Unique property ID | Primary key for tracking, deduplication |
| `externalID` | string | External reference number | Cross-referencing with other systems |
| `referenceNumber` | string | Agent's reference code | Agent performance tracking |
| `ownerID` | integer | Property owner/agent ID | Agent relationship mapping |
| `slug` | string | URL-friendly property identifier | Web scraping, link generation |
| `objectID` | string | Algolia search ID | Search optimization |

---

### **PRICING & FINANCIAL DATA**

| Field | Type | Description | Algorithm Use |
|-------|------|-------------|---------------|
| `price` | float | Listing price in AED | **CRITICAL for valuation algorithms** |
| `rentFrequency` | string | "monthly", "yearly", "weekly" | Rental yield calculations |
| `purpose` | string | "for-rent" or "for-sale" | Market segmentation |
| `hidePrice` | boolean | Whether price is hidden | Filter for data quality |

**Example Values:**
```json
{
  "price": 15999.0,
  "rentFrequency": "monthly",
  "purpose": "for-rent"
}
```

**Valuation Algorithm Inputs:**
- Calculate annual rent: `price * 12` (if monthly)
- Compare similar properties by `purpose` and `price` range
- Estimate rental yield: `(annual_rent / sale_price) * 100`

---

### **PROPERTY SPECIFICATIONS**

| Field | Type | Description | Algorithm Use |
|-------|------|-------------|---------------|
| `rooms` | integer | Number of bedrooms (0 = studio) | Comp selection, valuation |
| `baths` | integer | Number of bathrooms | Feature matching |
| `area` | float | Size in square feet | **CRITICAL: Price per sqft calculation** |
| `plotArea` | float/null | Land area (for villas) | Land value analysis |
| `furnishingStatus` | string | "furnished", "unfurnished", "semi-furnished" | Premium pricing factor |

**Example:**
```json
{
  "rooms": 2,
  "baths": 2,
  "area": 75.06565632,
  "furnishingStatus": "furnished"
}
```

**Key Calculations:**
```python
price_per_sqft = price / area
bedroom_to_bath_ratio = rooms / baths
avg_room_size = area / (rooms + 1)  # +1 for living area
```

---

### **LOCATION DATA (HIERARCHICAL)**

The `location` array contains a **5-level hierarchy**:

```json
"location": [
  {
    "id": 1,
    "level": 0,  // Country
    "externalID": "5001",
    "name": "UAE",
    "slug": "/uae"
  },
  {
    "id": 2,
    "level": 1,  // City
    "externalID": "5002",
    "name": "Dubai",
    "slug": "/dubai"
  },
  {
    "id": 59,
    "level": 2,  // Neighborhood
    "externalID": "5416",
    "name": "Jumeirah Village Circle (JVC)",
    "slug": "/dubai/jumeirah-village-circle-jvc",
    "type": "neighbourhood"
  },
  {
    "id": 1881,
    "level": 3,  // District
    "name": "JVC District 12"
  },
  {
    "id": 80858,
    "level": 4,  // Building
    "name": "Nicholas Residence",
    "type": "condo-building"
  }
]
```

**Location Algorithm Strategies:**

1. **Neighborhood Analysis:**
```python
neighborhood = location[2]["name"]  # Level 2
neighborhood_id = location[2]["externalID"]
```

2. **Comparable Property Search:**
   - Match on level 2 (neighborhood) for same area
   - Match on level 3 (district) for hyper-local comps
   - Match on level 4 (building) for identical building comps

3. **Market Segmentation:**
   - Group by neighborhood for area-specific yield analysis
   - Track price trends per district
   - Building-level occupancy and pricing patterns

**Multi-language Support:**
- `name_l1`: Arabic
- `name_l2`: Chinese
- `name_l3`: Russian

---

### **GEOGRAPHIC COORDINATES**

```json
"_geoloc": {
  "lat": 25.17731883819991,
  "lng": 55.3145995423444
},
"geography": {  // Duplicate of _geoloc
  "lat": 25.17731883819991,
  "lng": 55.3145995423444
}
```

**Algorithm Applications:**
- Calculate distance between properties
- Proximity to landmarks (beaches, malls, metro)
- Heat map visualization of pricing by location
- Cluster analysis for market micro-segmentation

---

### **CATEGORY & PROPERTY TYPE**

```json
"category": [
  {
    "level": 0,
    "externalID": "1",
    "name": "Residential",
    "slug": "residential"
  },
  {
    "level": 1,
    "externalID": "4",
    "name": "Apartments",  // or "Villas", "Townhouses"
    "slug": "apartments",
    "nameSingular": "Apartment"
  }
]
```

**Property Types:**
- Apartments (externalID: "4")
- Villas
- Townhouses
- Penthouses
- Studios (rooms = 0)

**Algorithm Use:**
- Filter comparables by exact property type
- Type-specific valuation models (villa vs apartment)
- Market analysis per property category

---

### **PHOTOS & MEDIA**

```json
"coverPhoto": {
  "id": 793045933,
  "externalID": "234805575",
  "url": "https://bayut-production.s3.eu-central-1.amazonaws.com/image/...",
  "nimaScore": 8.892648690292845,  // Photo quality score (0-10)
  "main": true
},
"photoCount": 45,
"videoCount": 0,
"panoramaCount": 0,
"photoIDs": [793045933, 793045910, ...]  // All photo IDs
```

**Media Quality Indicators:**
- `nimaScore`: Neural Image Assessment score (higher = better quality)
- High photo count suggests professional listing
- Video/panorama presence = premium listing

**Algorithm Applications:**
- Listing quality scoring
- Marketing effectiveness correlation
- Days-on-market prediction based on media quality

---

### **TIMESTAMPS & LISTING STATUS**

```json
"createdAt": 1756998527.0,      // Unix timestamp
"updatedAt": 1762337567.0,
"reactivatedAt": 1756998527.0,
"state": "active"
```

**Calculate Days on Market:**
```python
import time
current_time = time.time()
days_on_market = (current_time - created_at) / 86400  # 86400 seconds in a day
```

**Algorithm Use:**
- Identify stale listings (long days on market)
- Price reduction prediction
- Market velocity analysis

---

### **AMENITIES (EXTENSIVE LIST)**

```json
"amenities": [
  "Swimming Pool",
  "Gym or Health Club",
  "Kids Play Area",
  "Parking Spaces",
  "Security Staff",
  "CCTV Security",
  // ... 30+ possible amenities
]
```

**Common Amenities Categories:**

**Building Features:**
- Swimming Pool, Gym, Sauna, Steam Room
- Security Staff, CCTV Security, 24 Hours Concierge
- Elevators, Service Elevators, Electricity Backup

**Property Features:**
- Balcony or Terrace, Maids Room, Study Room
- Centrally Air-Conditioned, Central Heating
- Double Glazed Windows, Built-in Wardrobes

**Location Features:**
- Nearby Schools, Nearby Hospitals, Nearby Shopping Malls
- Nearby Public Transport, Distance From Airport

**Amenity Scoring Algorithm:**
```python
# Weighted amenity score
amenity_weights = {
    "Swimming Pool": 5,
    "Gym or Health Club": 4,
    "Parking Spaces": 3,
    "Security Staff": 4,
    "Balcony or Terrace": 3,
    "Maids Room": 2
}

amenity_score = sum(amenity_weights.get(a, 1) for a in amenities)
```

**Premium Indicators:**
- Jacuzzi, Steam Room, Sauna = luxury properties
- Smart Home, Smart Lock = modern/tech properties
- Concierge, Valet Parking = high-end buildings

---

### **VERIFICATION & TRUST SCORES**

```json
"isVerified": true,
"verification": {
  "status": "verified",
  "verifiedAt": 1762337567.0,
  "trucheckedAt": 1762337567.0,
  "eligible": true
},
"verifiedScore": 0,
"truBrokerScore": 1,
"isTruBroker": true
```

**Trust Indicators:**
- `isVerified`: Property has been verified by Bayut
- `truBrokerScore`: Agent trustworthiness (0-1)
- `verifiedScore`: Listing verification score

**Data Quality Filter:**
```python
reliable_listing = (
    property["isVerified"] and
    property["verification"]["status"] == "verified" and
    property["truBrokerScore"] >= 0.5
)
```

---

### **AGENT & AGENCY DATA**

```json
"contactName": "Ahmad Al Saleh",
"phoneNumber": {
  "mobile": "+971559557640",
  "whatsapp": "971545695868",
  "proxyPhone": "+97148757251"
},
"ownerAgent": {
  "externalID": "2463376",
  "name": "Ahmad Al Saleh",
  "user_image": "https://...",
  "isTruBroker": true,
  "slug": "ahmad-al-saleh-2463376"
},
"agency": {
  "id": 29874478,
  "name": "Rise And Chill Holiday Homes",
  "externalID": "106331",
  "product": "premium",  // "premium", "basic", "superhot"
  "productScore": 2,
  "tier": 4,  // Agency tier (1-4, lower = better)
  "tr": 4,
  "performanceCohort": "overachieving",  // or "average", "underperforming"
  "logo": {...},
  "createdAt": "2025-01-20T11:21:25+00:00"
}
```

**Agency Performance Metrics:**
- `tier`: 1 = top tier, 4 = basic tier
- `performanceCohort`: Market performance classification
- `productScore`: Listing product quality (0-2)

**Agent Reliability Algorithm:**
```python
agent_score = (
    (5 - agency["tier"]) * 0.3 +  # Tier (inverted)
    agency["productScore"] * 0.2 +
    (1 if ownerAgent["isTruBroker"] else 0) * 0.5
)
```

---

### **SCORING & RANKING METRICS**

```json
"score": 100,
"score_l1": 91,  // Language-specific scores
"score_l2": 75,
"score_l3": 75,
"boostedScore_l1": 840,
"deltaScore_l1": 330,
"indyScore": 840,
"cityLevelScore": 1,
"locationPurposeTier": 3  // Location quality tier (1-4)
```

**Bayut's Internal Ranking:**
- `score`: Base listing quality score (0-100)
- `boostedScore`: Promoted/boosted listing score
- `indyScore`: Independent quality score
- `cityLevelScore`: City-level ranking
- `locationPurposeTier`: Location desirability (1=best, 4=lower)

**Use in Algorithms:**
- High `indyScore` = high-quality listing
- Low `locationPurposeTier` = premium location
- `deltaScore` shows score changes over time

---

### **PRODUCT & LISTING TYPE**

```json
"product": "superhot",  // "superhot", "hot", "premium", "basic"
"productLabel": "default",
"productScore": 0,
"productTruBrokerScore": 0
```

**Product Types:**
- **superhot**: Featured/promoted listings (best visibility)
- **hot**: Premium listings
- **premium**: Standard premium
- **basic**: Regular listings

**Market Insights:**
- Superhot properties may be overpriced (high marketing spend)
- Basic listings might be undervalued opportunities
- Filter by product type for fair market comparison

---

### **OCCUPANCY & STATUS**

```json
"occupancyStatus": "vacant",  // or "occupied"
"completionStatus": "completed",  // or "under-construction", "off-plan"
"furnishingStatus": "furnished",  // or "unfurnished", "semi-furnished"
"floorPlanID": 11793,  // Floor plan availability
"hasProject": false,
"hasUnitPlan": false,
"hasMatchingFloorPlans": true
```

**Immediate Availability Factors:**
- `occupancyStatus: "vacant"` = ready to move in
- `completionStatus: "completed"` = not off-plan
- `furnishingStatus: "furnished"` = no setup needed

**Investment Analysis:**
```python
# Ready-to-rent score
ready_score = (
    (1 if occupancy == "vacant" else 0) * 0.4 +
    (1 if completion == "completed" else 0) * 0.3 +
    (1 if furnishing == "furnished" else 0.5) * 0.3
)
```

---

### **KEYWORDS & MARKETING TAGS**

```json
"keywords": [
  "new",
  "luxury",
  "pool",
  "modern",
  "furnished",
  "parking",
  "balcony",
  "fully furnished",
  "ready"
],
"keywords_l1": ["جديدة", "فاخرة", ...]  // Arabic
```

**Keyword Analysis:**
- **Premium Keywords**: "luxury", "designer", "brand new", "sea view"
- **Value Keywords**: "spacious", "bright", "modern"
- **Urgency Keywords**: "ready", "immediate", "vacant"

**Natural Language Processing:**
```python
luxury_keywords = ["luxury", "designer", "premium", "exclusive"]
is_luxury = any(kw in keywords for kw in luxury_keywords)

value_keywords = ["spacious", "bright", "large", "community"]
value_score = sum(1 for kw in value_keywords if kw in keywords)
```

---

### **TRANSACTION HISTORY**

```json
"extraFields": {
  "dldBuildingNK": "tabu-349454436",
  "dldPropertySK": "8405283",
  "hasRentTransactions": true,
  "hasSaleTransactions": true
}
```

**DLD (Dubai Land Department) Integration:**
- `dldBuildingNK`: Official building registration
- `dldPropertySK`: Official property registration
- `hasRentTransactions`: Historical rental data exists
- `hasSaleTransactions`: Historical sale data exists

**Market Intelligence:**
- Properties with transaction history = more reliable data
- Cross-reference with DLD for official sale prices
- Historical transaction analysis for price trends

---

### **PROJECT INFORMATION** (For New Developments)

```json
"project": {
  "id": 5872266,
  "externalID": "906",
  "completionStatus": "under-construction",  // or "completed"
  "agency": {
    "externalID": "551",
    "name": "Sobha Realty",
    "slug": "sobha-realty"
  }
},
"projectNumber": null,
"permitNumber": null
```

**Developer Analysis:**
- Track projects by major developers (Emaar, Sobha, Azizi)
- Off-plan vs completed ratio
- Developer reputation scoring

---

## COMPLETE PROPERTY OBJECT EXAMPLE

```json
{
  "id": 9397996,
  "externalID": "12708951",
  "referenceNumber": "HH.THCREST.2050",
  "price": 15999.0,
  "rentFrequency": "monthly",
  "purpose": "for-rent",
  "rooms": 2,
  "baths": 2,
  "area": 75.06565632,
  "furnishingStatus": "furnished",
  "title": "Fully Furnished | Prime Location | Negotiable",
  "location": [
    {"level": 0, "name": "UAE"},
    {"level": 1, "name": "Dubai"},
    {"level": 2, "name": "Sobha Hartland", "externalID": "8949"},
    {"level": 3, "name": "The Crest"},
    {"level": 4, "name": "The Crest Tower B", "type": "condo-building"}
  ],
  "_geoloc": {"lat": 25.177318, "lng": 55.314599},
  "amenities": [
    "Swimming Pool", "Gym or Health Club", "Kids Play Area",
    "Security Staff", "CCTV Security", "Parking Spaces"
  ],
  "photoCount": 45,
  "coverPhoto": {
    "url": "https://bayut-production.s3...",
    "nimaScore": 8.89
  },
  "isVerified": true,
  "agency": {
    "name": "Rise And Chill Holiday Homes",
    "tier": 4,
    "performanceCohort": "overachieving"
  },
  "occupancyStatus": "vacant",
  "completionStatus": "completed",
  "indyScore": 840,
  "locationPurposeTier": 3
}
```

---

## ALGORITHM DEVELOPMENT STRATEGIES

### **1. VALUATION ALGORITHM**

```python
def calculate_property_value(target_property, comparable_properties):
    """
    Inputs needed:
    - target_property: {price, area, rooms, baths, location, amenities}
    - comparable_properties: List of similar properties
    """
    
    # Price per sqft analysis
    comp_prices_per_sqft = [
        comp["price"] / comp["area"] 
        for comp in comparable_properties 
        if comp["area"] > 0
    ]
    
    avg_price_per_sqft = statistics.median(comp_prices_per_sqft)
    estimated_value = avg_price_per_sqft * target_property["area"]
    
    # Amenity adjustment
    target_amenities = set(target_property["amenities"])
    avg_comp_amenities = statistics.mean([
        len(comp["amenities"]) for comp in comparable_properties
    ])
    
    amenity_factor = len(target_amenities) / avg_comp_amenities
    estimated_value *= amenity_factor
    
    # Verification/quality adjustment
    if target_property["isVerified"]:
        estimated_value *= 1.02  # 2% premium for verified
    
    return estimated_value
```

### **2. COMPARABLE PROPERTY SELECTION**

```python
def find_comparables(target, all_properties, max_distance_km=2):
    """
    Find comparable properties based on multiple factors
    """
    comparables = []
    
    target_neighborhood = target["location"][2]["externalID"]  # Level 2
    
    for prop in all_properties:
        # Must match criteria
        if (prop["purpose"] != target["purpose"] or
            abs(prop["rooms"] - target["rooms"]) > 1 or
            prop["location"][2]["externalID"] != target_neighborhood):
            continue
        
        # Area similarity (within 30%)
        area_ratio = prop["area"] / target["area"]
        if not (0.7 <= area_ratio <= 1.3):
            continue
        
        # Price similarity (within 40%)
        price_ratio = prop["price"] / target["price"]
        if not (0.6 <= price_ratio <= 1.4):
            continue
        
        # Geographic distance
        distance = haversine_distance(
            target["_geoloc"], 
            prop["_geoloc"]
        )
        if distance > max_distance_km:
            continue
        
        # Quality filters
        if not prop["isVerified"] or prop["state"] != "active":
            continue
        
        comparables.append(prop)
    
    return comparables[:20]  # Top 20 comps
```

### **3. RENTAL YIELD CALCULATION**

```python
def calculate_rental_yield(property_data):
    """
    Calculate rental yield for investment analysis
    """
    if property_data["purpose"] == "for-rent":
        # Estimate sale price from similar sold properties
        # (requires historical sale data)
        annual_rent = property_data["price"] * 12  # Monthly to annual
        estimated_sale_price = estimate_sale_price(property_data)
        rental_yield = (annual_rent / estimated_sale_price) * 100
    
    elif property_data["purpose"] == "for-sale":
        # Estimate rent from similar rental properties
        sale_price = property_data["price"]
        estimated_annual_rent = estimate_annual_rent(property_data)
        rental_yield = (estimated_annual_rent / sale_price) * 100
    
    # Adjust for location tier
    location_tier = property_data["locationPurposeTier"]
    yield_adjustment = {1: 1.1, 2: 1.05, 3: 1.0, 4: 0.95}
    
    adjusted_yield = rental_yield * yield_adjustment.get(location_tier, 1.0)
    
    return {
        "gross_yield": rental_yield,
        "adjusted_yield": adjusted_yield,
        "location_factor": yield_adjustment.get(location_tier, 1.0)
    }
```

### **4. UNDERVALUED PROPERTY DETECTION**

```python
def find_undervalued_properties(properties):
    """
    Identify potentially undervalued properties
    """
    undervalued = []
    
    for prop in properties:
        # Get comparables
        comps = find_comparables(prop, properties)
        
        if len(comps) < 5:
            continue  # Not enough data
        
        # Calculate expected price
        expected_value = calculate_property_value(prop, comps)
        actual_price = prop["price"]
        
        # Valuation ratio
        ratio = actual_price / expected_value
        
        # Undervalued if priced 10%+ below expected
        if ratio < 0.90:
            undervalued.append({
                "property": prop,
                "expected_value": expected_value,
                "actual_price": actual_price,
                "discount_percentage": (1 - ratio) * 100,
                "confidence": calculate_confidence(prop, comps)
            })
    
    # Sort by discount percentage
    undervalued.sort(key=lambda x: x["discount_percentage"], reverse=True)
    
    return undervalued
```

### **5. MARKET TREND ANALYSIS**

```python
def analyze_market_trends(properties, time_window_days=90):
    """
    Analyze pricing trends by neighborhood
    """
    from collections import defaultdict
    import datetime
    
    current_time = time.time()
    cutoff_time = current_time - (time_window_days * 86400)
    
    neighborhood_data = defaultdict(list)
    
    for prop in properties:
        if prop["createdAt"] < cutoff_time:
            continue
        
        neighborhood = prop["location"][2]["name"]
        price_per_sqft = prop["price"] / prop["area"] if prop["area"] > 0 else 0
        
        neighborhood_data[neighborhood].append({
            "price_per_sqft": price_per_sqft,
            "timestamp": prop["createdAt"],
            "rooms": prop["rooms"]
        })
    
    trends = {}
    for neighborhood, data in neighborhood_data.items():
        if len(data) < 10:
            continue
        
        # Calculate trend
        data.sort(key=lambda x: x["timestamp"])
        recent = data[-len(data)//3:]  # Last third
        older = data[:len(data)//3]    # First third
        
        recent_avg = statistics.mean([d["price_per_sqft"] for d in recent])
        older_avg = statistics.mean([d["price_per_sqft"] for d in older])
        
        trend_pct = ((recent_avg - older_avg) / older_avg) * 100
        
        trends[neighborhood] = {
            "price_change_pct": trend_pct,
            "avg_price_per_sqft": recent_avg,
            "sample_size": len(data),
            "trend": "increasing" if trend_pct > 2 else "decreasing" if trend_pct < -2 else "stable"
        }
    
    return trends
```

---

## KEY DATA POINTS FOR OPUS ALGORITHMS

### **Essential Fields for Property Valuation:**
1. `price` - Current asking price
2. `area` - Square footage
3. `rooms` - Bedroom count
4. `baths` - Bathroom count
5. `location[2].externalID` - Neighborhood identifier
6. `furnishingStatus` - Furnished status
7. `amenities` - List of amenities
8. `isVerified` - Data quality indicator

### **Essential Fields for Investment Analysis:**
1. `purpose` - For rent or for sale
2. `rentFrequency` - Monthly/yearly
3. `locationPurposeTier` - Location quality (1-4)
4. `occupancyStatus` - Vacancy status
5. `completionStatus` - Construction status
6. `hasRentTransactions` - Historical data availability
7. `indyScore` - Quality score

### **Essential Fields for Market Analysis:**
1. `createdAt` - Listing date
2. `updatedAt` - Last update
3. `location` hierarchy - Geographic segmentation
4. `_geoloc` - Coordinates for mapping
5. `agency.performanceCohort` - Market performance
6. `keywords` - Marketing indicators

---

## DATA QUALITY CONSIDERATIONS

### **High-Quality Listing Indicators:**
```python
def is_high_quality_listing(prop):
    return (
        prop["isVerified"] == True and
        prop["photoCount"] >= 10 and
        prop["area"] > 0 and
        prop["price"] > 0 and
        prop["indyScore"] > 500 and
        len(prop["amenities"]) >= 5
    )
```

### **Outlier Detection:**
```python
def is_outlier(prop, comps):
    """Detect price outliers"""
    comp_prices = [c["price"] / c["area"] for c in comps if c["area"] > 0]
    prop_price_per_sqft = prop["price"] / prop["area"]
    
    mean_price = statistics.mean(comp_prices)
    std_price = statistics.stdev(comp_prices)
    
    z_score = abs((prop_price_per_sqft - mean_price) / std_price)
    
    return z_score > 3  # More than 3 standard deviations
```

---

## NEXT STEPS FOR ALGORITHM DEVELOPMENT

1. **Data Collection Pipeline:**
   - Paginate through all results (`nbPages`)
   - Store in database with timestamps
   - Update daily for fresh market data

2. **Feature Engineering:**
   - Calculate price per sqft
   - Amenity scoring system
   - Location quality index
   - Agent reliability score

3. **Machine Learning Models:**
   - Price prediction (regression)
   - Undervalued property detection (classification)
   - Days-on-market prediction
   - Rental yield optimization

4. **Market Intelligence:**
   - Neighborhood price trends
   - Supply/demand by area
   - Seasonal patterns
   - Agent performance tracking

---

## SUMMARY FOR CLAUDE OPUS

**You now have access to:**
- 50+ data fields per property
- Hierarchical location data (5 levels)
- 30+ amenity types
- Agent & agency performance metrics
- Photo quality scores
- Verification status
- Market positioning scores
- Historical transaction indicators

**Use this data to build:**
- Property valuation models
- Comparable property selection algorithms
- Rental yield calculators
- Undervalued property detectors
- Market trend analyzers
- Investment opportunity scorers

**Key manipulation strategies:**
- Group by `location[2].externalID` for neighborhood analysis
- Calculate `price / area` for price per sqft
- Filter by `isVerified` and `indyScore` for quality
- Use `_geoloc` for geographic clustering
- Leverage `amenities` for feature scoring
- Track `createdAt` for market velocity

---

*End of Documentation*
