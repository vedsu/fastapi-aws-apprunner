from fastapi import FastAPI
from pymongo import MongoClient
app = FastAPI(title="My First FastAPI on AWS")
# 🔹 Hardcoded MongoDB connection string
MONGO_URI = "mongodb+srv://Vedsu:CVxB6F2N700cQ0qu@cluster0.thbmwqi.mongodb.net/webinarprof"
# 🔹 Initialize Mongo client
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
