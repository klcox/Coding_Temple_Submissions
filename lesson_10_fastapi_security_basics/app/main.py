# Run with: uvicorn app.main:app --reload 
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
from fastapi.responses import JSONResponse
from app.routers import items


app = FastAPI(title="Security Basics API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[  # Only these domains are allowed to make requests to the API
        "http://localhost:3000"
        "https://yourfrontend.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)


request_counts: dict[str, list[float]] = {}  # Key is IP address as a string; Value is a list of timestamps pertaining to requests made

RATE_LIMIT = 10  # Number of requests
TIME_FRAME = 60.0  # Timeframe (number of seconds) for requests -> 10 requests per minute

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    """Manual rate-limiter. Tracks timestamps of requests and assesses whether the number of requests made by an IP address exceeds the designated rate limit. If so, returns a JSONResponse with an error message (429)."""

    client_ip = request.client.host
    current_time = time.time()

    timestamps = request_counts.get(client_ip, [])
    timestamps = [t for t in timestamps if current_time - t < TIME_FRAME]  # Pull only the timestamps from the last 60 seconds for this IP 

    if len(timestamps) >= RATE_LIMIT:  # If the rate limit has been exceeded, return a JSONResponse with an error message
        return JSONResponse(
            status_code=429,
            content = {
                "error": True,
                "detail": "Too many requests",
                "message": "Rate limit exceeded. Please try again in a moment."
            }
        )

    timestamps.append(current_time)
    request_counts[client_ip] = timestamps  # If the rate limit has not been exceeded, add the timestamp of the most recent request to the log.

    return await call_next(request)


app.include_router(
    items.router,
    prefix = "/items",
    tags = ["Items"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)