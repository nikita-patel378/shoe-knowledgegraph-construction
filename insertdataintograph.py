import json
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

# Neo4j connection details from your docker-compose
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

class Neo4jIngestion:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def create_constraints(self):
        """Create uniqueness constraints and indexes"""
        with self.driver.session() as session:
            # Constraints for unique IDs
            session.run("CREATE CONSTRAINT research_paper_id IF NOT EXISTS FOR (p:ResearchPaper) REQUIRE p.id IS UNIQUE")
            session.run("CREATE CONSTRAINT keypoint_id IF NOT EXISTS FOR (k:Keypoint) REQUIRE k.id IS UNIQUE")
            session.run("CREATE CONSTRAINT observation_id IF NOT EXISTS FOR (o:Observation) REQUIRE o.id IS UNIQUE")
            session.run("CREATE CONSTRAINT topic_name IF NOT EXISTS FOR (t:Topic) REQUIRE t.name IS UNIQUE")
            
            print("✓ Constraints created")
    
    def create_topics(self):
        """Create the 7 topic nodes"""
        topics = [
            "Offset",
            "Cushioning",
            "Stack Height",
            "Energy Return",
            "Gait Patterns",
            "Shoe Rotation",
            "Weather Conditions"
        ]
        
        with self.driver.session() as session:
            for topic in topics:
                session.run("""
                    MERGE (t:Topic {name: $name})
                """, name=topic)
            
            print(f"✓ Created {len(topics)} topic nodes")
    
    def create_topic_relationships(self):
        """Create RELATED_TO relationships between topics"""
        relationships = [
            # Bidirectional relationships
            ("Offset", "Stack Height", "affects stability and ground feel"),
            ("Cushioning", "Energy Return", "affects responsiveness and propulsion"),
            
            # Relationships to Shoe Rotation
            ("Offset", "Shoe Rotation", "varying offset helps prevent overuse injuries"),
            ("Cushioning", "Shoe Rotation", "rotating cushioning levels reduces repetitive stress"),
            ("Stack Height", "Shoe Rotation", "different stack heights work different muscle groups"),
            ("Energy Return", "Shoe Rotation", "alternating propulsive shoes aids recovery"),
        ]
        
        with self.driver.session() as session:
            for start_topic, end_topic, relationship in relationships:
                session.run("""
                    MATCH (t1:Topic {name: $start})
                    MATCH (t2:Topic {name: $end})
                    MERGE (t1)-[:RELATED_TO {relationship: $rel}]->(t2)
                """, start=start_topic, end=end_topic, rel=relationship)
            
            print(f"✓ Created {len(relationships)} topic relationships")
    
    def import_research_papers(self, json_file):
        """Import research papers with keypoints and create relationships"""
        with open(json_file, 'r') as f:
            articles = json.load(f)
        
        with self.driver.session() as session:
            for idx, article in enumerate(articles):
                # Create ResearchPaper node
                paper_id = f"paper_{idx + 1}"
                
                # Join abstract list into single string if it exists
                abstract_list = article.get("abstract", [])
                abstract = " ".join(abstract_list) if abstract_list else ""
                
                session.run("""
                    MERGE (p:ResearchPaper {id: $id})
                    SET p.title = $title,
                        p.authors = $authors,
                        p.publicationYear = $year,
                        p.sourceFile = $sourceFile,
                        p.abstract = $abstract
                """, 
                    id=paper_id,
                    title=article.get("title", ""),
                    authors=article.get("authors", []),
                    year=article.get("publication_year"),
                    sourceFile=article.get("source_file", ""),
                    abstract=abstract
                )
                
                # Create Keypoint nodes and relationships
                keypoints = article.get("keypoints", [])
                for kp_idx, keypoint_text in enumerate(keypoints):
                    keypoint_id = f"{paper_id}_kp_{kp_idx + 1}"
                    
                    session.run("""
                        MERGE (k:Keypoint {id: $id})
                        SET k.text = $text
                        WITH k
                        MATCH (p:ResearchPaper {id: $paper_id})
                        MERGE (p)-[:HAS_KEYPOINT]->(k)
                    """,
                        id=keypoint_id,
                        text=keypoint_text,
                        paper_id=paper_id
                    )
                
                print(f"✓ Imported paper {idx + 1}/{len(articles)}: {article.get('title', 'Untitled')[:50]}...")
            
            print(f"\n✓ Total: {len(articles)} papers imported")
    
    def import_observations(self):
        """Import my personal observations"""
        observations = [
            {
                "text": "If pushing for more distance, max cushioning can be beneficial while training. For race day, you can consider a lighter cushioning shoe. Max cushioning will absorb impact on the ground while less cushioning will be more responsive when running. Hoka's website mentions this on their cushioning scale.",
                "topics": ["Cushioning"]
            },
            {
                "text": "For half marathons and marathons, having training shoes and having race day shoes can be beneficial. This lessens the risk of your shoes wearing out during your race. yYou can also consider a carbon-plated shoe for your race day shoe when ready. You can also have a range in offset for your shoe rotation. For example, I am alright with a shoe offset between 6-8mm for my long runs and my easy runs. But if I am doing a hard speed workout, I prefer a 4mm shoe.",
                "topics": ["Shoe Rotation", "Energy Return", "Offset"]
            },
            {
                "text": "Look for shoes that are labeled as GTX or Gore-Tex. These shoes are designed to be water-resistant or waterproof, making them suitable for wet weather conditions. I was unable to run a race before because I didn't have water proof shoes and it was raining heavily that day.",
                "topics": ["Weather Conditions"]
            },
            {
                "text": "Offset, also known as heel to toe drop can be a shoe spec to look at depending on your striking pattern or if you're experiencing pain in the knees or ankles. There are a lot of shoes that range between 8 to 10 mm. This is a great place to start before adjusting. If feeling pain in knees, you can decrease your offset. If feeling pain in ankles, you can increase your offset. When increasing or decreasing, go in small increments. If a heel striker, you'll benefit from a higher offset shoe. If a mid/forefoot striker, you'll benefit from a lower offset shoe.",
                "topics": ["Offset", "Gait Patterns"]
            },
            {
                "text": "Carbon-plated shoes have become popular and give great energy return. But this is honestly more useful for those that run faster. I personally am a slow runner and haven't seen much of a difference. But there are shoes out there that are still propulsive without a carbon plate. There are also nylon plated shoes as well that give great energy return.",
                "topics": ["Energy Return"]
            },
            {
                "text": "Depending on gait patterns, a person can be a neutral runner(balanced roll), an underpronated runner(roll outward), and an overpronated runner(roll inward).",
                "topics": ["Gait Patterns"]
            }
        ]
        
        with self.driver.session() as session:
            for idx, obs in enumerate(observations):
                obs_id = f"obs_{idx + 1}"
                
                # Create Observation node
                session.run("""
                    MERGE (o:Observation {id: $id})
                    SET o.text = $text
                """, id=obs_id, text=obs["text"])
                
                # Create RELATES_TO relationships with topics
                for topic in obs["topics"]:
                    session.run("""
                        MATCH (o:Observation {id: $obs_id})
                        MATCH (t:Topic {name: $topic})
                        MERGE (o)-[:RELATES_TO]->(t)
                    """, obs_id=obs_id, topic=topic)
                
                print(f"✓ Imported observation {idx + 1}/{len(observations)}")
            
            print(f"\n✓ Total: {len(observations)} observations imported")
    
    def get_statistics(self):
        """Print database statistics"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:ResearchPaper)
                OPTIONAL MATCH (p)-[:HAS_KEYPOINT]->(k:Keypoint)
                RETURN count(DISTINCT p) as papers, count(DISTINCT k) as keypoints
            """)
            stats = result.single()
            
            result = session.run("MATCH (t:Topic) RETURN count(t) as topics")
            topics = result.single()["topics"]
            
            result = session.run("MATCH (o:Observation) RETURN count(o) as observations")
            observations = result.single()["observations"]
            
            result = session.run("MATCH ()-[r:RELATED_TO]->() RETURN count(r) as topic_rels")
            topic_rels = result.single()["topic_rels"]
            
            print("\n" + "="*60)
            print("DATABASE STATISTICS")
            print("="*60)
            print(f"Research Papers: {stats['papers']}")
            print(f"Keypoints: {stats['keypoints']}")
            print(f"Observations: {observations}")
            print(f"Topics: {topics}")
            print(f"Topic Relationships: {topic_rels}")
            print("="*60)


def main():
    # Initialize connection
    ingestor = Neo4jIngestion(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    
    try:
        print("Starting Neo4j ingestion...\n")
        
        # Step 1: Create constraints
        print("Step 1: Creating constraints...")
        ingestor.create_constraints()
        
        # Step 2: Create topic nodes
        print("\nStep 2: Creating topic nodes...")
        ingestor.create_topics()
        
        # Step 3: Create topic relationships
        print("\nStep 3: Creating topic relationships...")
        ingestor.create_topic_relationships()
        
        # Step 4: Import research papers and keypoints
        print("\nStep 4: Importing research papers and keypoints...")
        ingestor.import_research_papers("extracted_articles.json")
        
        # Step 5: Import observations
        print("\nStep 5: Importing observations...")
        ingestor.import_observations()
        
        # Step 6: Show statistics
        ingestor.get_statistics()
        
        print("\n✅ Ingestion complete!")
        
    finally:
        ingestor.close()


if __name__ == "__main__":
    main()