"""
Script to generate a test JWT token for API testing.

This script generates a JWT token that can be used to test the API endpoints.
"""
import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the secret key from environment or use default
SECRET_KEY = os.getenv('BETTER_AUTH_SECRET', 'your-super-secret-jwt-key-change-this-in-production')
ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
EXPIRES_MINUTES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '30'))

def generate_test_token(user_id: int = 1, email: str = "test@example.com"):
    """
    Generate a test JWT token with default user data.

    Args:
        user_id: User ID to include in the token
        email: Email to include in the token

    Returns:
        str: Encoded JWT token
    """
    # Create payload with claims
    payload = {
        "sub": str(user_id),  # subject (user ID)
        "email": email,       # email address
        "user_id": user_id,   # user ID
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRES_MINUTES),  # expiration
        "iat": datetime.now(timezone.utc),  # issued at
        "jti": "test-token"   # JWT ID (for testing)
    }

    # Encode the token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

if __name__ == "__main__":
    print("JWT Token Generator for Testing")
    print("=" * 40)
    print(f"Using SECRET_KEY: {SECRET_KEY[:20]}..." if len(SECRET_KEY) > 20 else f"Using SECRET_KEY: {SECRET_KEY}")
    print(f"Algorithm: {ALGORITHM}")
    print(f"Expires in: {EXPIRES_MINUTES} minutes")
    print()

    # Generate token with default values
    token = generate_test_token()
    print(f"Generated JWT Token:")
    print(token)
    print()

    print("Example usage for API calls:")
    print(f"Authorization: Bearer {token}")
    print()

    # Decode and show token contents (without verification to avoid expiration issues)
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})
        print("Token payload (decoded):")
        for key, value in decoded_payload.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Could not decode token payload: {e}")

    print()
    print("To use this token in API calls:")
    print("- Add header: Authorization: Bearer <token>")
    print("- Or use as cookie: access_token=<token>")