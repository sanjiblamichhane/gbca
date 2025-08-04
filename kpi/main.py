#!/usr/bin/env python3
"""
FastAPI + MCP Integration for Startup KPI Dashboard
===================================================

This module provides a complete integration between FastAPI and MCP (Model Control Plane)
to fetch and analyze startup KPI data. It allows startup founders to chat with Claude Desktop
to get insights on business metrics like MRR, active users, and churn rate.

Requirements:
- pip install fastapi uvicorn httpx mcp

Usage:
1. Run the FastAPI server: uvicorn main:app --reload
2. Run the MCP server: python main.py
3. Connect Claude Desktop to the MCP server
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
FASTAPI_URL = "http://127.0.0.1:8000"
MCP_SERVER_NAME = "startup-kpi-server"

# Initialize FastMCP server
mcp = FastMCP(MCP_SERVER_NAME)

# Initialize FastAPI app
app = FastAPI(
    title="Startup KPI Dashboard API",
    description="API for fetching startup business metrics and KPI data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample KPI data (in production, this would come from your database)
SAMPLE_KPI_DATA = {
    "metrics": {
        "monthly_recurring_revenue": {
            "unit": "USD",
            "description": "Monthly Recurring Revenue - predictable revenue from subscriptions",
            "data": [
                {"month": "2025-03", "value": 8800},
                {"month": "2025-04", "value": 9700},
                {"month": "2025-05", "value": 10500},
                {"month": "2025-06", "value": 11400},
                {"month": "2025-07", "value": 12250},
                {"month": "2025-08", "value": 12500}
            ]
        },
        "active_users": {
            "unit": "users",
            "description": "Monthly Active Users - unique users who engaged with the product",
            "data": [
                {"month": "2025-03", "value": 2100},
                {"month": "2025-04", "value": 2350},
                {"month": "2025-05", "value": 2675},
                {"month": "2025-06", "value": 2920},
                {"month": "2025-07", "value": 3050},
                {"month": "2025-08", "value": 3100}
            ]
        },
        "churn_rate": {
            "unit": "%",
            "description": "Customer Churn Rate - percentage of customers who stopped using the service",
            "data": [
                {"month": "2025-03", "value": 4.2},
                {"month": "2025-04", "value": 3.8},
                {"month": "2025-05", "value": 3.3},
                {"month": "2025-06", "value": 2.7},
                {"month": "2025-07", "value": 2.3},
                {"month": "2025-08", "value": 2.1}
            ]
        },
        "customer_acquisition_cost": {
            "unit": "USD",
            "description": "Customer Acquisition Cost - average cost to acquire a new customer",
            "data": [
                {"month": "2025-03", "value": 85},
                {"month": "2025-04", "value": 78},
                {"month": "2025-05", "value": 72},
                {"month": "2025-06", "value": 68},
                {"month": "2025-07", "value": 65},
                {"month": "2025-08", "value": 62}
            ]
        },
        "lifetime_value": {
            "unit": "USD",
            "description": "Customer Lifetime Value - predicted revenue from a customer relationship",
            "data": [
                {"month": "2025-03", "value": 580},
                {"month": "2025-04", "value": 620},
                {"month": "2025-05", "value": 650},
                {"month": "2025-06", "value": 680},
                {"month": "2025-07", "value": 720},
                {"month": "2025-08", "value": 750}
            ]
        }
    },
    "last_updated": datetime.now().isoformat(),
    "company_info": {
        "name": "Your Startup",
        "founded": "2024-01-01",
        "industry": "SaaS",
        "stage": "Early Growth"
    }
}

# FastAPI Routes
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Startup KPI Dashboard API",
        "version": "1.0.0",
        "endpoints": {
            "/kpi": "Get all KPI metrics",
            "/kpi/{metric_name}": "Get specific metric data",
            "/insights": "Get AI-generated insights",
            "/health": "Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/kpi")
async def get_all_kpi_data():
    """Get all KPI metrics data."""
    try:
        return SAMPLE_KPI_DATA
    except Exception as e:
        logger.error(f"Error fetching KPI data: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch KPI data")

@app.get("/kpi/{metric_name}")
async def get_specific_metric(metric_name: str):
    """Get data for a specific metric."""
    try:
        if metric_name not in SAMPLE_KPI_DATA["metrics"]:
            raise HTTPException(status_code=404, detail=f"Metric '{metric_name}' not found")
        
        return {
            "metric": metric_name,
            "data": SAMPLE_KPI_DATA["metrics"][metric_name],
            "last_updated": SAMPLE_KPI_DATA["last_updated"]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching metric {metric_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch metric data")

@app.get("/insights")
async def get_business_insights():
    """Generate business insights from KPI data."""
    try:
        insights = analyze_kpi_trends(SAMPLE_KPI_DATA)
        return {
            "insights": insights,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error generating insights: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate insights")

# Helper Functions
async def fetch_kpi_data_async() -> Optional[Dict[str, Any]]:
    """Asynchronously fetch KPI data from the FastAPI endpoint."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{FASTAPI_URL}/kpi", timeout=10.0)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        logger.error(f"Request error while fetching KPI data: {e}")
        return None
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error while fetching KPI data: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error while fetching KPI data: {e}")
        return None

