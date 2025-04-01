import psycopg2
from psycopg2 import OperationalError
import os
from dotenv import load_dotenv

load_dotenv()

def test_postgresql_connection():
    try:
        # Replace with your actual database credentials
        connection = psycopg2.connect(
            dbname = os.getenv('DB_NAME'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            host = os.getenv('DB_HOST'),
            port = os.getenv('DB_PORT')
        )
        
        print("Connection to PostgreSQL successful!")
        connection.close()
    except OperationalError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_postgresql_connection()
