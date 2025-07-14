import os
import logging
from typing import Optional
import aiohttp

logger = logging.getLogger(__name__)

async def get_agentos_jwt_token(session: aiohttp.ClientSession, agentos_url: str) -> Optional[str]:
    """
    Retrieve AgentOS JWT token from environment or by logging in.
    Args:
        session: aiohttp session
        agentos_url: Base URL for AgentOS
    Returns:
        JWT token string or None if authentication fails
    """
    # 1. Check for token in environment
    jwt_token = os.environ.get("AGENTOS_JWT_TOKEN")
    if jwt_token:
        logger.info("✅ Using JWT token from environment for AgentOS")
        return jwt_token

    # 2. Otherwise, login with username/password
    username = os.environ.get("AGENTOS_USERNAME", "ethiq_user")
    password = os.environ.get("AGENTOS_PASSWORD", "ethiq_password")
    login_url = f"{agentos_url}/api/login/access-token"
    try:
        resp = await session.post(
            login_url,
            data={"username": username, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if resp.status == 200:
            data = await resp.json()
            token = data.get("access_token")
            if token:
                logger.info("✅ Authenticated with AgentOS and obtained JWT token")
                return token
            else:
                logger.warning("⚠️ Login succeeded but no access_token in response")
        else:
            logger.warning(f"⚠️ AgentOS login failed: HTTP {resp.status}")
    except Exception as e:
        logger.warning(f"⚠️ Exception during AgentOS login: {e}")
    return None 