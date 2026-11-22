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

### OpenRouter

Poskytovateľa vyberá OpenRouter automaticky (uprednostňuje lacnejších, pri výpadku skúsi ďalšieho).
Ak potrebuješ konkrétneho, pozri [Výber poskytovateľa](#vyber-poskytovatela).

| Alias | Upstream model | Poznámka |
|---|---|---|
| `openrouter-free` | `openrouter/free` | router cez bezplatné modely, prompty môžu byť logované |
| `qwen4-max-openrouter` | `qwen/qwen4-max` | |
| `deepseek-v4.1-flash-openrouter` | `deepseek/deepseek-v4.1-flash-1017` | |
| `glm-5.3-flash-openrouter` | `z-ai/glm-5.3-flash` | |
| `glm-5.3-openrouter` | `z-ai/glm-5.3` | |
| `minimax-m3.1-flash-openrouter` | `minimax/minimax-m3.1-flash` | |
| `inkling-2-small-openrouter` | `thinkingmachines/inkling-2-small` | |

#### Výber poskytovateľa

Poskytovateľa si vyberáš v každej požiadavke cez `provider`:

```bash
curl "$API_BASE/v1/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-5.3-flash-openrouter",
    "messages": [{"role": "user", "content": "Ahoj!"}],
    "provider": {"only": ["deepinfra"]}
  }'
```

- **Bez `provider`:** OpenRouter vyberie automaticky.
- **`"only": ["deepinfra"]`:** použije sa iba DeepInfra.
- **`"order": ["nebius", "deepinfra"]`:** najprv skúsi Nebius, potom DeepInfra a potom ostatných.

V Pythone pridaj do volania `extra_body={"provider": {"only": ["deepinfra"]}}`.

Vybrať si môžeš každého poskytovateľa, ktorý daný model ponúka. Ich názvy vypíšeš takto
(do URL daj *Upstream model* z tabuľky):

```bash
curl -s "https://openrouter.ai/api/v1/models/z-ai/glm-5.3-flash/endpoints" \
  | jq -r '.data.endpoints[].tag | split("/")[0]' | sort -u
```

!!! warning "Skontroluj si názov"
    Neplatný názov v `only` vráti chybu 404. V `order` sa bez upozornenia preskočí
    a odpovie iný poskytovateľ.

### Lokálne modely (FIIT servery)

| Alias | Server | Poznámka |
|---|---|---|
| `gemma4-26b-a4b-hpc` | HPC | reasoning model |
| `ornith-hpc` | HPC | |
| `qwen3.8-flash-next` | fuska | [nvidia/Qwen3.8-Flash-Next-NVFP4](https://huggingface.co/nvidia/Qwen3.8-Flash-Next-NVFP4), reasoning model |
| `decision-local` | decision | nie chat model: volá sa cez `/v1/systemone`, pozri [Decision služba](#decision-sluzba) |

!!! tip "Reasoning modely"
    `gemma4-26b-a4b-hpc` a `qwen3.8-flash-next` najprv „premýšľajú“ a až potom odpovedajú.
    Pri malom `max_tokens` (napr. 16) minú všetky tokeny na premýšľanie a
    odpoveď je prázdna. Nastav `max_tokens` aspoň na 512.

## Prepis reči (audio transcription)

Endpoint `/v1/audio/transcriptions`.

| Alias | Poznámka |
|---|---|
| `gpt-transcribe-fiit` | odporúčaný |

## Generovanie obrázkov

Endpoint `/v1/images/generations`.

| Alias | Upstream model |
|---|---|
| `gpt-image-2.6-flare-fiit` | `gpt-image-2.6-flare` |
| `gpt-image-2.6-sunburst-fiit` | `gpt-image-2.6-sunburst` |

## Decision služba

Decision služba používa formát **System One** (state + questions), nie OpenAI
chat formát. Nevoláš ju cez `/v1/chat/completions`, ale cez endpoint
`/v1/systemone` s bežným LiteLLM kľúčom.

| Endpoint | Model | Limity |
|---|---|---|
| `POST $API_BASE/v1/systemone` | `decision-local` | 16 384 tokenov na požiadavku, 2 súbežné požiadavky |

```bash
curl -X POST "$API_BASE/v1/systemone" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "decision-local",
    "state": "Customer wrote: I was charged twice for my order and want my money back.",
    "questions": {
      "is_refund_request": {"type": "noul", "instructions": "Is the customer asking for a refund?"}
    }
  }'
```

Odpoveď obsahuje odpoveď na každú otázku pod jej menom, napr.
`{"is_refund_request": {"type": "noul", "noul": 0.98}}`. Typy otázok sú
`noul`, `choice` a `score`. Viac v
[LiteLLM dokumentácii](https://docs.litellm.ai/docs/decisions).

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