def fetch_kpi_data_sync() -> Optional[Dict[str, Any]]:
    """Synchronously fetch KPI data from the FastAPI endpoint."""
    try:
        response = httpx.get(f"{FASTAPI_URL}/kpi", timeout=10.0)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        logger.error(f"Request error while fetching KPI data: {e}")
        return None
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error while fetching KPI data: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error while fetching KPI data: {e}")
        return None

def calculate_growth_rate(data: List[Dict[str, Any]]) -> float:
    """Calculate growth rate between first and last data points."""
    if len(data) < 2:
        return 0.0
    
    first_value = data[0]["value"]
    last_value = data[-1]["value"]
    
    if first_value == 0:
        return 0.0
    
    return ((last_value - first_value) / first_value) * 100

def analyze_kpi_trends(kpi_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Analyze KPI trends and generate insights."""
    insights = []
    
    for metric_name, metric_info in kpi_data["metrics"].items():
        data = metric_info["data"]
        growth_rate = calculate_growth_rate(data)
        latest_value = data[-1]["value"] if data else 0
        
        # Generate insight based on metric type and trend
        if metric_name == "monthly_recurring_revenue":
            if growth_rate > 15:
                insight = f"🚀 Excellent MRR growth of {growth_rate:.1f}%! Your revenue is scaling well."
            elif growth_rate > 5:
                insight = f"📈 Solid MRR growth of {growth_rate:.1f}%. Consider strategies to accelerate growth."
            else:
                insight = f"📊 MRR growth is {growth_rate:.1f}%. Focus on customer acquisition and retention."
        
        elif metric_name == "churn_rate":
            if latest_value < 3:
                insight = f"✅ Excellent churn rate of {latest_value}%! Your customer retention is strong."
            elif latest_value < 5:
                insight = f"👍 Good churn rate of {latest_value}%. Room for improvement in retention."
            else:
                insight = f"⚠️ High churn rate of {latest_value}%. Urgent attention needed for retention."
        
        elif metric_name == "active_users":
            if growth_rate > 20:
                insight = f"🎯 Outstanding user growth of {growth_rate:.1f}%! Your product is gaining traction."
            elif growth_rate > 10:
                insight = f"📱 Good user growth of {growth_rate:.1f}%. Keep up the momentum."
            else:
                insight = f"👥 User growth is {growth_rate:.1f}%. Consider user acquisition strategies."
        
        else:
            if growth_rate > 0:
                insight = f"📈 {metric_name.replace('_', ' ').title()} is trending up by {growth_rate:.1f}%."
            else:
                insight = f"📉 {metric_name.replace('_', ' ').title()} is trending down by {abs(growth_rate):.1f}%."
        
        insights.append({
            "metric": metric_name,
            "current_value": latest_value,
            "growth_rate": round(growth_rate, 2),
            "insight": insight,
            "unit": metric_info["unit"]
        })
    
    return insights

# MCP Tools
@mcp.tool()
def fetch_startup_kpis() -> Dict[str, Any]:
    """
    Fetch all startup KPI data including MRR, active users, churn rate, CAC, and LTV.
    
    Returns:
        Complete KPI dataset with metrics, trends, and company information.
    """
    logger.info("Fetching startup KPI data via MCP tool")
    
    data = fetch_kpi_data_sync()
    if data is None:
        return {
            "error": "Failed to fetch KPI data from API",
            "status": "error",
            "fallback_data": SAMPLE_KPI_DATA
        }
    
    return {
        "status": "success",
        "data": data,
        "fetched_at": datetime.now().isoformat()
    }

@mcp.tool()
def get_metric_analysis(metric_name: str) -> Dict[str, Any]:
    """
    Get detailed analysis for a specific metric.
    
    Args:
        metric_name: Name of the metric to analyze (e.g., 'monthly_recurring_revenue', 'churn_rate')
    
    Returns:
        Detailed analysis including trends, insights, and recommendations.
    """
    logger.info(f"Analyzing metric: {metric_name}")
    
    try:
        response = httpx.get(f"{FASTAPI_URL}/kpi/{metric_name}", timeout=10.0)
        response.raise_for_status()
        metric_data = response.json()
        
        # Calculate additional analytics
        data_points = metric_data["data"]["data"]
        growth_rate = calculate_growth_rate(data_points)
        
        return {
            "status": "success",
            "metric": metric_name,
            "current_value": data_points[-1]["value"] if data_points else 0,
            "growth_rate": round(growth_rate, 2),
            "trend_direction": "up" if growth_rate > 0 else "down" if growth_rate < 0 else "stable",
            "data_points": len(data_points),
            "unit": metric_data["data"]["unit"],
            "description": metric_data["data"]["description"],
            "raw_data": data_points
        }
    
    except Exception as e:
        logger.error(f"Error analyzing metric {metric_name}: {e}")
        return {
            "status": "error",
            "error": f"Failed to analyze metric: {str(e)}"
        }

@mcp.tool()
def generate_business_insights() -> Dict[str, Any]:
    """
    Generate AI-powered business insights based on current KPI trends.
    
    Returns:
        Comprehensive business insights, recommendations, and strategic analysis.
    """
    logger.info("Generating business insights")
    
    try:
        response = httpx.get(f"{FASTAPI_URL}/insights", timeout=10.0)
        response.raise_for_status()
        insights_data = response.json()
        
        return {
            "status": "success",
            "insights": insights_data["insights"],
            "generated_at": insights_data["generated_at"],
            "summary": "Business insights generated successfully"
        }
    
    except Exception as e:
        logger.error(f"Error generating insights: {e}")
        # Fallback to local analysis
        insights = analyze_kpi_trends(SAMPLE_KPI_DATA)
        return {
            "status": "success_fallback",
            "insights": insights,
            "generated_at": datetime.now().isoformat(),
            "note": "Generated from cached data due to API unavailability"
        }

@mcp.tool()
def compare_metrics(metric1: str, metric2: str) -> Dict[str, Any]:
    """
    Compare two metrics and analyze their correlation.
    
    Args:
        metric1: First metric name
        metric2: Second metric name
    
    Returns:
        Comparison analysis between the two metrics.
    """
    logger.info(f"Comparing metrics: {metric1} vs {metric2}")
    
    data = fetch_kpi_data_sync()
    if not data or metric1 not in data["metrics"] or metric2 not in data["metrics"]:
        return {
            "status": "error",
            "error": "One or both metrics not found"
        }
    
    metric1_data = data["metrics"][metric1]["data"]
    metric2_data = data["metrics"][metric2]["data"]
    
    growth1 = calculate_growth_rate(metric1_data)
    growth2 = calculate_growth_rate(metric2_data)
    
    return {
        "status": "success",
        "comparison": {
            metric1: {
                "growth_rate": round(growth1, 2),
                "current_value": metric1_data[-1]["value"],
                "unit": data["metrics"][metric1]["unit"]
            },
            metric2: {
                "growth_rate": round(growth2, 2),
                "current_value": metric2_data[-1]["value"],
                "unit": data["metrics"][metric2]["unit"]
            }
        },
        "analysis": f"{metric1} is growing at {growth1:.1f}% while {metric2} is at {growth2:.1f}%",
        "correlation": "positive" if (growth1 > 0 and growth2 > 0) or (growth1 < 0 and growth2 < 0) else "negative"
    }

# Main execution functions
async def run_fastapi_server():
    """Run the FastAPI server."""
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=True
    )
    server = uvicorn.Server(config)
    await server.serve()

def run_mcp_server():
    """Run the MCP server."""
    logger.info(f"Starting MCP server: {MCP_SERVER_NAME}")
    mcp.run()

def main():
    """Main entry point - runs both servers."""
    print("🚀 Starting Startup KPI Dashboard")
    print("=" * 50)
    print("This will start both FastAPI and MCP servers.")
    print("FastAPI will be available at: http://127.0.0.1:8000")
    print("MCP server will be available for Claude Desktop integration.")
    print("=" * 50)
    
    # For development, you might want to run these separately:
    # 1. FastAPI: uvicorn main:app --reload
    # 2. MCP: python main.py
    
    print("To run the servers separately:")
    print("1. FastAPI server: uvicorn main:app --reload")
    print("2. MCP server: python main.py")
    print("\nFor Claude Desktop integration, run only the MCP server.")
    
    # Run MCP server (comment out if running FastAPI separately)
    run_mcp_server()

if __name__ == "__main__":
    # Initialize and run the MCP server with stdio transport
    # This is the correct way to run MCP server for Claude Desktop integration
    main()
    mcp.run(transport='stdio')