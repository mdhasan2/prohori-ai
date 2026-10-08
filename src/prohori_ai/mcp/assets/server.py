"""Asset Context MCP server."""

from mcp.server import MCPServer

from prohori_ai.mcp.assets.registry import AssetRegistry


def create_asset_context_server(
    registry: AssetRegistry,
) -> MCPServer:
    """Create the Asset Context MCP Server."""

    mcp = MCPServer("prohoriai-asset-context")

    @mcp.resource(
        "assets://allowlist",
        mime_type="application/json",
    )
    def list_allowlisted_assets() -> list[dict[str, object]]:
        """Return the complete allowlisted asset inventory."""
        return [
            {
                "asset_id": asset.asset_id,
                "name": asset.name,
                "environment": asset.environment,
                "allowed_checks": list(asset.allowed_checks),
            }
            for asset in registry.list_assets()
        ]

    return mcp
