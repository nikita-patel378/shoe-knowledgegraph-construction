from neo4j import GraphDatabase
from transformers import pipeline
from dotenv import load_dotenv
import os

load_dotenv()

# Neo4j connection
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Topics to classify against
TOPICS = [
    "Offset",
    "Cushioning",
    "Stack Height",
    "Energy Return",
    "Gait Patterns",
    "Shoe Rotation",
    "Weather Conditions"
]

class KeypointClassifier:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print("Loading zero-shot classification model...")
        self.classifier = pipeline("zero-shot-classification", 
                                   model="facebook/bart-large-mnli")
        print("✓ Model loaded")
    
    def close(self):
        self.driver.close()
    
    def get_all_keypoints(self):
        """Fetch all keypoints from the database"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (k:Keypoint)
                RETURN k.id as id, k.text as text
            """)
            return [{"id": record["id"], "text": record["text"]} 
                    for record in result]
    
    def classify_keypoint(self, keypoint_text, max_topics=2):
        """
        Classify a keypoint against all topics.
        Returns top max_topics (default 2) most relevant topics.
        """
        result = self.classifier(keypoint_text, TOPICS, multi_label=True)
        
        # Get top N topics
        top_topics = result['labels'][:max_topics]
        
        return top_topics
    
    def create_relationships(self, keypoint_id, topics):
        """Create RELATES_TO relationships between keypoint and topics"""
        with self.driver.session() as session:
            for topic in topics:
                session.run("""
                    MATCH (k:Keypoint {id: $keypoint_id})
                    MATCH (t:Topic {name: $topic})
                    MERGE (k)-[:RELATES_TO]->(t)
                """, keypoint_id=keypoint_id, topic=topic)
    
    def classify_all_keypoints(self, max_topics=2):
        """Classify all keypoints and create relationships"""
        keypoints = self.get_all_keypoints()
        total = len(keypoints)
        
        print(f"\nClassifying {total} keypoints (max {max_topics} topics each)...\n")
        
        for idx, kp in enumerate(keypoints, 1):
            # Classify
            topics = self.classify_keypoint(kp["text"], max_topics)
            
            # Create relationships
            self.create_relationships(kp["id"], topics)
            print(f"✓ [{idx}/{total}] Keypoint linked to: {', '.join(topics)}")
        
        print(f"\n✅ Classification complete!")
    
    def get_statistics(self):
        """Show classification statistics"""
        with self.driver.session() as session:
            # Total keypoints
            result = session.run("MATCH (k:Keypoint) RETURN count(k) as total")
            total = result.single()["total"]
            
            # Keypoints with topics
            result = session.run("""
                MATCH (k:Keypoint)-[:RELATES_TO]->(:Topic)
                RETURN count(DISTINCT k) as classified
            """)
            classified = result.single()["classified"]
            
            # Relationships by topic
            result = session.run("""
                MATCH (k:Keypoint)-[:RELATES_TO]->(t:Topic)
                RETURN t.name as topic, count(k) as keypoints
                ORDER BY keypoints DESC
            """)
            
            print("\n" + "="*60)
            print("CLASSIFICATION STATISTICS")
            print("="*60)
            print(f"Total Keypoints: {total}")
            print(f"Classified Keypoints: {classified}")
            print("\nKeypoints per Topic:")
            for record in result:
                print(f"  {record['topic']}: {record['keypoints']}")
            print("="*60)


def main():
    classifier = KeypointClassifier(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    
    try:
        # Classify keypoints to max 2 topics each
        classifier.classify_all_keypoints(max_topics=2)
        
        # Show statistics
        classifier.get_statistics()
        
    finally:
        classifier.close()


if __name__ == "__main__":
    main()