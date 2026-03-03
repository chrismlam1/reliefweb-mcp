"""
ReliefWeb MCP Server
Model Context Protocol server for ReliefWeb humanitarian information API.
Provides access to humanitarian reports, disasters, and jobs.
"""

import os
from typing import Dict
import httpx
from mcp.server.fastmcp import FastMCP
import json
import logging

# Initialize FastMCP server
mcp = FastMCP("reliefweb")

# Constants
API_BASE_URL = 'https://api.reliefweb.int/v1'


async def make_request(endpoint: str, params: Dict) -> str:
    """Make HTTP request to ReliefWeb API"""
    url = f"{API_BASE_URL}/{endpoint}"
    logging.info(f"ReliefWeb Request - URL: {url}, Params: {params}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url,
                json=params,
                timeout=60.0,
                follow_redirects=True
            )
            response.raise_for_status()
            logging.info("ReliefWeb data retrieved successfully")
            return response.text
        except Exception as e:
            logging.error(f"ReliefWeb API request failed: {e}")
            return json.dumps({"error": f"request_failed: {str(e)}"})


@mcp.tool(
    name="search_reports",
    description="Search ReliefWeb reports by country, keywords, and date"
)
async def search_reports(
    country: str,
    query: str = "",
    start_date: str = "",
    end_date: str = "",
    limit: int = 100
) -> str:
    """
    Search ReliefWeb reports
    
    Args:
        country: Country name or ISO3 code
        query: Search keywords (optional)
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        limit: Max results (default 100)
    
    Returns:
        JSON string with reports
    """
    filters = {
        "operator": "AND",
        "conditions": [
            {
                "field": "primary_country.iso3",
                "value": country
            }
        ]
    }
    
    if start_date or end_date:
        date_filter = {"field": "date.created"}
        if start_date and end_date:
            date_filter["value"] = {"from": start_date, "to": end_date}
        elif start_date:
            date_filter["value"] = {"from": start_date}
        else:
            date_filter["value"] = {"to": end_date}
        filters["conditions"].append(date_filter)
    
    params = {
        "appname": "humanitarian-intelligence",
        "filter": filters,
        "limit": limit,
        "fields": {
            "include": ["id", "title", "body", "url", "source", "date", "country"]
        }
    }
    
    if query:
        params["query"] = {"value": query}
    
    return await make_request("reports", params)


@mcp.tool(
    name="search_disasters",
    description="Search ReliefWeb disasters by country and date"
)
async def search_disasters(
    country: str = "",
    disaster_type: str = "",
    start_date: str = "",
    end_date: str = "",
    limit: int = 100
) -> str:
    """
    Search ReliefWeb disasters
    
    Args:
        country: Country name or ISO3 code
        disaster_type: Disaster type (flood, drought, etc.)
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        limit: Max results
    
    Returns:
        JSON string with disasters
    """
    filters = {"operator": "AND", "conditions": []}
    
    if country:
        filters["conditions"].append({
            "field": "primary_country.iso3",
            "value": country
        })
    
    if disaster_type:
        filters["conditions"].append({
            "field": "type.name",
            "value": disaster_type
        })
    
    if start_date or end_date:
        date_filter = {"field": "date.created"}
        if start_date and end_date:
            date_filter["value"] = {"from": start_date, "to": end_date}
        elif start_date:
            date_filter["value"] = {"from": start_date}
        else:
            date_filter["value"] = {"to": end_date}
        filters["conditions"].append(date_filter)
    
    params = {
        "appname": "humanitarian-intelligence",
        "limit": limit,
        "fields": {
            "include": ["id", "name", "description", "url", "date", "country", "type", "status"]
        }
    }
    
    if filters["conditions"]:
        params["filter"] = filters
    
    return await make_request("disasters", params)


@mcp.tool(
    name="search_updates",
    description="Get latest situation updates for a country"
)
async def search_updates(
    country: str,
    theme: str = "",
    limit: int = 50
) -> str:
    """
    Get latest situation updates
    
    Args:
        country: Country name or ISO3 code
        theme: Theme/sector filter (optional)
        limit: Max results
    
    Returns:
        JSON string with updates
    """
    filters = {
        "operator": "AND",
        "conditions": [
            {
                "field": "primary_country.iso3",
                "value": country
            }
        ]
    }
    
    if theme:
        filters["conditions"].append({
            "field": "theme.name",
            "value": theme
        })
    
    params = {
        "appname": "humanitarian-intelligence",
        "filter": filters,
        "limit": limit,
        "sort": ["date:desc"],
        "fields": {
            "include": ["id", "title", "body", "url", "source", "date", "theme"]
        }
    }
    
    return await make_request("reports", params)


def main():
    # Initialize and run the server
    logging.info("Starting ReliefWeb MCP Server")
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
