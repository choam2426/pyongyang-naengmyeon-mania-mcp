"""평양냉면 MCP 서버 (SSE + Streamable HTTP 지원)"""

import asyncio
import json
import os
import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.server.streamable_http import StreamableHTTPServerTransport

from .server import create_server

# 타입 정의
Scope = dict[str, Any]
Receive = Callable[[], Awaitable[dict[str, Any]]]
Send = Callable[[dict[str, Any]], Awaitable[None]]

# SSE Transport 설정 (하위 호환성 유지)
sse = SseServerTransport("/messages/")


@dataclass
class StreamableSession:
    """Streamable HTTP 세션"""

    transport: StreamableHTTPServerTransport
    server: Server
    task: asyncio.Task[None] | None = None
    ready: asyncio.Event | None = None


# Streamable HTTP Transport 세션 저장소
streamable_sessions: dict[str, StreamableSession] = {}


async def _send_json_response(send: Send, body: dict[str, Any], status: int = 200) -> None:
    """JSON 응답 전송 헬퍼"""
    body_bytes = json.dumps(body).encode()
    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": [[b"content-type", b"application/json"]],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": body_bytes,
        }
    )


async def streamable_http_handler(scope: Scope, receive: Receive, send: Send) -> None:
    """Streamable HTTP ASGI 핸들러 (MCP 2025-03-26 스펙)"""
    # 세션 ID 확인
    headers = dict(scope.get("headers", []))
    session_id = headers.get(b"mcp-session-id", b"").decode() or None
    method = scope.get("method", "GET")

    if method == "POST":
        # 기존 세션이 있으면 사용
        if session_id and session_id in streamable_sessions:
            session = streamable_sessions[session_id]
            if session.ready:
                await session.ready.wait()
            await session.transport.handle_request(scope, receive, send)
            return

        # 새 세션 생성
        new_session_id = str(uuid.uuid4())
        transport = StreamableHTTPServerTransport(
            mcp_session_id=new_session_id,
            is_json_response_enabled=True,
        )
        server = create_server()
        ready_event = asyncio.Event()

        async def run_session() -> None:
            """세션에서 서버 실행"""
            async with transport.connect() as streams:
                ready_event.set()
                await server.run(streams[0], streams[1], server.create_initialization_options())

        # 백그라운드 태스크 시작
        task = asyncio.create_task(run_session())

        # 연결이 준비될 때까지 대기
        await ready_event.wait()

        # 요청 처리
        await transport.handle_request(scope, receive, send)

        # 세션 저장
        streamable_sessions[new_session_id] = StreamableSession(
            transport=transport,
            server=server,
            task=task,
            ready=ready_event,
        )
        return

    elif method == "GET":
        if session_id and session_id in streamable_sessions:
            session = streamable_sessions[session_id]
            if session.ready:
                await session.ready.wait()
            await session.transport.handle_request(scope, receive, send)
            return
        await _send_json_response(send, {"error": "Session not found"}, 404)
        return

    elif method == "DELETE":
        if session_id and session_id in streamable_sessions:
            session = streamable_sessions.pop(session_id)
            session.transport.terminate()
            if session.task and not session.task.done():
                session.task.cancel()
                try:
                    await session.task
                except asyncio.CancelledError:
                    pass
            await _send_json_response(send, {"status": "session terminated"}, 200)
            return
        await _send_json_response(send, {"error": "Session not found"}, 404)
        return

    await _send_json_response(send, {"error": "Method not allowed"}, 405)


async def health_check_handler(scope: Scope, receive: Receive, send: Send) -> None:
    """헬스 체크 ASGI 핸들러"""
    await _send_json_response(
        send,
        {
            "status": "ok",
            "service": "pyongyang-naengmyeon-mcp",
            "transports": ["sse", "streamable-http"],
        },
    )


async def sse_handler(scope: Scope, receive: Receive, send: Send) -> None:
    """SSE ASGI 핸들러"""
    server = create_server()
    async with sse.connect_sse(scope, receive, send) as streams:
        await server.run(streams[0], streams[1], server.create_initialization_options())


class MCPApp:
    """SSE + Streamable HTTP를 모두 지원하는 MCP ASGI 앱"""

    def __init__(self) -> None:
        self.sse_message_handler = sse.handle_post_message

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return

        path = scope.get("path", "")

        # 라우팅
        if path in ("/", "/health"):
            await health_check_handler(scope, receive, send)
        elif path == "/mcp":
            await streamable_http_handler(scope, receive, send)
        elif path == "/sse":
            await sse_handler(scope, receive, send)
        elif path.startswith("/messages"):
            await self.sse_message_handler(scope, receive, send)
        else:
            await _send_json_response(send, {"error": "Not found"}, 404)


# ASGI 앱 생성
app = MCPApp()


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)  # type: ignore[arg-type]
