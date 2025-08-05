from typing import Any, Dict, List, Optional
import httpx
from constants import MCP_SERVER_NAME, FASTAPI_URL, logger

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