from fastapi import FastAPI
from pymongo import MongoClient
import boto3
import json
app = FastAPI(title="My First FastAPI on AWS")
def get_mongo_uri():
    secret_name = "pharmaprofsbackend"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name
    )

    response = client.get_secret_value(SecretId=secret_name)
    secret_data = json.loads(response["SecretString"])

    return secret_data["CONNECTION_STRING"]
# 🔹 Initialize Mongo client
MONGO_URI = get_mongo_uri()
client = MongoClient(MONGO_URI)
db = client["webinarprof"]
collection = db["webinar_data"]
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on AWS App Runner"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# 🔥 New endpoint to fetch webinars
@app.get("/webinars")
def get_webinars():
    try:
        webinars = list(collection.find({}, {"_id": 0}))
        return {
            "status": "success",
            "count": len(webinars),
            "data": webinars
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
@app.get("/routes-check")
def routes_check():
    return {
        "routes": ["/", "/health", "/webinars"]
    }
