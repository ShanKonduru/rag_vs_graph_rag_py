#!/usr/bin/env python3
"""Check Neo4j database content"""

from neo4j import GraphDatabase

def check_neo4j_data():
    try:
        driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'LocalInstance'))
        
        # Check total nodes
        records, _, _ = driver.execute_query('MATCH (n) RETURN count(n) as total')
        total_nodes = records[0]['total']
        print(f"Total nodes in Neo4j: {total_nodes}")
        
        # Check labels
        records, _, _ = driver.execute_query('CALL db.labels()')
        labels = [record['label'] for record in records]
        print(f"Node labels: {labels}")
        
        driver.close()
        
    except Exception as e:
        print(f"❌ Neo4j check failed: {e}")

if __name__ == "__main__":
    check_neo4j_data()