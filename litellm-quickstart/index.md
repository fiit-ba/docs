# LiteLLM Quickstart

```
!uv add litellm python-dotenv
```

```
import litellm
import os
from dotenv import load_dotenv

load_dotenv()
```

Treba mať vytvorený súbor .env s premennými API_KEY a API_BASE:

```
API_KEY=your_api_key_here
API_BASE=https://your_api_base_here
```

API_KEY a API_BASE vám boli dodané vedúcim.

```
API_KEY = os.getenv("API_KEY")
API_BASE = os.getenv("API_BASE")
```

# TLDR

```
response = litellm.completion(
    model="openai/claude-haiku-5.5-fiit", # model ID
    messages=[{"content": "Hello, how are you?", "role": "user"}], # chat messages v openai formate (user, system, assistant)
    api_key=API_KEY,
    api_base=API_BASE,
)
response
```

```
!curl -X GET "{API_BASE}/v1/models" -H "Authorization: Bearer {API_KEY}"
```

Všetky modely, ktoré sú dostupné pre tvoj API_KEY a API_BASE

- zoznam modelov s popisom: [LiteLLM modely](https://fiit-ba.github.io/docs/litellm-models/index.md)
- ako "model" parameter do litellm zadávaš "id", takže `openai/claude-haiku-5.5-fiit` a nie `anthropic/claude-haiku-5-5`

# Viac info

- litellm dokumentácia: [litellm.ai/docs](https://docs.litellm.ai/docs)
- batch call - [batching_completion](https://docs.litellm.ai/docs/completion/batching)
- steaming - [stream+async](https://docs.litellm.ai/docs/completion/stream)
