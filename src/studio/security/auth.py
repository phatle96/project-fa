# import os
# import httpx
# from langgraph_sdk import Auth

# auth = Auth()

# # This is loaded from the `.env` file you created above
# FRESH_ALERT_BASE_URL = os.getenv("FRESH_ALERT_BASE_URL", "http://51.79.219.71:3000")

# @auth.authenticate
# async def get_current_user(headers: dict):
#     """Validate JWT tokens and extract user information."""
    
#     freshalert_token = headers.get(b"freshalert-token")
    
#     if not freshalert_token:
#         raise Auth.exceptions.HTTPException(status_code=401, detail="Invalid Token")
    
#     scheme, token = freshalert_token.decode("utf-8").split()
    
#     assert scheme.lower() == "bearer"

#     try:
#         # Verify token with auth provider
#         async with httpx.AsyncClient() as client:
#             response = await client.get(
#                 f"{FRESH_ALERT_BASE_URL}/user/me",
#                 headers={
#                     "authorization": f"Bearer {token}",
#                     "user-agent": "langgraph-agent-auth"
#                 },
#             )
#             assert response.status_code == 200
#             user = response.json()
            
#             return {
#                 "identity": user["sub"],  # Unique user identifier
#                 "email": user["email"],
#                 "name": user["name"],
#                 "freshalert-token": token,
#                 "is_authenticated": True,
#             }
#     except Exception as e:
#         raise Auth.exceptions.HTTPException(status_code=401, detail=str(e))
    


# @auth.on
# async def add_owner(
#     ctx: Auth.types.AuthContext,
#     value: dict  # The payload being sent to this access method
# ) -> dict:  # Returns a filter dict that restricts access to resources
#     """Authorize all access to threads, runs, crons, and assistants.

#     This handler does two things:
#         - Adds a value to resource metadata (to persist with the resource so it can be filtered later)
#         - Returns a filter (to restrict access to existing resources)

#     Args:
#         ctx: Authentication context containing user info, permissions, the path, and
#         value: The request payload sent to the endpoint. For creation
#               operations, this contains the resource parameters. For read
#               operations, this contains the resource being accessed.

#     Returns:
#         A filter dictionary that LangGraph uses to restrict access to resources.
#         See [Filter Operations](#filter-operations) for supported operators.
#     """
#     # Create filter to restrict access to just this user's resources
#     filters = {"owner": ctx.user.identity}

#     # Get or create the metadata dictionary in the payload
#     # This is where we store persistent info about the resource
#     metadata = value.setdefault("metadata", {})

#     # Add owner to metadata - if this is a create or update operation,
#     # this information will be saved with the resource
#     # So we can filter by it later in read operations
#     metadata.update(filters)

#     # Return filters tox restrict access
#     # These filters are applied to ALL operations (create, read, update, search, etc.)
#     # to ensure users can only access their own resources
#     return filters