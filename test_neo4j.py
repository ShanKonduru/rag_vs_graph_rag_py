#!/usr/bin/env python3
"""Test Neo4j connection and list databases"""

from neo4j import GraphDatabase

def test_neo4j():
    try:
        driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'LocalInstance'))
        
        # Test connection
        driver.verify_connectivity()
        print("✅ Neo4j connection successful!")
        
        # List databases
        records, _, _ = driver.execute_query('SHOW DATABASES')
        print("\nAvailable databases:")
        for record in records:
            print(f"  - {record['name']}")
        
        driver.close()
        
    except Exception as e:
        print(f"❌ Neo4j connection failed: {e}")

if __name__ == "__main__":
    test_neo4j()