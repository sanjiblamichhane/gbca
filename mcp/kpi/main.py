from datetime import datetime
import logging
from typing import Any, Dict
from helpers import analyze_kpi_trends, calculate_growth_rate, fetch_kpi_data_sync
from api import SAMPLE_KPI_DATA, app
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool
import httpx 
import uvicorn 
from constants import MCP_SERVER_NAME, FASTAPI_URL, logger


# Initialize FastMCP server
mcp = FastMCP(MCP_SERVER_NAME)

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
    main()
    mcp.run(tranport='stdio')
