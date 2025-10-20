class Article {
  title string?
  authors string[]?
  publication_year int?
  
  // Just the key takeaways
  keypoints string[]
  @description("List of practical insights about shoe features and their effects")
  
  // One-liner summary
  practical_summary string?
  @description("Bottom line: what should runners know from this research?")
}

function ExtractArticle(article: string) -> Article {
  client GraniteClient
  prompt #"
    Extract PRACTICAL shoe advice from this research paper.
    
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

test sample_article {
  functions [ExtractArticle]
  args {
    article #"
      Running in highly cushioned shoes increases leg stiffness and amplifies impact loading
      Juha-Pekka Kulmala
      1,2, Jukka Kosonen3, Jussi Nurminen1 & Janne Avela3
      Running shoe cushioning has become a standard method for managing impact loading and consequent
      injuries due to running. However, despite decades of shoe technology developments and the fact that
      shoes have become increasingly cushioned, aimed to ease the impact on runners' legs, running injuries
      have not decreased. To better understand the shoe cushioning paradox, we examined impact loading
      and the spring-like mechanics of running in a conventional control running shoe and a highly cushioned
      maximalist shoe at two training speeds, 10 and 14.5 km/h. We found that highly cushioned maximalist
      shoes alter spring-like running mechanics and amplify rather than attenuate impact loading. This
      surprising outcome was more pronounced at fast running speed (14.5 km/h), where ground reaction
      force impact peak and loading rate were 10.7% and 12.3% greater, respectively, in the maximalist shoe
      compared to the conventional shoe, whereas only a slightly higher impact peak (6.4%) was found at the
      10 km/h speed with the maximalist shoe. We attribute the greater impact loading with the maximalist
      shoes to stiffer leg during landing compared to that of running with the conventional shoes. These
      discoveries may explain why shoes with more cushioning do not protect against impact-related running
      injuries.
      Running, a popular exercise across the world, offers significant cardiovascular and other health benefits1.
      However, each year between 37% and 56% of runners worldwide incur injuries2 that typically result from repeated
      loading of the musculoskeletal system. In particular, when the foot hits the ground, the magnitude of the vertical
      ground reaction force impact peak (IP) and loading rate (LR) have been linked to the risk of running injuries3,4,
      so the study of running injury prevention has primarily focused on the management of impact loading.
      In order to reduce the risk of running-related injuries, running shoe manufactures have added cushioning
      to shoe soles aimed at reducing impact loading. However, studies show no evidence of reduced running injury
      rates with increasing amounts of cushioning5–8. The explanation for this counterintuitive finding may lie in the
      well-recognized, but poorly understood phenomenon that highly cushioned shoes have a limited ability to reduce
      impact loading6,9. In fact, some studies have noted even a slight increase in impact loading when running in shoes
      with a compliant versus a hard midsole10–13. These findings counters the impact attenuation theory14 and the
      results of in vitro mechanical impact tests15, both of which indicate a significant reduction in impact loading with
      increased cushioning. Our goal in this paper is to shed new light on understanding the mechanisms that might be
      responsible for countering the impact attenuation effect of extra shoe cushioning during running.
      Previous research16 has identified elastic leg behaviour as critical to terrestrial locomotion. During running,
      the leg undergoes compression in the first half of the stance while gradually decelerating the body and then recoils
      in the second half of the stance to reaccelerate the body. This cyclic behaviour permits efficient force produc-
      tion through a stretch-shortening muscle action17 and is essential for avoiding mechanically costly high-energy
      impacts during foot–ground contact18. The elastic leg behaviour during running can be described as a simple
      spring-mass system, where a leg-spring supports the point mass representing the runner's centre of mass (CoM)
      (Fig. 1)19–21.
      Received: 23 May 2018
      Accepted: 9 November 2018
      Published online: 30 November 2018
    "#
  }
}