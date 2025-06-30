"""
Real Estate Data Utilities
Comprehensive utilities for managing and querying real estate data
"""

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class PropertyFilter:
    """Filter criteria for property searches"""

    min_price: Optional[int] = None
    max_price: Optional[int] = None
    min_bedrooms: Optional[int] = None
    max_bedrooms: Optional[int] = None
    min_bathrooms: Optional[float] = None
    max_bathrooms: Optional[float] = None
    areas: Optional[List[str]] = None
    property_types: Optional[List[str]] = None
    min_sqft: Optional[int] = None
    max_sqft: Optional[int] = None
    features: Optional[List[str]] = None


class RealEstateDataManager:
    """Centralized manager for all real estate data"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self._cache = {}
        self._load_all_data()

    def _load_json_file(self, filepath: str) -> Dict[str, Any]:
        """Load JSON file with caching"""
        if filepath in self._cache:
            return self._cache[filepath]

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._cache[filepath] = data
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _load_all_data(self):
        """Load all data files"""
        self.properties = self._load_json_file(
            os.path.join(self.data_dir, "properties", "active_listings.json")
        )
        self.agents = self._load_json_file(
            os.path.join(self.data_dir, "agents", "agent_profiles.json")
        )
        self.market = self._load_json_file(
            os.path.join(self.data_dir, "market", "market_analytics.json")
        )
        self.clients = self._load_json_file(
            os.path.join(self.data_dir, "clients", "client_database.json")
        )
        self.amenities = self._load_json_file(
            os.path.join(self.data_dir, "amenities", "local_amenities.json")
        )
        self.transactions = self._load_json_file(
            os.path.join(self.data_dir, "transactions", "recent_sales.json")
        )
        self.areas = self._load_json_file(
            os.path.join(self.data_dir, "areas", "city_overview.json")
        )

    def refresh_data(self):
        """Refresh all cached data"""
        self._cache.clear()
        self._load_all_data()

    # Property Operations
    def get_all_properties(self) -> List[Dict[str, Any]]:
        """Get all active property listings"""
        return self.properties.get("active_listings", [])

    def get_property_by_id(self, property_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific property by ID"""
        for prop in self.get_all_properties():
            if prop.get("id") == property_id:
                return prop
        return None

    def filter_properties(self, filters: PropertyFilter) -> List[Dict[str, Any]]:
        """Filter properties based on criteria"""
        properties = self.get_all_properties()
        filtered = []

        for prop in properties:
            if self._matches_filter(prop, filters):
                filtered.append(prop)

        return filtered

    def _matches_filter(self, prop: Dict[str, Any], filters: PropertyFilter) -> bool:
        """Check if property matches filter criteria"""
        # Price range
        if filters.min_price and prop.get("price", 0) < filters.min_price:
            return False
        if filters.max_price and prop.get("price", float("inf")) > filters.max_price:
            return False

        # Bedrooms
        if filters.min_bedrooms and prop.get("bedrooms", 0) < filters.min_bedrooms:
            return False
        if (
            filters.max_bedrooms
            and prop.get("bedrooms", float("inf")) > filters.max_bedrooms
        ):
            return False

        # Bathrooms
        if filters.min_bathrooms and prop.get("bathrooms", 0) < filters.min_bathrooms:
            return False
        if (
            filters.max_bathrooms
            and prop.get("bathrooms", float("inf")) > filters.max_bathrooms
        ):
            return False

        # Areas
        if filters.areas and prop.get("area") not in filters.areas:
            return False

        # Property types
        if (
            filters.property_types
            and prop.get("property_type") not in filters.property_types
        ):
            return False

        # Square footage
        if filters.min_sqft and prop.get("square_feet", 0) < filters.min_sqft:
            return False
        if (
            filters.max_sqft
            and prop.get("square_feet", float("inf")) > filters.max_sqft
        ):
            return False

        # Features
        if filters.features:
            prop_features = prop.get("features", [])
            for required_feature in filters.features:
                if not any(
                    required_feature.lower() in feature.lower()
                    for feature in prop_features
                ):
                    return False

        return True

    def search_properties(self, query: str) -> List[Dict[str, Any]]:
        """Search properties by text query"""
        properties = self.get_all_properties()
        results = []
        query_lower = query.lower()

        for prop in properties:
            # Search in address, description, features, and area
            searchable_text = " ".join(
                [
                    prop.get("address", ""),
                    prop.get("description", ""),
                    prop.get("area", ""),
                    " ".join(prop.get("features", [])),
                    prop.get("property_type", ""),
                    prop.get("style", ""),
                ]
            ).lower()

            if query_lower in searchable_text:
                results.append(prop)

        return results

    def get_properties_by_agent(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get all properties handled by a specific agent"""
        properties = self.get_all_properties()
        return [prop for prop in properties if prop.get("agent_id") == agent_id]

    def get_properties_by_area(self, area: str) -> List[Dict[str, Any]]:
        """Get all properties in a specific area"""
        properties = self.get_all_properties()
        return [
            prop for prop in properties if prop.get("area", "").lower() == area.lower()
        ]

    # Agent Operations
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """Get all agent profiles"""
        return self.agents.get("agents", [])

    def get_agent_by_id(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific agent by ID"""
        for agent in self.get_all_agents():
            if agent.get("id") == agent_id:
                return agent
        return None

    def search_agents(self, query: str) -> List[Dict[str, Any]]:
        """Search agents by name, specialization, or area"""
        agents = self.get_all_agents()
        results = []
        query_lower = query.lower()

        for agent in agents:
            searchable_text = " ".join(
                [
                    agent.get("name", ""),
                    " ".join(agent.get("specializations", [])),
                    " ".join(agent.get("expertise_areas", [])),
                    agent.get("bio", ""),
                ]
            ).lower()

            if query_lower in searchable_text:
                results.append(agent)

        return results

    def get_agent_performance(self, agent_id: str) -> Dict[str, Any]:
        """Get agent performance metrics"""
        agent = self.get_agent_by_id(agent_id)
        if not agent:
            return {}

        properties = self.get_properties_by_agent(agent_id)
        recent_sales = agent.get("recent_sales", [])

        return {
            "agent_id": agent_id,
            "name": agent.get("name"),
            "active_listings": len(properties),
            "recent_sales_count": len(recent_sales),
            "avg_days_on_market": self._calculate_avg_days_on_market(recent_sales),
            "total_sales_volume": sum(
                sale.get("sale_price", 0) for sale in recent_sales
            ),
            "specializations": agent.get("specializations", []),
            "client_rating": self._calculate_avg_rating(
                agent.get("client_testimonials", [])
            ),
        }

    def _calculate_avg_days_on_market(self, sales: List[Dict[str, Any]]) -> float:
        """Calculate average days on market for sales"""
        if not sales:
            return 0
        days = [sale.get("days_on_market", 0) for sale in sales]
        return sum(days) / len(days) if days else 0

    def _calculate_avg_rating(self, testimonials: List[Dict[str, Any]]) -> float:
        """Calculate average client rating"""
        if not testimonials:
            return 0
        ratings = [t.get("rating", 0) for t in testimonials]
        return sum(ratings) / len(ratings) if ratings else 0

    # Market Operations
    def get_market_overview(self) -> Dict[str, Any]:
        """Get overall market overview"""
        return self.market.get("market_overview", {})

    def get_area_market_data(self, area: str) -> Optional[Dict[str, Any]]:
        """Get market data for a specific area"""
        area_performance = self.market.get("area_performance", {})
        return area_performance.get(area)

    def get_price_analytics(self) -> Dict[str, Any]:
        """Get price analytics data"""
        return self.market.get("price_analytics", {})

    def get_investment_opportunities(self) -> Dict[str, Any]:
        """Get investment opportunity data"""
        return self.market.get("investment_opportunities", {})

    def compare_areas(self, areas: List[str]) -> Dict[str, Any]:
        """Compare market data across multiple areas"""
        comparison = {}
        area_performance = self.market.get("area_performance", {})

        for area in areas:
            if area in area_performance:
                comparison[area] = area_performance[area]

        return comparison

    # Client Operations
    def get_all_clients(self) -> List[Dict[str, Any]]:
        """Get all clients"""
        return self.clients.get("clients", [])

    def get_client_by_id(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific client by ID"""
        for client in self.get_all_clients():
            if client.get("id") == client_id:
                return client
        return None

    def get_clients_by_agent(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get all clients for a specific agent"""
        clients = self.get_all_clients()
        return [client for client in clients if client.get("agent_id") == agent_id]

    def match_clients_to_properties(self, client_id: str) -> List[Dict[str, Any]]:
        """Match properties to client preferences"""
        client = self.get_client_by_id(client_id)
        if not client or client.get("type") != "Buyer":
            return []

        preferences = client.get("preferences", {})
        budget = preferences.get("budget_range", {})

        filters = PropertyFilter(
            min_price=budget.get("min"),
            max_price=budget.get("max"),
            areas=preferences.get("desired_areas"),
            property_types=(
                [preferences.get("property_type")]
                if preferences.get("property_type")
                else None
            ),
        )

        return self.filter_properties(filters)

    # Amenities Operations
    def get_schools_by_area(self, area: str) -> List[Dict[str, Any]]:
        """Get schools near a specific area"""
        # This is a simplified implementation - in reality you'd use geographic data
        all_schools = []
        schools_data = self.amenities.get("schools", {})

        for school_type in [
            "elementary_schools",
            "middle_schools",
            "high_schools",
            "private_schools",
        ]:
            schools = schools_data.get(school_type, [])
            all_schools.extend(schools)

        return all_schools  # In a real implementation, filter by proximity to area

    def get_amenities_by_type(self, amenity_type: str) -> List[Dict[str, Any]]:
        """Get amenities by type (parks, shopping, healthcare, etc.)"""
        return self.amenities.get(amenity_type, {})

    def get_area_amenities(self, area: str) -> Dict[str, Any]:
        """Get all amenities for a specific area"""
        amenities = {}

        # Schools
        amenities["schools"] = self.get_schools_by_area(area)

        # Parks
        parks = self.amenities.get("parks_and_recreation", {}).get("parks", [])
        amenities["parks"] = [
            park for park in parks if park.get("area", "").lower() == area.lower()
        ]

        # Shopping
        shopping = self.amenities.get("shopping", {})
        area_shopping = {}
        for shop_type, shops in shopping.items():
            if isinstance(shops, list):
                area_shopping[shop_type] = [
                    shop
                    for shop in shops
                    if shop.get("area", "").lower() == area.lower()
                ]
        amenities["shopping"] = area_shopping

        return amenities

    # Transaction Operations
    def get_recent_sales(self) -> List[Dict[str, Any]]:
        """Get all recent sales"""
        return self.transactions.get("recent_sales", [])

    def get_sales_by_area(self, area: str) -> List[Dict[str, Any]]:
        """Get recent sales in a specific area"""
        sales = self.get_recent_sales()
        return [sale for sale in sales if sale.get("area", "").lower() == area.lower()]

    def get_sales_by_agent(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get recent sales by a specific agent"""
        sales = self.get_recent_sales()
        return [sale for sale in sales if sale.get("agent_id") == agent_id]

    def calculate_market_trends(self, area: str = None) -> Dict[str, Any]:
        """Calculate market trends based on recent sales"""
        sales = self.get_sales_by_area(area) if area else self.get_recent_sales()

        if not sales:
            return {}

        total_sales = len(sales)
        avg_sale_price = sum(sale.get("sale_price", 0) for sale in sales) / total_sales
        avg_days_on_market = (
            sum(sale.get("days_on_market", 0) for sale in sales) / total_sales
        )
        avg_price_per_sqft = (
            sum(sale.get("price_per_sqft", 0) for sale in sales) / total_sales
        )

        return {
            "total_sales": total_sales,
            "average_sale_price": avg_sale_price,
            "average_days_on_market": avg_days_on_market,
            "average_price_per_sqft": avg_price_per_sqft,
            "area": area or "All Areas",
        }

    # Area Operations
    def get_all_areas(self) -> List[Dict[str, Any]]:
        """Get all area information"""
        return self.areas.get("areas", [])

    def get_area_info(self, area_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific area"""
        areas = self.get_all_areas()
        for area in areas:
            if area.get("name", "").lower() == area_name.lower():
                return area
        return None

    def get_city_overview(self) -> Dict[str, Any]:
        """Get overall city information"""
        return {
            "city_name": self.areas.get("city_name"),
            "state": self.areas.get("state"),
            "population": self.areas.get("population"),
            "median_income": self.areas.get("median_income"),
            "school_districts": self.areas.get("school_districts", []),
            "market_trends": self.areas.get("market_trends", {}),
        }

    # Cross-referencing and Analytics
    def get_comprehensive_area_report(self, area: str) -> Dict[str, Any]:
        """Get comprehensive report for an area including properties, market data, amenities"""
        return {
            "area_info": self.get_area_info(area),
            "market_data": self.get_area_market_data(area),
            "active_properties": self.get_properties_by_area(area),
            "recent_sales": self.get_sales_by_area(area),
            "amenities": self.get_area_amenities(area),
            "market_trends": self.calculate_market_trends(area),
        }

    def get_agent_dashboard(self, agent_id: str) -> Dict[str, Any]:
        """Get comprehensive dashboard for an agent"""
        agent = self.get_agent_by_id(agent_id)
        if not agent:
            return {}

        return {
            "agent_info": agent,
            "performance": self.get_agent_performance(agent_id),
            "active_listings": self.get_properties_by_agent(agent_id),
            "clients": self.get_clients_by_agent(agent_id),
            "recent_sales": self.get_sales_by_agent(agent_id),
        }

    def get_property_insights(self, property_id: str) -> Dict[str, Any]:
        """Get detailed insights for a property including comparable sales and area info"""
        prop = self.get_property_by_id(property_id)
        if not prop:
            return {}

        area = prop.get("area")
        agent = self.get_agent_by_id(prop.get("agent_id"))

        return {
            "property": prop,
            "agent": agent,
            "area_info": self.get_area_info(area),
            "area_market_data": self.get_area_market_data(area),
            "comparable_sales": self.get_sales_by_area(area),
            "area_amenities": self.get_area_amenities(area),
        }


# Global instance
data_manager = RealEstateDataManager()
