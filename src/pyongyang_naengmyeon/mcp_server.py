"""평양냉면 MCP 서버 (SSE + Streamable HTTP 둘 다 지원)"""

import os

from mcp.server.sse import SseServerTransport
from mcp.server.streamable_http import StreamableHTTPServerTransport
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

from .server import create_server

# ============================================================
# SSE Transport (레거시 클라이언트용)
# ============================================================
sse_transport = SseServerTransport("/messages/")


async def handle_sse(request):
    """SSE 연결 핸들러"""
    server = create_server()
    async with sse_transport.connect_sse(request.scope, request.receive, request._send) as streams:
        await server.run(streams[0], streams[1], server.create_initialization_options())


# ============================================================
# Streamable HTTP Transport (PlayMCP 등 최신 클라이언트용)
# ============================================================
class MCPHandler:
    """MCP Streamable HTTP 핸들러"""

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return

        import anyio

        # 요청 경로에 맞게 transport 생성
        path = scope.get("path", "/mcp").rstrip("/") or "/mcp"
        request_transport = StreamableHTTPServerTransport(path)
        server = create_server()

        async with request_transport.connect() as (read_stream, write_stream):

            async def run_server():
                await server.run(read_stream, write_stream, server.create_initialization_options())

            async with anyio.create_task_group() as tg:
                tg.start_soon(run_server)
                await request_transport.handle_request(scope, receive, send)
                tg.cancel_scope.cancel()


mcp_handler = MCPHandler()


# ============================================================
# Health Check
# ============================================================
async def health_check(request):
    """헬스 체크 엔드포인트"""
    return JSONResponse(
        {
            "status": "ok",
            "service": "pyongyang-naengmyeon-mcp",
            "endpoints": {"sse": "/sse", "streamable_http": "/mcp", "health": "/health"},
        }
    )


# ============================================================
# Starlette 앱
# ============================================================
app = Starlette(
    routes=[
        # Health
        Route("/", endpoint=health_check),
        Route("/health", endpoint=health_check),
        # SSE (레거시)
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse_transport.handle_post_message),
        # Streamable HTTP (PlayMCP용) - 두 경로 모두 지원
        Route("/mcp", endpoint=mcp_handler, methods=["GET", "POST", "DELETE", "OPTIONS"]),
        Route("/mcp/", endpoint=mcp_handler, methods=["GET", "POST", "DELETE", "OPTIONS"]),
    ],
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ],
)


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
