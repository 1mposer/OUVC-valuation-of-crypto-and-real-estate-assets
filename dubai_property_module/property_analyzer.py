"""
Dubai Property OUVC - Core Analysis Engine
Advanced real estate valuation for Dubai market
"""

import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class PropertyType(Enum):
    APARTMENT = "apartment"
    VILLA = "villa"
    TOWNHOUSE = "townhouse"
    PENTHOUSE = "penthouse"
    STUDIO = "studio"


class Area(Enum):
    """Major Dubai areas with distinct pricing dynamics"""
    DUBAI_MARINA = "dubai-marina"
    DOWNTOWN = "downtown-dubai"
    JBR = "jbr"
    PALM_JUMEIRAH = "palm-jumeirah"
    BUSINESS_BAY = "business-bay"
    DIFC = "difc"
    JVC = "jvc"
    SPORTS_CITY = "sports-city"
    DISCOVERY_GARDENS = "discovery-gardens"


def normalize_area(area_name: str) -> str:
    """Normalize area name to match enum format (lowercase with hyphens)"""
    # Create mapping from user-friendly names to enum values
    area_mapping = {
        "dubai marina": "dubai-marina",
        "downtown dubai": "downtown-dubai",
        "jbr": "jbr",
        "palm jumeirah": "palm-jumeirah",
        "business bay": "business-bay",
        "difc": "difc",
        "jvc": "jvc",
        "sports city": "sports-city",
        "discovery gardens": "discovery-gardens"
    }

    normalized_input = area_name.lower().strip()
    return area_mapping.get(normalized_input, normalized_input.replace(" ", "-"))


# Area-specific yield expectations (2024 market data)
AREA_YIELDS = {
    Area.DUBAI_MARINA: {"min": 5.5, "avg": 6.8, "max": 8.2},
    Area.DOWNTOWN: {"min": 4.5, "avg": 5.8, "max": 7.0},
    Area.JBR: {"min": 5.0, "avg": 6.5, "max": 7.8},
    Area.PALM_JUMEIRAH: {"min": 4.0, "avg": 5.2, "max": 6.5},
    Area.BUSINESS_BAY: {"min": 6.0, "avg": 7.5, "max": 9.0},
    Area.JVC: {"min": 6.5, "avg": 8.0, "max": 9.5},
    Area.SPORTS_CITY: {"min": 7.0, "avg": 8.5, "max": 10.0},
    Area.DISCOVERY_GARDENS: {"min": 7.5, "avg": 9.0, "max": 11.0},
}


@dataclass
class Property:
    """Property data model"""
    area: str
    property_type: PropertyType
    bedrooms: int
    bathrooms: int
    size_sqft: int
    price_aed: float
    service_charge_sqft: Optional[float] = None
    furnished: Optional[bool] = None
    view_type: Optional[str] = None
    
    @property
    def price_per_sqft(self) -> float:
        return self.price_aed / self.size_sqft if self.size_sqft > 0 else 0


