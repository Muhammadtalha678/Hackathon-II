from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import base64

def load_eddsa_public_key(jwk):
    """
    jwk is the dict from your JWKS.
    """
    if jwk['kty'] != 'OKP' or jwk['crv'] != 'Ed25519':
        raise ValueError("JWK is not Ed25519")

    # Ed25519 public key is the 'x' parameter (base64url)
    x_b64 = jwk['x']
    # Decode base64url
    x_bytes = base64.urlsafe_b64decode(x_b64 + "==")  # Pad if needed

    # Create Ed25519 public key
    public_key = ed25519.Ed25519PublicKey.from_public_bytes(x_bytes)
    return public_key
