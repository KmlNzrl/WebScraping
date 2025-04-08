import os
from dotenv import load_dotenv
import psycopg2
from fastapi import FastAPI, HTTPException, Query
from psycopg2.extras import RealDictCursor
from geopy.distance import geodesic

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
    
@app.get("/outlets/search/id")
def get_outlet(outlets_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mcdonalds_outlets WHERE id = %s;", (outlets_id,))
        outlets = cursor.fetchone()
        cursor.close()
        conn.close()
        if outlets:
            return {"data": outlets}
        else:
            raise HTTPException(status_code=404, detail="Outlet not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve outlet")
    
@app.get("/outlets/search/name")
def search_outlets(name: str = Query(..., description="Name of the outlet:")):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mcdonalds_outlets WHERE name ILIKE %s;", (f"%{name}%",))
        outlets = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"data": outlets}
    except Exception as e:
        raise HTTPException (status_code=500, detail=str(e))
    
# @app.get("/outlets/search/nearest")
# def search_nearest(lat: float = Query(...), lon: float = Query(...)):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM mcdonalds_outlets WHERE latitude IS NOT NULL AND longitude IS NOT NULL;")
#         outlets = cursor.fetchall()
#         cursor.close()
#         conn.close()

#         if not outlets:
#             raise HTTPException (status_code=404, detail="No outlets found")
        
#         nearest_outlet = min(outlets, key=lambda outlet:geodesic((lat, lon), float((outlet["latitude"]), float(outlet["longitude"]))).km)
#         return {"data", nearest_outlet}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.get("/outlets/with-geolocation")
def get_outlets_with_geolocation():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mcdonalds_outlets WHERE geolocation IS NOT NULL;")
        outlets = cursor.fetchall()
        cursor.close()
        conn.close()
        return{"data": outlets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))