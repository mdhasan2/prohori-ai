import pytest
from mcp import Client
from mcp.server import MCPServer

from prohori_ai.mcp.assets.registry import (
    Asset,
    AssetRegistry,
)
from prohori_ai.mcp.assets.server import (
    create_asset_context_server,
)


@pytest.fixture
def server() -> MCPServer:
    registry = AssetRegistry(
        assets=(
            Asset(
                asset_id="lab-api",
                name="Local Lab",
                base_url="http://127.0.0.1:8081",
                environment="local-lab",
                allowed_checks=("admin_authentication",),
            ),
        ),
        relationships=(),
    )

    return create_asset_context_server(registry)


@pytest.mark.anyio
async def test_allowlist_resource_is_available(
    server: MCPServer,
) -> None:
    async with Client(server) as client:
        resources = await client.list_resources()

        uris = {str(resource.uri) for resource in resources.resources}

        assert "assets://allowlist" in uris
