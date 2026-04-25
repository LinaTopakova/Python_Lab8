import sys
import uuid
import json
import datetime
from loguru import logger
from app.config import settings
from fastapi import Request

SENSITIVE_HEADERS = {"authorization", "cookie", "set-cookie", "x-api-key", "x-auth-token"}
SENSITIVE_BODY_FIELDS = {"password", "token", "refresh_token", "secret", "old_password", "new_password"}


def mask_sensitive_data(data: dict, mask: str = "***") -> dict:
    if not isinstance(data, dict):
        return data
    result = {}
    for key, value in data.items():
        key_lower = key.lower()
        if key_lower in SENSITIVE_BODY_FIELDS:
            result[key] = mask
        elif isinstance(value, dict):
            result[key] = mask_sensitive_data(value, mask)
        elif isinstance(value, list):
            result[key] = [mask_sensitive_data(v, mask) if isinstance(v, dict) else v for v in value]
        else:
            result[key] = value
    return result


def mask_headers(headers: dict) -> dict:
    masked = {}
    for key, value in headers.items():
        key_lower = key.lower()
        if key_lower in SENSITIVE_HEADERS:
            masked[key] = "***"
        else:
            masked[key] = value
    return masked


def setup_logging():
    logger.remove()
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name} | {message}",
        level=settings.log_level,
        colorize=True
    )

    # Комбинированная ротация: ежедневно или при превышении 10 МБ
    last_rotation_date = datetime.date.today()

    def rotation_func(msg, file):
        nonlocal last_rotation_date
        today = datetime.date.today()
        if today != last_rotation_date:
            last_rotation_date = today
            return True
        if file.tell() + len(msg) > 10 * 1024 * 1024:
            return True
        return False

    logger.add(
        settings.log_file,
        rotation=rotation_func,
        retention="7 days",
        compression="gz",
        serialize=True,
        level="ERROR",
        enqueue=True
    )


setup_logging()


async def get_request_body(request: Request, max_bytes: int = 2048) -> str:
    try:
        body = await request.body()
        if len(body) > max_bytes:
            return f"[TRUNCATED] {body[:max_bytes].decode('utf-8', errors='replace')}... (total {len(body)} bytes)"
        return body.decode('utf-8', errors='replace')
    except Exception:
        return "[UNABLE TO READ BODY]"


async def log_error(request: Request, exc: Exception, status_code: int, request_id: str = None):
    if request_id is None:
        request_id = getattr(request.state, "request_id", None)
    if request_id is None:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

    try:
        method = request.method
        url = str(request.url)
        client_host = request.client.host if request.client else None
        client_port = request.client.port if request.client else None
        headers = mask_headers(dict(request.headers))
        query_params = dict(request.query_params)
        path_params = dict(request.path_params)
        cookies = dict(request.cookies) if request.cookies else {}
        body = None
        if method in ("POST", "PUT", "PATCH"):
            body = await get_request_body(request)
            if body and not body.startswith("[TRUNCATED]") and not body.startswith("[UNABLE"):
                try:
                    body_json = json.loads(body)
                    body_masked = mask_sensitive_data(body_json)
                    body = json.dumps(body_masked, ensure_ascii=False)
                except:
                    pass
    except Exception as e:
        method = url = client_host = client_port = headers = query_params = path_params = cookies = body = None
        logger.error(f"Failed to extract request context: {e}")

    logger.bind(
        request_id=request_id,
        method=method,
        path=url,
        client_host=client_host,
        client_port=client_port,
        query_params=query_params,
        path_params=path_params,
        headers=headers,
        cookies=cookies,
        body=body,
        content_type=request.headers.get("content-type") if request.headers else None,
        status_code=status_code,
        error_type=type(exc).__name__,
        error_message=str(exc)
    ).opt(exception=exc).error("Request error")
