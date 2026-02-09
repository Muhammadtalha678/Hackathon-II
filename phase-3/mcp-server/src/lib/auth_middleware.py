import jwt
from typing import Optional
from starlette import status
from fastmcp import FastMCP, Context
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.exceptions import ToolError
from sqlmodel import select
import time
# Assumes src.models.user.User is available
from src.lib.public_key_Ed25519 import load_eddsa_public_key
from src.models.user import User

class AuthMiddleware(Middleware):
    async def on_request(self, context: MiddlewareContext, call_next):
        
        print(f"DEBUG: Middleware running for method: {context.method}")
        # start_time = time.perf_counter()
        # print("Middleware: Pre-processing")
        # """Intercepts requests to verify JWT and set user in scope."""
        # 1. Access the global FastMCP context from the Middleware context
        mcp_ctx = context.fastmcp_context

        # 2. Get the HTTP request context
        req_ctx = mcp_ctx.request_context
        
        if not req_ctx:
            return await call_next(context)

        # 1. Extract and Verify Token
        request = req_ctx.request
        auth_header = request.headers.get("authorization")
        token = auth_header[7:] if auth_header and auth_header.startswith("Bearer ") else request.cookies.get("access_token")
        
        if not token:
            raise ToolError("Authorization token missing")
        try:
            # Note: Implement proper signature verification (e.g., using jwks)
            unverified_header = jwt.get_unverified_header(token)
            # print("unverified_header:", unverified_header)
            kid = unverified_header["kid"]
        except Exception as e:
            raise ToolError(f"Invalid token header: {str(e)}")


        # jwks verfiy
        jwks = mcp_ctx.lifespan_context.get("jwks")
        key = next((k for k in jwks if k["kid"] == kid), None)
        # print(key)
        if not key:
            raise ToolError("Public key for token not found")
        public_key_obj = load_eddsa_public_key(key)
        # print("public_key_obj",public_key_obj)
        # Decode and verify the token
        try:
            decoded_data = jwt.decode(
                token,
                public_key_obj,
                algorithms=[key['alg']],
                issuer= "https://hackathon-ii-eta.vercel.app",
                audience= "https://hackathon-ii-eta.vercel.app"
            )
            email = decoded_data["email"]
            # print(decoded_data)
        except jwt.ExpiredSignatureError:
            raise ToolError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise ToolError(f"Invalid token: {str(e)}")

        # 2. Verify User in DB
        try:
            # print(email)
            db = mcp_ctx.lifespan_context.get("db")
            # print(db)
            with next(db.get_session()) as session:
                user = session.exec(select(User).where(User.email == email)).first()
                if not user:
                    raise ToolError("User not found")
                req_ctx.request.state.user = user
        except Exception as e:
            raise ToolError(f"Database error: {str(e)}")
        response  = await call_next(context)
        # Back in middleware after tool finished
        # duration = time.perf_counter() - start_time
        # print(f"Middleware: Tool took {duration:.4f} seconds")
        print("response",response)
        return response


# Helper to get current user in Tools
def get_current_user(ctx: Context) -> User:
    user = ctx.request_context.scope.get("current_user")
    if not user:
        raise ToolError("Not authenticated")
    return user
