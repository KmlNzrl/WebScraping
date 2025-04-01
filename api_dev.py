import os
from dotenv import load_dotenv
import psycopg2
from fastapi import FastAPI, HTTPException
from psycopg2.extras import RealDictCursor

load_dotenv()

DB_PARAMS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

app = FastAPI()

# Function to connect to database
def get_db_connection():
    return psycopg2.connect(**DB_PARAMS, cursor_factory=RealDictCursor)

@app.get("/outlets")
def get_outlets():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mcdonalds_outlets;")
        outlets = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"data": outlets}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve outlets")
    
@app.get("/outlets/{outlets_id}")
def get_outlet(outlets_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mcdonalds_outlets WHERE id = %s;", (outlets_id,))
        outlet = cursor.fetchone()
        cursor.close()
        conn.close()
        if outlet:
            return {"data": outlet}
        else:
            raise HTTPException(status_code=404, detail="Outlet not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve outlet")