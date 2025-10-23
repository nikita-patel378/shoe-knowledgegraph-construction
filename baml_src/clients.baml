// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview

client<llm> GraniteClient {
  provider "openai-generic"
  options {
    base_url "http://localhost:11434/v1"
    model granite4:latest
  }
}

client<llm> GemmaClient {
  provider "openai-generic"
  options {
    base_url "http://localhost:11434/v1"
    model gemma3:latest
  }
}

client<llm> LlamaClient {
  provider "openai-generic"
  options {
    base_url "http://localhost:11434/v1"
    model llama3.2:latest
  }
}
client<llm> CustomGPT{
  provider openai
  retry_policy Constant
  options {
    model "gpt-5-mini-2025-08-07"
    api_key env.OPENAI_API_KEY
  }
}



client<llm> CustomSonnet {
  provider anthropic
  options {
    model "claude-sonnet-4-5-20250929"
    api_key env.ANTHROPIC_API_KEY
  }
}


client<llm> CustomHaiku {
  provider anthropic
  retry_policy Exponential
  options {
    model "claude-haiku-4-5-20251001"
    api_key env.ANTHROPIC_API_KEY
  }
}

client<llm> OpenRouterClient {
  provider openai-generic
  options {
    base_url "https://openrouter.ai/api/v1"
    model "google/gemini-2.5-flash"
    api_key env.OPENROUTER_API_KEY
  }
}

client<llm> ClaudeClient {
  provider fallback
  options {
    strategy [CustomHaiku, CustomSonnet]
  }
}
// https://docs.boundaryml.com/docs/snippets/clients/round-robin
client<llm> CustomFast {
  provider round-robin
  options {
    // This will alternate between the two clients
    strategy [CustomGPT, CustomHaiku]
  }
}

// https://docs.boundaryml.com/docs/snippets/clients/fallback
client<llm> OpenaiFallback {
  provider fallback
  options {
    // This will try the clients in order until one succeeds
    strategy [CustomGPT, CustomGPT]
  }
}

// https://docs.boundaryml.com/docs/snippets/clients/retry
retry_policy Constant {
  max_retries 3
  // Strategy is optional
  strategy {
    type constant_delay
    delay_ms 200
  }
}

retry_policy Exponential {
  max_retries 3
  // Strategy is optional
  strategy {
    type exponential_backoff
    delay_ms 1500
    multiplier 2
    max_delay_ms 10000
  }
}