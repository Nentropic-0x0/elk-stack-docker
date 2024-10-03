import os
from fastapi import FastAPI, HTTPException
import uvicorn.logging
from elasticsearch import Elasticsearch
import requests
from logger import logger
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Set up Elasticsearch connection
username = 'elastic'
password = os.getenv('ELASTIC_PASSWORD')  # Ensure this environment variable is set

client = Elasticsearch(
    "elasticsearch:9200",
    basic_auth=(username, password)
)

@app.get("/")
async def hello_elk():
    """
    Simple endpoint that returns 'Hello ELK' and lists the status of Elastic, Logstash, and Kibana.
    """
    try:
        # Check Elasticsearch status
        es_status = client.info()
        
        # Check Logstash status
        logstash_response = requests.get("http://localhost:9600/_node/pipelines", timeout=5)
        logstash_status = logstash_response.json() if logstash_response.status_code == 200 else {"status": "unreachable"}

        # Check Kibana status
        kibana_response = requests.get("http://localhost:5601/api/status", timeout=5)
        kibana_status = kibana_response.json() if kibana_response.status_code == 200 else {"status": "unreachable"}

        return {
            "message": "Hello ELK",
            "elasticsearch": es_status,
            "logstash": logstash_status,
            "kibana": kibana_status
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    print("Uvicorn is running")