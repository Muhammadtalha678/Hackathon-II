from dataclasses import dataclass
from src.models.user import User

@dataclass
class AuthContext:
    user: User
    token: str
