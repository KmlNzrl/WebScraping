import psycopg2
from psycopg2 import OperationalError

def test_postgresql_connection():
    try:
        # Replace with your actual database credentials
        connection = psycopg2.connect(
            dbname="Scraping",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        
        print("Connection to PostgreSQL successful!")
        connection.close()
    except OperationalError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_postgresql_connection()
