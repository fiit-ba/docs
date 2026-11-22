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

GPT modely idú cez OpenRouter, aliasy ostávajú rovnaké. Požiadavku môže obslúžiť OpenAI, Azure
alebo Amazon Bedrock, podľa modelu. Ak chceš len OpenAI, pridaj `"provider": {"only": ["openai"]}`.

V Responses API posielaj vždy celú históriu. `previous_response_id` a `store: true` cez OpenRouter nefungujú.

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
Ak si ho chceš vybrať, pozri [Výber poskytovateľa](#vyber-poskytovatela)
a [odporúčania podľa súkromia, ceny a rýchlosti](#odporucani-poskytovatelia).

| Alias | Upstream model | Poznámka |
|---|---|---|
| `openrouter-free` | `openrouter/free` | router cez bezplatné modely, prompty môžu byť logované |
| `qwen4-max-openrouter` | `qwen/qwen4-max` | |
| `deepseek-v4.1-flash-openrouter` | `deepseek/deepseek-v4.1-flash-1017` | |
| `glm-5.3-flash-openrouter` | `z-ai/glm-5.3-flash` | |
| `glm-5.3-openrouter` | `z-ai/glm-5.3` | |
| `minimax-m3.1-flash-openrouter` | `minimax/minimax-m3.1-flash` | |
| `inkling-2-small-openrouter` | `thinkingmachines/inkling-2-small` | |
| `jev-openrouter` | `~typesafe/jev-latest` | nie chat model: volá sa cez `/v1/systemone`, pozri [Decision služba](#decision-sluzba) |

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

#### Odporúčaní poskytovatelia

Vyber si podľa toho, na čom ti záleží. Všetci v tabuľke podporujú ZDR
(zero data retention), čiže prompty po spracovaní bežne neukladajú.

| Alias | Súkromie | Cena (vstup / výstup) | Rýchlosť |
|---|---|---|---|
| `deepseek-v4.1-flash-openrouter` | `nebius` | `sail-research` ($0,04 / $0,10) | `nebius` (350 t/s) |
| `glm-5.3-flash-openrouter` | `nebius` | `relace` ($0,05 / $0,07) | `mistral` (213 t/s) |
| `glm-5.3-openrouter` | `nebius` | `wafer` ($0,07 až 0,18 / $1,40) | `nebius` (354 t/s) |
| `minimax-m3.1-flash-openrouter` | `nebius` | `nebius` ($0,15 / $0,60) | `nebius` (300 t/s) |
| `inkling-2-small-openrouter` | `nebius` | `primeintellect` ($0,15 / $0,50) | `primeintellect` (399 t/s) |

Názov z tabuľky daj do `provider`:

- **Súkromie:** `"provider": {"only": ["nebius"], "zdr": true}`. Nebius sídli v Holandsku. Keď má výpadok,
  dostaneš chybu a prompt k inému poskytovateľovi nejde.
- **Cena alebo rýchlosť:** `"provider": {"order": ["sail-research"], "zdr": true}` (názov vymeň podľa modelu).
  Pri výpadku odpovie iný poskytovateľ so ZDR, ktorý môže byť drahší alebo pomalší.

Ak nevieš, čo si vybrať, zober `nebius`. Nájdeš ho pri všetkých piatich modeloch z tabuľky
a pri troch bol v teste aj najrýchlejší. Najlacnejší ale väčšinou nie je.

`qwen4-max-openrouter` má iba poskytovateľa Alibaba, bez ZDR. So `"zdr": true` preto vráti chybu.
Pri `openrouter-free` si poskytovateľa nevyberaj a počítaj s logovaním promptov.

!!! warning "Citlivé dáta"
    ZDR platí len pre poskytovateľa. FIIT LiteLLM si prompty ukladá vždy a sídlo v EÚ
    nezaručuje, že sa dáta spracujú v EÚ. Ak dáta nesmú odísť z fakulty, použi
    `gemma4-26b-a4b-hpc`, `ornith-hpc` alebo `qwen3.8-flash-next`.

!!! note "Ako sme vyberali (22. 11. 2026)"
    - Ceny sú v USD za milión tokenov podľa OpenRouter. Porovnávali sme ich pri pomere
      3 vstupné tokeny na 1 výstupný, bez flex a spot endpointov.
    - Pri MiniMax je `wafer` o 10 % lacnejší, v teste však vracal 429 alebo bol pomalý.
    - Rýchlosť je medián zo 7 požiadaviek po 350 tokenov cez FIIT proxy, vrátane čakania
      na začiatok odpovede. Merali sme len vybraných poskytovateľov a v jeden deň,
      takže čísla ber orientačne. Ceny aj rýchlosť sa menia.

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

Endpoint `/v1/images/generations`. Úprava obrázkov (`/v1/images/edits`) cez OpenRouter nefunguje.

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
| `POST $API_BASE/v1/systemone` | `jev-openrouter` | 262 144 tokenov podľa OpenRouter, iba text |

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

Pre Jev od TypeSafe zmeň v ukážke iba `model` na `jev-openrouter`. Stojí $0,042 za milión
vstupných tokenov, výstup je zadarmo. Alias ide vždy na najnovšiu verziu, takže sa výsledky môžu
časom zmeniť.

!!! warning "Jev ide mimo fakulty"
    Dáta idú cez OpenRouter k firme TypeSafe. Pole `provider` (aj `"zdr": true`) sa pri
    `/v1/systemone` zahodí bez upozornenia, takže ZDR si tu nevynútiš. Citlivé dáta sem neposielaj.

!!! note "Používaj alias"
    Pri lokálnej službe vždy posielaj `"model": "decision-local"`. Názov fyzického modelu sa môže
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
