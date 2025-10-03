from neo4j import GraphDatabase
import logging
from typing import List, Dict, Any, Optional

from .base import (
    Entity, Relation, EntityType, KnowledgeGraph, 
    GraphNode, GraphEdge, GraphPath, GraphQueryResult
)


logger = logging.getLogger(__name__)


class Neo4jKnowledgeGraph(KnowledgeGraph):
    """Neo4j implementation of knowledge graph"""
    
    def __init__(self, uri: str, username: str, password: str, database: str = "neo4j"):
        self.uri = uri
        self.username = username  
        self.password = password
        self.database = database
        
        try:
            self.driver = GraphDatabase.driver(uri, auth=(username, password))
            # Test connection
            with self.driver.session(database=database) as session:
                session.run("RETURN 1")
            logger.info(f"Connected to Neo4j at {uri}")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.driver:
            self.driver.close()
    
    def add_entities(self, entities: List[Entity]) -> None:
        """Add entities to the knowledge graph"""
        with self.driver.session(database=self.database) as session:
            for entity in entities:
                # Flatten properties to primitive types only
                flattened_props = {}
                for key, value in entity.properties.items():
                    if isinstance(value, (str, int, float, bool)):
                        flattened_props[f"prop_{key}"] = value
                    else:
                        # Convert complex types to strings
                        flattened_props[f"prop_{key}"] = str(value)
                
                session.run("""
                    MERGE (e:Entity {id: $id})
                    SET e.text = $text,
                        e.type = $type,
                        e.source_chunk_id = $source_chunk_id,
                        e.confidence = $confidence
                """, {
                    "id": entity.id,
                    "text": entity.text,
                    "type": entity.type.value,
                    "source_chunk_id": entity.source_chunk_id,
                    "confidence": entity.confidence
                })
                
                # Add flattened properties as separate SET operations
                if flattened_props:
                    prop_sets = ", ".join([f"e.{key} = ${key}" for key in flattened_props.keys()])
                    query = f"MATCH (e:Entity {{id: $id}}) SET {prop_sets}"
                    params = {"id": entity.id, **flattened_props}
                    session.run(query, params)
        
        logger.info(f"Added {len(entities)} entities to Neo4j")
    
    def add_relations(self, relations: List[Relation]) -> None:
        """Add relations to the knowledge graph"""
        with self.driver.session(database=self.database) as session:
            for relation in relations:
                # Flatten properties to primitive types only
                flattened_props = {}
                for key, value in relation.properties.items():
                    if isinstance(value, (str, int, float, bool)):
                        flattened_props[f"prop_{key}"] = value
                    else:
                        # Convert complex types to strings
                        flattened_props[f"prop_{key}"] = str(value)
                
                session.run("""
                    MATCH (s:Entity {id: $subject_id})
                    MATCH (o:Entity {id: $object_id})
                    MERGE (s)-[r:RELATED {
                        id: $id,
                        predicate: $predicate
                    }]->(o)
                    SET r.source_chunk_id = $source_chunk_id,
                        r.confidence = $confidence
                    RETURN r
                """, {
                    "id": relation.id,
                    "subject_id": relation.subject_id,
                    "object_id": relation.object_id,
                    "predicate": relation.predicate,
                    "source_chunk_id": relation.source_chunk_id,
                    "confidence": relation.confidence
                })
                
                # Add flattened properties as separate SET operations
                if flattened_props:
                    prop_sets = ", ".join([f"r.{key} = ${key}" for key in flattened_props.keys()])
                    query = f"MATCH ()-[r:RELATED {{id: $id}}]-() SET {prop_sets}"
                    params = {"id": relation.id, **flattened_props}
                    session.run(query, params)
        
        logger.info(f"Added {len(relations)} relations to Neo4j")
    
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get an entity by ID"""
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (e:Entity {id: $entity_id})
                RETURN e
            """, {"entity_id": entity_id})
            
            record = result.single()
            if record:
                node = record["e"]
                return Entity(
                    id=node["id"],
                    text=node["text"],
                    type=EntityType(node["type"]),
                    properties=node.get("properties", {}),
                    source_chunk_id=node["source_chunk_id"],
                    confidence=node.get("confidence", 1.0)
                )
            return None
    
    def get_entities_by_text(self, text: str) -> List[Entity]:
        """Get entities by their text representation"""
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (e:Entity)
                WHERE toLower(e.text) CONTAINS toLower($text)
                RETURN e
            """, {"text": text})
            
            entities = []
            for record in result:
                node = record["e"]
                entities.append(Entity(
                    id=node["id"],
                    text=node["text"],
                    type=EntityType(node["type"]),
                    properties=node.get("properties", {}),
                    source_chunk_id=node["source_chunk_id"],
                    confidence=node.get("confidence", 1.0)
                ))
            
            return entities
    
    def get_relations_for_entity(self, entity_id: str) -> List[Relation]:
        """Get all relations involving an entity"""
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (e1:Entity {id: $entity_id})-[r:RELATED]-(e2:Entity)
                RETURN r, e1.id AS subject_id, e2.id AS object_id
            """, {"entity_id": entity_id})
            
            relations = []
            for record in result:
                rel = record["r"]
                relations.append(Relation(
                    id=rel["id"],
                    subject_id=record["subject_id"],
                    predicate=rel["predicate"],
                    object_id=record["object_id"],
                    properties=rel.get("properties", {}),
                    source_chunk_id=rel["source_chunk_id"],
                    confidence=rel.get("confidence", 1.0)
                ))
            
            return relations
    
    def find_path(
        self, 
        start_entity_id: str, 
        end_entity_id: str, 
        max_depth: int = 3
    ) -> List[GraphPath]:
        """Find paths between two entities"""
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH path = (start:Entity {id: $start_id})-[*1..$max_depth]-(end:Entity {id: $end_id})
                RETURN path
                LIMIT 10
            """, {
                "start_id": start_entity_id,
                "end_id": end_entity_id,
                "max_depth": max_depth
            })
            
            paths = []
            for record in result:
                path = record["path"]
                nodes = []
                edges = []
                
                # Extract nodes
                for node in path.nodes:
                    graph_node = GraphNode(
                        id=node["id"],
                        label=node["text"],
                        properties=node.get("properties", {}),
                        entity_type=EntityType(node["type"])
                    )
                    nodes.append(graph_node)
                
                # Extract edges
                for rel in path.relationships:
                    graph_edge = GraphEdge(
                        id=rel["id"],
                        source_id=rel.start_node["id"],
                        target_id=rel.end_node["id"],
                        relationship=rel["predicate"],
                        properties=rel.get("properties", {})
                    )
                    edges.append(graph_edge)
                
                paths.append(GraphPath(
                    nodes=nodes,
                    edges=edges,
                    total_weight=len(edges)
                ))
            
            return paths
    
    def get_subgraph(
        self, 
        entity_ids: List[str], 
        depth: int = 1
    ) -> GraphQueryResult:
        """Get subgraph around specified entities"""
        with self.driver.session(database=self.database) as session:
            # Build the query with the depth parameter directly embedded
            # since Neo4j doesn't allow parameter substitution in variable patterns
            query = f"""
                MATCH (e:Entity) 
                WHERE e.id IN $entity_ids
                OPTIONAL MATCH (e)-[r:RELATED*1..{depth}]-(connected:Entity)
                RETURN e, r, connected
            """
            
            result = session.run(query, {
                "entity_ids": entity_ids
            })
            
            nodes = {}
            edges = {}
            paths = []
            
            for record in result:
                # Process main entity
                entity_node = record["e"]
                node_id = entity_node["id"]
                if node_id not in nodes:
                    nodes[node_id] = GraphNode(
                        id=node_id,
                        label=entity_node["text"],
                        properties=entity_node.get("properties", {}),
                        entity_type=EntityType(entity_node["type"])
                    )
                
                # Process connected entities and relationships
                if record["r"] and record["connected"]:
                    connected_node = record["connected"]
                    connected_id = connected_node["id"]
                    
                    if connected_id not in nodes:
                        nodes[connected_id] = GraphNode(
                            id=connected_id,
                            label=connected_node["text"],
                            properties=connected_node.get("properties", {}),
                            entity_type=EntityType(connected_node["type"])
                        )
                    
                    # Process relationships in the path
                    relationships = record["r"]
                    if not isinstance(relationships, list):
                        relationships = [relationships]
                    
                    for rel in relationships:
                        edge_id = rel["id"]
                        if edge_id not in edges:
                            edges[edge_id] = GraphEdge(
                                id=edge_id,
                                source_id=rel.start_node["id"],
                                target_id=rel.end_node["id"],
                                relationship=rel["predicate"],
                                properties=rel.get("properties", {})
                            )
            
            return GraphQueryResult(
                nodes=list(nodes.values()),
                edges=list(edges.values()),
                paths=paths,
                metadata={
                    "num_nodes": len(nodes),
                    "num_edges": len(edges),
                    "query_entity_ids": entity_ids,
                    "depth": depth
                }
            )
    
    def query(self, query: str) -> GraphQueryResult:
        """Execute a Cypher query"""
        with self.driver.session(database=self.database) as session:
            result = session.run(query)
            
            nodes = []
            edges = []
            
            for record in result:
                for key, value in record.items():
                    if hasattr(value, 'labels'):  # It's a node
                        nodes.append(GraphNode(
                            id=value.get("id", str(value.id)),
                            label=value.get("text", str(value.id)),
                            properties=dict(value),
                            entity_type=EntityType.OTHER
                        ))
                    elif hasattr(value, 'type'):  # It's a relationship
                        edges.append(GraphEdge(
                            id=value.get("id", str(value.id)),
                            source_id=str(value.start_node.id),
                            target_id=str(value.end_node.id),
                            relationship=value.type,
                            properties=dict(value)
                        ))
            
            return GraphQueryResult(
                nodes=nodes,
                edges=edges,
                paths=[],
                metadata={"custom_query": True}
            )
    
    def clear(self) -> None:
        """Clear all data from the knowledge graph"""
        with self.driver.session(database=self.database) as session:
            session.run("MATCH (n) DETACH DELETE n")
        logger.info("Cleared Neo4j knowledge graph")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics"""
        with self.driver.session(database=self.database) as session:
            # Count nodes
            node_result = session.run("MATCH (n:Entity) RETURN count(n) AS count")
            node_count = node_result.single()["count"]
            
            # Count relationships
            rel_result = session.run("MATCH ()-[r:RELATED]->() RETURN count(r) AS count")
            rel_count = rel_result.single()["count"]
            
            # Count by entity type
            type_result = session.run("""
                MATCH (n:Entity) 
                RETURN n.type AS type, count(n) AS count
            """)
            type_counts = {record["type"]: record["count"] for record in type_result}
            
            return {
                "total_entities": node_count,
                "total_relations": rel_count,
                "entity_types": type_counts,
                "database": self.database
            }