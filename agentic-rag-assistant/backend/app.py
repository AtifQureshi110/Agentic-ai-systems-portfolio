from fastapi import FastAPI
from backend.routes.ingestion import router as ingestion_router
from backend.routes.query import router as query_router
from backend.routes.health import router as health_router

app = FastAPI( title="Agentic RAG Assistant API" )

# Routes
app.include_router( health_router )
app.include_router( ingestion_router )
app.include_router( query_router )

@app.get("/")
def root():
    return { "message": "Agentic RAG Assistant API running" }