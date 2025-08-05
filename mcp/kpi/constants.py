import logging

# Configuration
FASTAPI_URL = "http://127.0.0.1:8000"
MCP_SERVER_NAME = "startup-kpi-server"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)