# LiteLLM modely

Zoznam modelov dostupných cez FIIT LiteLLM proxy. Do parametra `model` zadávaš
**alias** z prvého stĺpca (s prefixom `openai/` pri volaní cez knižnicu `litellm`).
Aktuálny zoznam pre tvoj kľúč vráti:

```bash
curl "$API_BASE/v1/models" -H "Authorization: Bearer $API_KEY"
```

## Chat modely

### Anthropic

| Alias | Upstream model | Poznámka |
|---|---|---|
| `claude-fable-5.2-fiit` | `claude-fable-5-2` | najsilnejší, náročné uvažovanie |
| `claude-opus-5.5-fiit` | `claude-opus-5-5` | odporúčaný na väčšinu úloh |
| `claude-sonnet-5.5-fiit` | `claude-sonnet-5-5` | rýchly a lacnejší |
| `claude-haiku-5.5-fiit` | `claude-haiku-5-5` | najrýchlejší, najlacnejší |

### OpenAI

| Alias | Upstream model | Poznámka |
|---|---|---|
| `gpt-6.2-astra-fiit` | `gpt-6.2-astra` | najsilnejší |
| `gpt-6.2-sol-fiit` | `gpt-6.2-sol` | pomer výkon/cena |
| `gpt-6.1-terra-fiit` | `gpt-6.1-terra` | rýchly |
| `gpt-6-luna-fiit` | `gpt-6-luna` | najlacnejší |
| `gpt-5.6-sol-fiit` | `gpt-5.6-sol` | staršia generácia |
| `gpt-5.6-terra-fiit` | `gpt-5.6-terra` | staršia generácia |
| `gpt-5.6-luna-fiit` | `gpt-5.6-luna` | staršia generácia |
| `gpt-5.4-fiit` | `gpt-5.4` | staršia generácia |
| `gpt-5.4-mini-fiit` | `gpt-5.4-mini` | staršia generácia |
| `gpt-5.4-nano-fiit` | `gpt-5.4-nano` | končí 2027-04-01, náhrada `gpt-6-luna-fiit` |
| `gpt-4.1-fiit` | `gpt-4.1` | končí 2027-01-14, náhrada `gpt-6-luna-fiit` |
| `gpt-4.1-mini-fiit` | `gpt-4.1-mini` | končí 2027-01-14, náhrada `gpt-6-luna-fiit` |

### Lokálne modely (FIIT servery)

| Alias | Server | Poznámka |
|---|---|---|
| `gemma4-26b-a4b-hpc` | HPC | reasoning model |
| `ornith-hpc` | HPC | |
| `qwen` | fuska | reasoning model |

!!! tip "Reasoning modely"
    `gemma4-26b-a4b-hpc` a `qwen` najprv „premýšľajú“ a až potom odpovedajú.
    Pri malom `max_tokens` (napr. 16) minú všetky tokeny na premýšľanie a
    odpoveď je prázdna. Nastav `max_tokens` aspoň na 512.

## Prepis reči (audio transcription)

Endpoint `/v1/audio/transcriptions`.

| Alias | Poznámka |
|---|---|
| `gpt-transcribe-fiit` | odporúčaný |
| `whisper-fiit` | končí 2027-02-26, náhrada `gpt-transcribe-fiit` |
| `gpt-4o-transcribe-fiit` | končí 2027-02-26, náhrada `gpt-transcribe-fiit` |
| `gpt-4o-mini-transcribe-fiit` | končí 2027-02-26, náhrada `gpt-transcribe-fiit` |

## Generovanie obrázkov

Endpoint `/v1/images/generations`.

| Alias | Upstream model |
|---|---|
| `gpt-image-2.6-flare-fiit` | `gpt-image-2.6-flare` |
| `gpt-image-2.6-sunburst-fiit` | `gpt-image-2.6-sunburst` |

## Decision služba

Decision služba používa vlastný formát **System One** (state + questions), nie
OpenAI chat formát. Preto ju **nevoláš** cez `/v1/chat/completions` ani cez
`litellm.completion`, ale priamo cez endpoint `/v1/systemone` s LiteLLM kľúčom.

| Endpoint | Model | Limity |
|---|---|---|
| `POST $API_BASE/v1/systemone` | `decision-local` | 16 384 tokenov na požiadavku, 2 súbežné požiadavky |

```bash
curl -X POST "$API_BASE/v1/systemone" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "decision-local", ...}'
```

Telo požiadavky je vo formáte System One (state + questions).

!!! warning "Prístup na požiadanie"
    Endpoint `/v1/systemone` funguje len pre kľúče, ktorým ho povolil
    administrátor. Bez povolenia vráti `403`. O prístup požiadaj vedúceho.

!!! note "Používaj alias"
    Vždy posielaj `"model": "decision-local"`. Názov fyzického modelu sa môže
    po výmene zmeniť, preto naň v kóde nespoliehaj, ani na hodnotu poľa
    `model` v odpovedi.

## Ukážka

```python
import litellm

response = litellm.completion(
    model="openai/claude-haiku-5.5-fiit",
    messages=[{"role": "user", "content": "Ahoj!"}],
    api_key=API_KEY,
    api_base=API_BASE,
)
print(response.choices[0].message.content)
```
