"""평양냉면 MCP SSE 서버 (AWS 배포용)"""

import os

from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

from .server import create_server

# SSE Transport 설정
sse = SseServerTransport("/messages/")


async def handle_sse(request):
    """SSE 연결 핸들러"""
    server = create_server()
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await server.run(streams[0], streams[1], server.create_initialization_options())


async def health_check(request):
    """헬스 체크 엔드포인트"""
    return JSONResponse({"status": "ok", "service": "pyongyang-naengmyeon-mcp"})


# Starlette 앱 생성
app = Starlette(
    routes=[
        Route("/", endpoint=health_check),
        Route("/health", endpoint=health_check),
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ]
)


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
