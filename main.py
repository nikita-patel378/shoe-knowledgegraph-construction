import base64
import json
import time
from pathlib import Path
from baml_client import b
from baml_py import Pdf
from dotenv import load_dotenv

load_dotenv()

def process_papers(papers_dir: str, output_file: str, delay_seconds: int = 10):
    """Process all PDF papers with delay between requests"""
    results = []
    pdf_files = list(Path(papers_dir).glob("*.pdf"))
    
    print(f"Found {len(pdf_files)} papers to process...\n")
    
    for i, pdf_path in enumerate(pdf_files):
        print(f"Processing {i+1}/{len(pdf_files)}: {pdf_path.name}")
        
        try:
            # Read and convert to base64
            with open(pdf_path, 'rb') as f:
                pdf_bytes = f.read()
                pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
            
            # Create Pdf and extract
            pdf = Pdf.from_base64(pdf_base64)
            result = b.ExtractArticle(article=pdf)
            
            # Convert to dict
            article_dict = {
                "source_file": pdf_path.name,
                "title": result.title,
                "authors": result.authors,
                "publication_year": result.publication_year,
                "keypoints": result.keypoints,
                "practical_summary": result.practical_summary
            }
            
            results.append(article_dict)
            print(f"✓ Successfully extracted")
            
            # Add delay between requests (except for last one)
            if i < len(pdf_files) - 1:
                print(f"Waiting {delay_seconds} seconds before next request...\n")
                time.sleep(delay_seconds)
            
        except Exception as e:
            print(f"✗ Error: {e}\n")
            continue
    
    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"Processed {len(results)}/{len(pdf_files)} papers successfully")
    print(f"Results saved to: {output_file}")
    print(f"{'='*60}")
    
    return results

if __name__ == "__main__":
    # 20 second delay between each paper to avoid hitting rate limits for requests
    results = process_papers("papers", "extracted_articles.json", delay_seconds=20)
    
    # Print summary
    print("\n📊 Extraction Summary:")
    for article in results:
        print(f"\n• {article['title']}")
        print(f"  Year: {article['publication_year']}")
        print(f"  Keypoints: {len(article['keypoints'])}")