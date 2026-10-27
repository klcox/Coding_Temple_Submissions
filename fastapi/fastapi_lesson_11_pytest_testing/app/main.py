# exercises/test-suite/app/main.py
# L11 — Task API (already complete — your job is to write the tests)

from fastapi import FastAPI
from app.database import Base, engine
from app.routers import tasks

app = FastAPI(title="Task API")

Base.metadata.create_all(bind=engine)
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
