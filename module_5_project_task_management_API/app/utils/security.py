from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timezone, timedelta
from app.config import settings 
from jose import jwt, JWTError
from fastapi import Security, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.exceptions import UnauthorizedException, ForbiddenException
from app.models.user import User


pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

http_bearer = HTTPBearer()


def hash_password(password: str):
    """Returns a hashed version of the plain-text password."""

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """Compares the plain-text password provided against the hashed password. Returns True if there is a match or False if there is no match."""

    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    """Creates a JWT with an expiration date/time. Returns the JWT as a string."""

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)  # Sets expiration date/time

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str):
    """Decodes and validates a JWT. Returns a dictionary containing the subject and token expiration if successful; otherwise, returns None."""

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    except JWTError:
        return None

    return payload


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(http_bearer),  # HTTPBearer handles missing token scenario
    db: Session = Depends(get_db)
):
    """Extracts and validates a JWT. Returns the authenticated user if successful."""

    token = credentials.credentials

    payload = decode_access_token(token)

    if payload is None:  # Token invalid or expired
        raise UnauthorizedException("Invalid or expired token")    

    username = payload.get("sub")
    if username is None:  # Token is valid but has no associated username
        raise UnauthorizedException("Invalid token")   

    user = db.query(User).filter(User.username == username).first()
    if user is None:  # Token is valid, but user is not in the database
        raise UnauthorizedException("Invalid token. User not found.")

    if not user.is_active:  # Token is valid, but user is deactivated
        raise ForbiddenException("Cannot proceed. This account has been deactivated. Please contact admin or support.")

    return user


def verify_admin_status(user: User = Depends(get_current_user)):   
    """After a user is authenticated, verifies admin status. If verified, returns the authenticated user.""" 

    if not user.is_admin:
        raise ForbiddenException()  # Uses default error message outlined in the exception

    return user