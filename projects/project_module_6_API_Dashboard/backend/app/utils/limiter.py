from slowapi import Limiter
from slowapi.util import get_remote_address


limiter = Limiter(key_func=get_remote_address)  # Establishes rate limiter. Limits are set in router endpoints