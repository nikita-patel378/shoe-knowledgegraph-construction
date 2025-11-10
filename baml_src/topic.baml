enum Topic {
//the topics to classify user queries to 
  Offset
  Cushioning
  StackHeight
  EnergyReturn
  GaitPatterns
  ShoeRotation
  WeatherConditions
}

class ClassificationResult {
  primary_topic Topic
  @description("The main topic to focus the response on")
  
  related_topics Topic[]
  @description("Secondary topics to briefly mention if relevant")
}

function ClassifyQuery(input: string) -> ClassificationResult {
  client GraniteClient
  prompt #"
    Classify the user query to identify the primary topic and any related topics.

    {{ ctx.output_format }}

    {{ _.role("user") }} 
    
    {{ input }}
  "#
}

// Tests
test knee_pain {
  functions [ClassifyQuery]
  args {
    input "My knees hurt when I run"
  }
}

test rainy_weather {
  functions [ClassifyQuery]
  args {
    input "What shoes for rainy days?"
  }
}

test race_shoes {
  functions [ClassifyQuery]
  args {
    input "I want faster race shoes"
  }
}

test shoe_rotation {
  functions [ClassifyQuery]
  args {
    input "Should I rotate my shoes?"
  }
}

test gait_pattern {
  functions [ClassifyQuery]
  args {
    input "My feet roll inward"
  }
}

test offset_heel_drop {
  functions [ClassifyQuery]
  args {
    input "What's the difference between 4mm and 10mm heel drop shoes?"
  }
}