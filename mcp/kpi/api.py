from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from constants import logger

# Initialize FastAPI app
app = FastAPI(
    title="[GBCA] Startup KPI Dashboard API",
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
        "name": "GivingbackAI CoFounder Agent",
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
        insights = analyze_kpi_trends(SAMPLE_KPI_DATA) # TODO
        return {
            "insights": insights,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error generating insights: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate insights")