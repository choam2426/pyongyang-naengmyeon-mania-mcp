"""평양냉면 MCP 서버 (Streamable HTTP - 클라우드 배포용)"""

import os

from mcp.server.streamable_http import StreamableHTTPServerTransport
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

from .server import create_server

# 서버 인스턴스 (전역)
mcp_server = create_server()

# Streamable HTTP Transport 설정
transport = StreamableHTTPServerTransport("/mcp")


async def handle_mcp(scope, receive, send):
    """MCP ASGI 핸들러"""
    # 서버 연결 및 실행
    async with transport.connect() as (read_stream, write_stream):
        # 백그라운드에서 서버 실행
        import anyio

        async def run_server():
            await mcp_server.run(
                read_stream, write_stream, mcp_server.create_initialization_options()
            )

        async with anyio.create_task_group() as tg:
            tg.start_soon(run_server)
            await transport.handle_request(scope, receive, send)
            tg.cancel_scope.cancel()


async def health_check(request):
    """헬스 체크 엔드포인트"""
    return JSONResponse({"status": "ok", "service": "pyongyang-naengmyeon-mcp"})


# Starlette 앱 생성 (CORS 포함)
app = Starlette(
    routes=[
        Route("/", endpoint=health_check),
        Route("/health", endpoint=health_check),
        Mount("/mcp", app=handle_mcp),
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
