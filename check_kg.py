#!/usr/bin/env python3
"""
Check Knowledge Graph Contents
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.rag_system.knowledge_graph.neo4j_graph import Neo4jKnowledgeGraph

def main():
    print('🔍 Checking Knowledge Graph entities...')
    
    # Initialize Neo4j knowledge graph directly
    kg = Neo4jKnowledgeGraph()
    
    try:
        # Get basic statistics
        stats = kg.get_statistics()
        print(f'📈 Total entities in knowledge graph: {stats["total_entities"]}')
        print(f'📈 Total relations: {stats["total_relations"]}')
        print(f'� Entity types: {stats["entity_types"]}')
        
        if stats["total_entities"] > 0:
            # Get some sample entities using direct query
            print('\n📊 Sample entities:')
            result = kg.query("MATCH (e:Entity) RETURN e.text, e.type LIMIT 10")
            
            # Try to extract entity info from the query result
            sample_query = "MATCH (e:Entity) RETURN e.text as text, e.type as type LIMIT 10"
            with kg.driver.session(database=kg.database) as session:
                result = session.run(sample_query)
                for i, record in enumerate(result, 1):
                    text = record.get('text', 'Unknown')
                    entity_type = record.get('type', 'Unknown')
                    print(f'  {i}. {text} (type: {entity_type})')
            
        else:
            print('❌ Knowledge graph is empty!')
            return
            
        # Test entity search with sample queries
        print('\n🔍 Testing entity search...')
        test_queries = [
            "CTO",
            "Chief Technology Officer", 
            "digital transformation",
            "leadership",
            "technology",
            "AI",
            "quality",
            "team",
            "management",
            "software"
        ]
        
        for query in test_queries:
            try:
                entities = kg.get_entities_by_text(query)
                print(f'  Query: "{query}" -> {len(entities)} entities found')
                if entities:
                    for entity in entities[:3]:
                        print(f'    - {entity.text} (type: {entity.type})')
            except Exception as e:
                print(f'    Error searching for "{query}": {e}')
        
        # Test with partial matches
        print('\n🔍 Testing partial word matches...')
        partial_terms = ["tech", "lead", "manage", "qual", "digit"]
        
        for term in partial_terms:
            try:
                entities = kg.get_entities_by_text(term)
                print(f'  Partial: "{term}" -> {len(entities)} entities found')
                if entities:
                    for entity in entities[:2]:
                        print(f'    - {entity.text}')
            except Exception as e:
                print(f'    Error with partial "{term}": {e}')
        
    except Exception as e:
        print(f'❌ Error accessing knowledge graph: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()