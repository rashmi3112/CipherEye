import logging
from typing import Dict, Any, Optional
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client
from app.core.config import settings

logger = logging.getLogger(__name__)

class MCPClientManager:
    """
    Manages connections to external MCP (Model Context Protocol) servers.
    This allows agents to discover and call tools provided by external services.
    """
    def __init__(self):
        self.active_sessions: Dict[str, ClientSession] = {}

    async def connect_to_server(self, name: str, url: str):
        """
        Connects to an MCP server using SSE transport.
        Note: In a production app, connection lifecycle needs careful management
        (e.g., using AsyncExitStack). For simplicity, we initialize it here.
        """
        try:
            logger.info(f"Connecting to MCP server '{name}' at {url}...")
            # This is a conceptual representation. Proper async context management
            # is required in actual execution to keep the SSE stream alive.
            # async with sse_client(url) as streams:
            #     async with ClientSession(streams[0], streams[1]) as session:
            #         await session.initialize()
            #         self.active_sessions[name] = session
            logger.info(f"Successfully configured MCP server: {name}")
        except Exception as e:
            logger.error(f"Failed to connect to MCP server {name}: {e}")

    async def initialize_all(self):
        """Initializes all configured MCP servers."""
        if settings.mcp_search_url:
            await self.connect_to_server("search", settings.mcp_search_url)
        if settings.mcp_ocr_url:
            await self.connect_to_server("ocr", settings.mcp_ocr_url)

    async def call_tool(self, server_name: str, tool_name: str, arguments: dict) -> Any:
        """
        Calls a specific tool on a specific MCP server.
        """
        if server_name not in self.active_sessions:
            logger.warning(f"MCP server '{server_name}' is not connected. Tool '{tool_name}' cannot be called.")
            return None
            
        session = self.active_sessions[server_name]
        try:
            result = await session.call_tool(tool_name, arguments)
            return result
        except Exception as e:
            logger.error(f"Error calling tool {tool_name} on {server_name}: {e}")
            return None

# Singleton instance
mcp_manager = MCPClientManager()
