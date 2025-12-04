import structlog
import time
import uuid
from typing import Any
from litestar.types import ASGIApp, Receive, Scope, Send
from src.config.logger import get_logger


logger = get_logger()

def structlog_middleware_factory(app: ASGIApp) -> ASGIApp:

    async def middleware(scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await app(scope, receive, send)
            return

        trace_id = _extract_trace_id(scope)
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(trace_id=trace_id)

        scope.setdefault("state", {})["trace_id"] = trace_id

        _log_request_start(scope, trace_id, logger)

        start_time = time.perf_counter()
        status_code = 200

        async def send_wrapper(message: dict[str, Any]) -> None:
            nonlocal status_code

            if message["type"] == "http.response.start":
                status_code = message["status"]

                headers = message.get("headers", [])
                message["headers"] = _inject_trace_id(headers, trace_id)

            await send(message)

        try:
            await app(scope, receive, send_wrapper)
            process_time = time.perf_counter() - start_time
            _log_request_end(scope, status_code, process_time, trace_id, logger)

        except Exception as exc:
            process_time = time.perf_counter() - start_time
            _log_request_error(scope, exc, process_time, trace_id, logger)
            raise

        finally:
            structlog.contextvars.clear_contextvars()

    return middleware


def _extract_trace_id(scope: Scope) -> str:
    headers = scope.get("headers", [])
    for header_name, header_value in headers:
        if header_name.decode("latin-1").lower() == "x-request-id":
            return header_value.decode("latin-1")
    return str(uuid.uuid4())

def _inject_trace_id(
        headers: list[tuple[bytes, bytes]],
        trace_id: str
) -> list[tuple[bytes, bytes]]:
    headers = [h for h in headers if h[0] != b"x-trace-id"]
    headers.append((b"x-trace-id", trace_id.encode()))
    return headers

def _log_request_start(scope: Scope, trace_id: str, logger) -> None:
    method = scope["method"]
    path = scope["path"]

    logger.info(
        "request_started",
        trace_id=trace_id,
        method=method,
        path=path,
    )

def _log_request_end(
        scope: Scope,
        status_code: int,
        process_time: float,
        trace_id: str,
        logger
) -> None:
    method = scope["method"]
    path = scope["path"]

    if status_code >= 500:
        log_level = "error"
        event_message = "request_server_error"
    elif status_code >= 400:
        log_level = "warning"
        event_message = "request_client_error"
    else:
        log_level = "info"
        event_message = "request_completed"

    log_data = {
        "event": event_message,
        "trace_id": trace_id,
        "method": method,
        "path": path,
        "status_code": status_code,
        "process_time_ms": round(process_time * 1000, 2),
    }

    if log_level == "error":
        logger.error(**log_data)
    elif log_level == "warning":
        logger.warning(**log_data)
    else:
        logger.info(**log_data)

def _log_request_error(
        scope: Scope,
        exc: Exception,
        process_time: float,
        trace_id: str,
        logger
) -> None:
    method = scope["method"]
    path = scope["path"]

    logger.error(
        "request_failed",
        trace_id=trace_id,
        method=method,
        path=path,
        error_type=type(exc).__name__,
        error_message=str(exc),
        process_time_ms=round(process_time * 1000, 2),
    )