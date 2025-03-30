import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve credentials from .env file
# NEO4J_URI = os.getenv("NEO4J_URI")
# NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
# NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

NEO4J_URI="neo4j+s://477ab692.databases.neo4j.io"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="WhhzEl5YGp3gUOjPI4HeHK4k-QmJiYU52_Ax7YSfcYs"


def test_neo4j_connection():
    try:
        # Create a Neo4j driver instance
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        
        # Test the connection
        with driver.session() as session:
            result = session.run("RETURN 'Connection Successful' AS message")
            for record in result:
                print(record["message"])
        
        driver.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_neo4j_connection()
