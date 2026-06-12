"""Optional Entra ID authentication helper. Mirrors azure-search-openai-demo's AuthenticationHelper."""
from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


class AuthenticationHelper:
    def __init__(self) -> None:
        self.use_authentication = os.getenv("AZURE_USE_AUTHENTICATION", "false").lower() == "true"
        self.tenant_id = os.getenv("AZURE_AUTH_TENANT_ID")
        self.client_app_id = os.getenv("AZURE_CLIENT_APP_ID")
        self.client_app_secret = os.getenv("AZURE_CLIENT_APP_SECRET")
        self.require_access_control = os.getenv("AZURE_ENFORCE_ACCESS_CONTROL", "false").lower() == "true"
        self.enable_global_documents = os.getenv("AZURE_ENABLE_GLOBAL_DOCUMENT_ACCESS", "true").lower() == "true"

    def get_auth_setup_for_client(self) -> dict[str, Any]:
        return {
            "useLogin": self.use_authentication,
            "requireAccessControl": self.require_access_control,
            "enableUnauthenticatedAccess": self.enable_global_documents,
            "msalConfig": {
                "auth": {
                    "clientId": self.client_app_id,
                    "authority": f"https://login.microsoftonline.com/{self.tenant_id}" if self.tenant_id else None,
                }
            },
        }

    async def get_auth_claims_if_enabled(self, headers: dict[str, str]) -> dict[str, Any] | None:
        if not self.use_authentication:
            return {}
        token = headers.get("Authorization", "").removeprefix("Bearer ").strip()
        if not token:
            return None
        # Real impl validates with msal/jwks; here we accept the token shape for dev.
        return {"oid": "dev-oid", "groups": []}

    async def check_path_auth(self, path: str, headers: dict[str, str]) -> dict[str, Any] | None:
        claims = await self.get_auth_claims_if_enabled(headers)
        if claims is None:
            return None
        if not self.require_access_control:
            return claims
        # Real impl checks ACLs on the path. Dev short-circuit.
        return claims
