from fastapi import FastAPI

app = FastAPI(title="My First FastAPI on AWS")

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on AWS App Runner"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
