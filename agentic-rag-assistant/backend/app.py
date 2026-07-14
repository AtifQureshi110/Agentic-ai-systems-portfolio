from fastapi import FastAPI
# Import the FastAPI class — this is the core object used to create 
# and configure your entire web application.

from backend.routes.ingestion import router as ingestion_router
# Import the router object defined in routes/ingestion.py 
# (contains the /ingest endpoint) and rename it to `ingestion_router` 
# for clarity when registering it below.

from backend.routes.query import router as query_router
# Import the router object defined in routes/query.py 
# (contains the /query endpoint) and rename it to `query_router`.

from backend.routes.health import router as health_router
# Import the router object defined in routes/health.py 
# (contains the /health endpoint) and rename it to `health_router`.

app = FastAPI( title="Agentic RAG Assistant API" )
# Create the main FastAPI application instance. 
# The `title` shows up in the auto-generated Swagger docs (/docs) 
# and OpenAPI schema — helps identify the API when viewing documentation.

# Routes
# A comment marking the section where all routers get registered/mounted.

app.include_router( health_router )

# Register the health check routes onto the main app. 
# Now GET /health (or whatever path is defined inside health.py) is live.

app.include_router( ingestion_router )
# Register the ingestion routes onto the main app. 
# Now POST /ingest (or whatever path is defined inside ingestion.py) is live.

app.include_router( query_router )
# Register the query routes onto the main app. 
# Now POST /query (or whatever path is defined inside query.py) is live.

@app.get("/")
# Decorator that binds the function below to a GET request 
# at the root URL path "/".

def root():
# Handler function for the root endpoint — runs whenever someone 
# visits the base URL of the API (e.g., http://localhost:8000/).
    return { "message": "Agentic RAG Assistant API running" }
    # Return a simple JSON response confirming the API is up and running. 
    # Useful as a quick manual check that the server started correctly, 
    # separate from the dedicated /health endpoint.