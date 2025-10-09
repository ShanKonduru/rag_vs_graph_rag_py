from neo4j import GraphDatabase

def check_nodes():
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password'))
    try:
        with driver.session(database='neo4j') as session:
            result = session.run('MATCH (n) RETURN count(n) as node_count')
            node_count = result.single()['node_count']
            print(f'Nodes in database: {node_count}')
            
            if node_count > 0:
                # Check what types of nodes exist
                result = session.run('MATCH (n) RETURN DISTINCT labels(n) as labels, count(n) as count')
                print('\nNode types:')
                for record in result:
                    print(f'  {record["labels"]}: {record["count"]}')
            else:
                print('Database is empty - needs knowledge graph population')
    finally:
        driver.close()

if __name__ == "__main__":
    check_nodes()