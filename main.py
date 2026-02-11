from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg2

app = FastAPI()

# CORS for frontend CloudFront
origins = ["https://dev.factfinderspro.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "FastAPI sync from git running!"}

@app.get("/db")
def test_db():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        return {"error": "DATABASE_URL not set"}
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        now = cur.fetchone()
        cur.close()
        conn.close()
        return {"dev db_time": now[0]}
    except Exception as e:
        return {"error": str(e)}
