from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException
from contextvars import ContextVar
import typing as t

# ContextVar holds per-request token accessible anywhere during request handling
token_var: ContextVar[t.Optional[str]] = ContextVar("bearer_token", default=None)
# Optionally store decoded user info
# user_var: ContextVar[t.Optional[dict]] = ContextVar("user_info", default=None)


class BearerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        Extract Authorization header, store token (and optionally decoded user)
        in ContextVars so tool functions can access them without changing signatures.
        """
        auth = request.headers.get("authorization")  # case-insensitive
        if not auth:
            # Block or allow — here we block with 401. Change logic if some endpoints should be public.
            raise HTTPException(status_code=401, detail="Missing Authorization header")
        if not auth.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid Authorization scheme")
        token = auth.split(" ", 1)[1].strip()
        # Save token to context var for downstream handlers (tools) to read
        token_var.set(token)

        # Optional: decode token here (e.g. JWT decode) and set user_var
        # try:
        #     payload = decode_jwt(token)   # implement decode_jwt if using JWTs
        #     user_var.set(payload)
        # except Exception:
        #     raise HTTPException(status_code=401, detail="Invalid token")

        response = await call_next(request)
        return response

# Register middleware on the FastMCP (FastAPI) app
# mcp.add_middleware(BearerMiddleware)

# ---------- helper utilities ----------

def get_bearer_token() -> t.Optional[str]:
    """Read token set in middleware; returns None if not present."""
    return token_var.get()

def require_token(func):
    """
    Decorator for tools: ensures a token exists (set by middleware).
    Raises HTTPException(401) if not present.
    """
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = get_bearer_token()
        if not token:
            # If tools are invoked outside of HTTP context (e.g., tests), token may be None.
            raise HTTPException(status_code=401, detail="Authentication required")
        # Optionally: perform extra validation here (call introspection endpoint, check blacklist, etc.)
        return func(*args, **kwargs)
    return wrapper
