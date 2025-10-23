class Article {
  title string?
  authors string[]?
  publication_year int?
  
  // Key takeaways from research
  keypoints string[]
  @description("3-5 key insights about shoe features and their effects")
}

function ExtractArticle(article: pdf) -> Article {
  client ClaudeClient
  prompt #"
    Extract key information and insights from this running shoe research paper.
    
    Research content:
    {{ article }}
    
    Extract:
    - Title, authors, and publication year
    - 3-5 keypoints as separate statements
    
    Each keypoint should be:
    - Written for runners, not researchers (avoid technical jargon like "knee joint negative work" or "vertical ground reaction force")
    - About what shoe features do in practice, not study measurements
    - Include specific numbers when relevant (percentages, speeds, weights)
    - Translate findings into "what this means for shoe choice"
    
    Good keypoint examples:
    - "Maximalist cushioning increases leg stiffness by 15% at speeds above 14 km/h, making them less effective for faster running"
    - "Carbon plates provide minimal performance benefit to runners slower than 10 km pace—beginners should prioritize comfort over expensive carbon technology"
    - "Shoes over 200g significantly increase energy cost for novice runners, suggesting lighter options improve running efficiency"
    
    Bad keypoint examples (too technical):
    - "C1 showed significantly lower knee joint negative work (p=0.008)"
    - "Nike Vaporfly 2 demonstrated the lowest loading rates during initial contact"
    
    Focus on practical takeaways about shoe features (weight, stiffness, cushioning, carbon plates) that help runners make better shoe choices, not study methodology or biomechanical measurements.
    
    {{ ctx.output_format }}
  "#
}

// Test with sample PDF
test sample_article_pdf {
  functions [ExtractArticle]
  args {
    article {file "../papers/Running_in_highly_cushioned_shoes_increases_leg_st.pdf"}
  }
}