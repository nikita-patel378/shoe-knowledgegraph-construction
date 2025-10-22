class Article {
  title string?
  authors string[]?
  publication_year int?
  
  // Just the key takeaways
  keypoints string[]
  @description("List of practical insights about shoe features and their effects")
  
  // One-liner summary
  practical_summary string?
  @description("Bottom line: what should runners know from this research? (1-2 sentences max)")
}

function ExtractArticle(article: pdf) -> Article {
  client CustomHaiku
  prompt #"
    Extract details and practical insights from the research paper.
    
    Research content:
    {{ article }}
    
    Your goal: Help runners of all levels understand what shoe features actually matter.
    
    Extract 3-5 keypoints as separate bullet points. Each keypoint should be:
    - Clear and actionable
    - About specific shoe features and their real-world effects
    - Backed by the research findings
    
    Examples of good keypoints:
    - "Maximalist cushioning increases leg stiffness, especially at faster speeds (14.5 km/h)"
    - "Highly cushioned shoes amplify impact loading rather than reduce it"
    - "More cushioning does not correlate with fewer running injuries"
    
    Also provide a practical_summary: 1-2 sentences maximum that captures the main takeaway for runners.
    
    Focus on:
    - What shoe features do (good and bad)
    - When/why certain features matter
    - Real effects backed by research, not marketing claims
    
    {{ ctx.output_format }}
  "#
}

// Update test to use a PDF file
test sample_article_pdf {
  functions [ExtractArticle]
  args {
    article {file "../papers/Running_in_highly_cushioned_shoes_increases_leg_st.pdf"}
  }
}