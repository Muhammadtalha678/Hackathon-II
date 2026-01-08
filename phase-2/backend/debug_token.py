"""
Debug script to test JWT token decoding with the same parameters used in the application.
"""
import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the secret key and algorithm from environment
SECRET_KEY = os.getenv('BETTER_AUTH_SECRET', 'your-super-secret-jwt-key-change-this-in-production')
ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')

def generate_debug_token():
    """Generate a token exactly as the application would expect."""
    payload = {
        "sub": "1",
        "email": "test@example.com",
        "user_id": 1,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(timezone.utc),
        "jti": "debug-token"
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_debug_token(token):
    """Decode a token exactly as the application would."""
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Token decoded successfully!")
        print("Decoded payload:", decoded)
        return decoded
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {str(e)}")
        print(f"Token: {token}")
        # Let's try to manually split the token to see if there's a format issue
        parts = token.split('.')
        print(f"Token parts: {len(parts)}")
        for i, part in enumerate(parts):
            print(f"Part {i}: {part[:50]}... (length: {len(part)})")
        return None

if __name__ == "__main__":
    print("Debugging JWT Token Issues")
    print("=" * 40)
    print(f"SECRET_KEY: {SECRET_KEY[:20]}...")
    print(f"ALGORITHM: {ALGORITHM}")
    print()

    # Test with the token that was generated earlier
    test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJ0ZXN0QGV4YW1wbGUuY29tIiwidXNlcl9pZCI6MSwiZXhwIjoxNzY3ODE0NTgyLCJpYXQiOjE3Njc4MTI3ODIsImp0aSI6InRlc3QtdG9rZW4ifQ.9_YZkbUDFN-MAZMtfyzDqAQqoYn-CnfLs2ScweYVRio"

    print("Testing the previously generated token:")
    decode_debug_token(test_token)
    print()

    # Generate a new token and test it
    print("Generating a new token:")
    new_token = generate_debug_token()
    print(f"New token: {new_token}")
    print()

    print("Testing the new token:")
    decode_debug_token(new_token)
    print()

    # Test with a manual header extraction simulation
    auth_header = f"Bearer {new_token}"
    extracted_token = auth_header[7:]  # Remove "Bearer " prefix
    print(f"After removing 'Bearer ': {extracted_token}")
    print("Testing extracted token:")
    decode_debug_token(extracted_token)