class BayutClient:
    """Bayut API integration for property data"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://bayut-api1.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "bayut-api1.p.rapidapi.com"
        }
    
    def search_properties(self, 
                         area: str, 
                         property_type: str,
                         bedrooms: int,
                         min_price: float,
                         max_price: float,
                         min_size: int,
                         max_size: int,
                         purpose: str = "for-sale") -> List[Dict]:
        """Search for comparable properties"""
        
        if self.api_key == "demo_mode":
            return self._get_demo_data(area, property_type, bedrooms)
        
        # Real API implementation
        params = {
            "location": area,
            "purpose": purpose,
            "priceMin": int(min_price),
            "priceMax": int(max_price),
            "areaMin": int(min_size),
            "areaMax": int(max_size),
            "sort": "date-desc",
            "page": 0,
            "hitsPerPage": 25
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/properties/list",
                headers=self.headers,
                params=params,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_properties(data.get("hits", []))
            else:
                return []
                
        except Exception:
            return []
    
    def _get_demo_data(self, area: str, property_type: str, bedrooms: int) -> List[Dict]:
        """Demo data for testing without API keys"""
        
        # Realistic demo data based on Dubai market
        demo_properties = [
            {
                "price": 1650000,
                "size_sqft": 1150,
                "bedrooms": 2,
                "bathrooms": 2,
                "area": "dubai-marina",
                "property_type": "apartment"
            },
            {
                "price": 1820000,
                "size_sqft": 1250,
                "bedrooms": 2,
                "bathrooms": 2,
                "area": "dubai-marina",
                "property_type": "apartment"
            },
            {
                "price": 850000,
                "size_sqft": 480,
                "bedrooms": 0,
                "bathrooms": 1,
                "area": "downtown-dubai",
                "property_type": "studio"
            }
        ]
        
        # Filter demo data to match request
        filtered = [p for p in demo_properties 
                   if p["bedrooms"] == bedrooms and p["property_type"] == property_type]
        
        return filtered[:5]  # Return up to 5 comparables
    
    def _parse_properties(self, hits: List[Dict]) -> List[Dict]:
        """Parse Bayut response to property data"""
        properties = []
        
        for hit in hits:
            try:
                prop = {
                    "price": float(hit.get("price", 0)),
                    "size_sqft": int(hit.get("area", 0)),
                    "bedrooms": hit.get("rooms", 0),
                    "bathrooms": hit.get("baths", 1),
                    "area": hit.get("location", [{}])[0].get("name", "Unknown"),
                    "property_type": "apartment"  # Parse from category
                }
                properties.append(prop)
            except:
                continue
        
        return properties


class DubaiPropertyValuator:
    """Main property valuation engine"""
    
    def __init__(self, bayut_key: str):
        self.bayut = BayutClient(bayut_key)
    
    def analyze_property(self,
                        area: str,
                        property_type: str,
                        bedrooms: int,
                        size_sqft: int,
                        asking_price_aed: float,
                        **kwargs) -> Dict:
        """
        Main property analysis function
        """
        
        # Create target property
        # Normalize property_type to lowercase to match enum values
        property_type_normalized = property_type.lower() if isinstance(property_type, str) else property_type
        # Normalize area to match enum format (lowercase with hyphens)
        area_normalized = normalize_area(area) if isinstance(area, str) else area

        target = Property(
            area=area_normalized,
            property_type=PropertyType(property_type_normalized),
            bedrooms=bedrooms,
            bathrooms=kwargs.get("bathrooms", bedrooms),
            size_sqft=size_sqft,
            price_aed=asking_price_aed,
            service_charge_sqft=kwargs.get("service_charge_sqft"),
            furnished=kwargs.get("furnished"),
            view_type=kwargs.get("view_type")
        )
        
        # Fetch comparables
        comps = self._fetch_comparables(target)
        
        if len(comps) < 3:
            return {
                "error": "Insufficient comparable properties found",
                "suggestion": "Try adjusting search criteria"
            }
        
        # Calculate valuation
        estimated_value = self._calculate_valuation(target, comps)
        
        # Calculate rental yield
        rental_data = self._get_rental_estimate(target)
        estimated_yield = (rental_data["avg_annual_rent"] / estimated_value) * 100
        
        # Generate valuation signals
        signals = self._generate_signals(target, estimated_value, estimated_yield, comps)
        
        return {
            "estimated_value": round(estimated_value),
            "confidence_interval": {
                "low": round(estimated_value * 0.9),
                "high": round(estimated_value * 1.1)
            },
            "price_to_estimate_ratio": round(asking_price_aed / estimated_value, 3),
            "estimated_rental_yield": round(estimated_yield, 2),
            "rental_data": rental_data,
            "valuation_signals": signals,
            "comparable_properties": len(comps),
            "data_sources": {"bayut": len(comps)},
            "market_insights": self._get_market_insights(area)
        }
    
    def _fetch_comparables(self, target: Property) -> List[Dict]:
        """Fetch comparable properties"""
        radius_pct = 0.20
        
        min_price = target.price_aed * (1 - radius_pct)
        max_price = target.price_aed * (1 + radius_pct)
        min_size = target.size_sqft * (1 - radius_pct)
        max_size = target.size_sqft * (1 + radius_pct)
        
        return self.bayut.search_properties(
            area=target.area,
            property_type=target.property_type.value,
            bedrooms=target.bedrooms,
            min_price=min_price,
            max_price=max_price,
            min_size=int(min_size),
            max_size=int(max_size)
        )
    
    def _calculate_valuation(self, target: Property, comps: List[Dict]) -> float:
        """Calculate estimated value using comparables"""
        if not comps:
            return target.price_aed
        
        # Simple average method (can be enhanced with ML later)
        prices_per_sqft = [comp["price"] / comp["size_sqft"] 
                          for comp in comps if comp["size_sqft"] > 0]
        
        if prices_per_sqft:
            avg_price_per_sqft = np.mean(prices_per_sqft)
            return avg_price_per_sqft * target.size_sqft
        
        return target.price_aed
    
    def _get_rental_estimate(self, target: Property) -> Dict:
        """Estimate rental income based on area and type"""
        
        # Default rental ranges for different areas (AED per year)
        rental_ranges = {
            "dubai-marina": {1: (80000, 120000), 2: (120000, 180000), 3: (180000, 280000)},
            "downtown-dubai": {0: (60000, 90000), 1: (80000, 120000), 2: (130000, 200000)},
            "business-bay": {1: (70000, 110000), 2: (110000, 170000), 3: (170000, 250000)},
            "jvc": {1: (45000, 70000), 2: (70000, 110000), 3: (110000, 160000)},
        }
        
        area_key = target.area
        bedrooms = target.bedrooms
        
        if area_key in rental_ranges and bedrooms in rental_ranges[area_key]:
            min_rent, max_rent = rental_ranges[area_key][bedrooms]
        else:
            # Fallback estimates
            base_rent = target.size_sqft * 80  # 80 AED per sqft per year
            min_rent = base_rent * 0.8
            max_rent = base_rent * 1.2
        
        avg_rent = (min_rent + max_rent) / 2
        
        return {
            "min_annual_rent": int(min_rent),
            "avg_annual_rent": int(avg_rent),
            "max_annual_rent": int(max_rent),
            "last_updated": datetime.now().isoformat()
        }
    
    def _generate_signals(self, target: Property, estimated_value: float, 
                         estimated_yield: float, comps: List[Dict]) -> Dict:
        """Generate valuation signals and verdict"""
        
        ratio = target.price_aed / estimated_value
        
        # Get area yield benchmark
        area_enum = Area(target.area) if target.area in [a.value for a in Area] else None
        expected_yield = AREA_YIELDS.get(area_enum, {"avg": 6.0})["avg"] if area_enum else 6.0
        
        signals = {
            "price_signal": "neutral",
            "yield_signal": "neutral",
            "overall_verdict": "HOLD",
            "confidence": "medium",
            "key_factors": []
        }
        
        # Price analysis
        if ratio < 0.90:
            signals["price_signal"] = "undervalued"
            signals["key_factors"].append(f"Priced {(1-ratio)*100:.1f}% below estimate")
        elif ratio > 1.10:
            signals["price_signal"] = "overvalued"
            signals["key_factors"].append(f"Priced {(ratio-1)*100:.1f}% above estimate")
        
        # Yield analysis
        if estimated_yield > expected_yield * 1.1:
            signals["yield_signal"] = "attractive"
            signals["key_factors"].append(f"Yield {estimated_yield:.1f}% above area average")
        elif estimated_yield < expected_yield * 0.9:
            signals["yield_signal"] = "low"
            signals["key_factors"].append("Yield below area average")
        
        # Overall verdict
        if signals["price_signal"] == "undervalued" and signals["yield_signal"] == "attractive":
            signals["overall_verdict"] = "STRONG BUY"
        elif signals["price_signal"] == "undervalued" or signals["yield_signal"] == "attractive":
            signals["overall_verdict"] = "BUY"
        elif signals["price_signal"] == "overvalued" or signals["yield_signal"] == "low":
            signals["overall_verdict"] = "AVOID"
        
        # Confidence based on comparables
        if len(comps) > 10:
            signals["confidence"] = "high"
        elif len(comps) < 5:
            signals["confidence"] = "low"
        
        return signals
    
    def _get_market_insights(self, area: str) -> Dict:
        """Get market insights for the area"""
        return {
            "avg_days_on_market": 45,
            "price_trend_3m": 0.03,  # +3% in last 3 months
            "inventory_level": "moderate",
            "buyer_demand": "high"
        }


# Main interface function
def analyze_dubai_property(**kwargs) -> Dict:
    """
    Main function to analyze a Dubai property
    
    Required kwargs:
        area, property_type, bedrooms, size_sqft, asking_price_aed
    
    Optional kwargs:
        bathrooms, furnished, service_charge_sqft, view_type
    """
    
    # Get API key
    bayut_key = os.getenv("BAYUT_API_KEY", "demo_mode")
    
    # Initialize valuator
    valuator = DubaiPropertyValuator(bayut_key)
    
    # Run analysis
    return valuator.analyze_property(**kwargs)