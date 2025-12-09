from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import game_routes

app = FastAPI(
    title="Fantasy Inn Tycoon API",
    description="Backend API for the Fantasy Inn management game",
    version="1.0.0"
)

# CORS configuration for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular default dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(game_routes.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Fantasy Inn Tycoon API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
