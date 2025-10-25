# backend/app/core/security.py
import secrets
import hashlib
import hmac
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from .config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token handling
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.session_timeout)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    
    return encoded_jwt

def verify_token(token: str) -> Dict[str, Any]:
    """Verify a JWT token"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def generate_session_token() -> str:
    """Generate a secure session token"""
    return secrets.token_urlsafe(32)

def validate_file_upload(file_content: bytes, filename: str) -> bool:
    """Validate uploaded file content"""
    # Check file size (max 10MB)
    if len(file_content) > 10 * 1024 * 1024:
        return False
    
    # Check file extension
    allowed_extensions = {'.txt', '.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.gif'}
    file_extension = '.' + filename.split('.')[-1].lower() if '.' in filename else ''
    
    if file_extension not in allowed_extensions:
        return False
    
    # Check file content for malicious patterns
    malicious_patterns = [
        b'<script',
        b'javascript:',
        b'vbscript:',
        b'onload=',
        b'onerror=',
        b'eval(',
        b'exec('
    ]
    
    content_lower = file_content.lower()
    for pattern in malicious_patterns:
        if pattern in content_lower:
            return False
    
    return True

def sanitize_input(input_string: str) -> str:
    """Sanitize user input"""
    if not input_string:
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', '\x00', '\n', '\r', '\t']
    for char in dangerous_chars:
        input_string = input_string.replace(char, '')
    
    # Limit length
    max_length = 10000
    if len(input_string) > max_length:
        input_string = input_string[:max_length]
    
    return input_string.strip()

def create_api_key() -> str:
    """Create a new API key"""
    return secrets.token_urlsafe(32)

def verify_api_key(api_key: str, stored_hash: str) -> bool:
    """Verify an API key against its stored hash"""
    return hmac.compare_digest(
        hashlib.sha256(api_key.encode()).hexdigest(),
        stored_hash
    )

class RateLimiter:
    """Simple rate limiter implementation"""
    
    def __init__(self):
        self.requests: Dict[str, list] = {}
    
    def is_allowed(self, key: str, limit: int, window: int) -> bool:
        """Check if a request is allowed based on rate limit"""
        now = datetime.utcnow()
        
        if key not in self.requests:
            self.requests[key] = []
        
        # Remove old requests outside the window
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if (now - req_time).total_seconds() < window
        ]
        
        # Check if under limit
        if len(self.requests[key]) < limit:
            self.requests[key].append(now)
            return True
        
        return False

# Global rate limiter instance
rate_limiter = RateLimiter()

async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware"""
    # Get client IP
    client_ip = request.client.host if request.client else "unknown"
    
    # Define rate limits (requests per minute)
    rate_limits = {
        "/chat/sessions": 5,  # 5 session creations per minute
        "/chat/sessions/": 30,  # 30 messages per minute
        "/health/": 60,  # 60 health checks per minute
    }
    
    # Check rate limit for this endpoint
    path = request.url.path
    for pattern, limit in rate_limits.items():
        if path.startswith(pattern):
            if not rate_limiter.is_allowed(client_ip, limit, 60):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded"
                )
            break
    
    response = await call_next(request)
    return response
