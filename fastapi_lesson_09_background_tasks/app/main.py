# Run with: uvicorn app.main:app --reload

from fastapi import FastAPI
from app.routers import reports


app = FastAPI(title="Background Tasks Demo")

app.include_router(
    reports.router,
    prefix = "/reports",
    tags = ["Reports"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)