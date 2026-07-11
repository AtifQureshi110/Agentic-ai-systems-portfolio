import requests

BACKEND_URL = "http://localhost:8000"

def check_source(source):
    response = requests.post(f"{BACKEND_URL}/ingest/check-source",
        json={"source": source} )

    return response.json()

def ingest_source(source, force_update=False):
    response = requests.post(
        f"{BACKEND_URL}/ingest",
        json={ "source": source, "force_update": force_update } )

    return response.json() 

def ask_ai(question: str):
    response = requests.post( f"{BACKEND_URL}/query",
        json={ "question": question } )
    response.raise_for_status()
    return response.json()