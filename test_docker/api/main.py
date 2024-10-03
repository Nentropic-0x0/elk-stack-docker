from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any
import os
import logging

app = FastAPI()

# Elasticsearch configuration
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "elasticsearch")
ELASTICSEARCH_PORT = os.getenv("ELASTICSEARCH_PORT", "9200")

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Elasticsearch client
es = Elasticsearch(
    [f"http://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}"],
    basic_auth=("elastic", ELASTIC_PASSWORD)
    print("connected to ES via Docker")
)

class Document(BaseModel):
    index: str
    doc_type: str
    body: Dict[str, Any]

class SearchQuery(BaseModel):
    index: str
    query: Dict[str, Any]

@app.get("/")
async def root():
    return {"message": "Welcome to the ELK Stack API"}

@app.get("/health")
async def health_check():
    try:
        if es.ping():
            return {"status": "healthy", "elasticsearch": "connected"}
        else:
            logger.error("Elasticsearch ping failed")
            raise HTTPException(status_code=503, detail="Elasticsearch is not available")
    except Exception as e:
        logger.exception("Error connecting to Elasticsearch")
        raise HTTPException(status_code=503, detail=f"Error connecting to Elasticsearch: {str(e)}")

@app.post("/index")
async def index_document(document: Document):
    try:
        response = es.index(index=document.index, doc_type=document.doc_type, body=document.body)
        return {"message": "Document indexed successfully", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search_documents(search_query: SearchQuery):
    try:
        response = es.search(index=search_query.index, body=search_query.query)
        return {"results": response['hits']['hits']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/indices")
async def list_indices():
    try:
        indices = es.indices.get_alias().keys()
        return {"indices": list(indices)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    logger.info("Uvicorn is running")
    

