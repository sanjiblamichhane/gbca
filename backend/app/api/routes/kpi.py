# app/api/routes/kpi.py
from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import get_current_active_superuser
from app.models import KPI, KPIsPublic

router = APIRouter(tags=["kpi"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=KPIsPublic,
)
def read_kpis() -> Any:
    """
    Retrieve KPIs.
    """
    kpis = [
        KPI(id=1, name="Monthly Recurring Revenue", value=15000.0, unit="USD"),
        KPI(id=2, name="Customer Acquisition Cost", value=120.5, unit="USD"),
        KPI(id=3, name="Customer Churn Rate", value=5.2, unit="%"),
        KPI(id=4, name="Daily Active Users", value=1200, unit=None),
    ]

    return KPIsPublic(data=kpis, count=len(kpis))