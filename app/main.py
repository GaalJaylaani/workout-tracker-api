from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api.v1 import auth, users, exercises

# MVP: auto-create tables (later switch to Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Workout Tracker API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(exercises.router)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
