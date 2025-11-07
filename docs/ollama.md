## Ako používať Ollama spoločne s Dencun-om

Tento návod vám ukáže, ako sa pripojiť k službe Ollama, ktorá beží na serveri Dencun, a ako ju používať vo vašich aplikáciách.

### Čo je Ollama?

**Ollama** je nástroj, ktorý umožňuje jednoducho spúšťať a spravovať veľké jazykové modely (LLM) lokálne. V našom prípade beží Ollama na serveri **Dencun** a poskytuje API rozhranie, cez ktoré môžeme týmto modelom posielať požiadavky.

- Ollama docs: [https://ollama.com/docs](https://ollama.com/docs)

### ‼️ Predpoklady ‼️

Než začnete, musíte mať:
* Nastavený a funkčný **SSH prístup** na server `dencun`.

---

### 1. Pripojenie k Ollama API

Existujú dva hlavné spôsoby, ako sa k Ollama API pripojiť. 

#### Spôsob A: Chcem pracovať z môjho **lokálneho počítača**

Ak chcete API volať z kódu, ktorý beží na vašom osobnom počítači (napr. vo VS Code na vašom laptope), musíte si "presmerovať" port zo servera Dencun k sebe pomocou **port forwardingu**. 

Do terminálu zadajte nasledujúci príkaz:

```bash
ssh -L 11434:localhost:11434 dencun
```
* **Vysvetlenie:** Tento príkaz hovorí: "Všetko, čo pošlem na `localhost:11434` na *mojom* počítači, presmeruj cez SSH na `localhost:11434` na serveri `dencun`."
* **Dôležité:** Nechajte tento terminál otvorený po celý čas, kým chcete pripojenie používať.

Teraz je pre vás Ollama API dostupné na adrese `http://localhost:11434`.

#### Spôsob B: Chcem pracovať **priamo na serveri Dencun**

Ak spúšťate svoj kód (napr. Python skript) priamo na serveri Dencun, nepotrebujete žiadny port forwarding.

1.  Jednoducho sa prihláste na server:
    ```bash
    ssh dencun
    ```
2.  Keďže váš kód beží na tom istom stroji ako Ollama, API je pre vás automaticky dostupné na adrese `http://localhost:11434`.

---

### 2. Overenie funkčnosti

Bez ohľadu na to, ktorý scenár ste si vybrali, môžete funkčnosť overiť rovnako.

Otvorte vo vašom webovom prehliadači (ak používate Scenár A) alebo použite nástroj `curl` v termináli (funguje pre oba scenáre) nasledujúcu adresu:

`http://localhost:11434/api/tags`

**Očakávaný výsledok:** Mali by ste vidieť odpoveď vo formáte JSON, ktorá obsahuje zoznam všetkých LLM modelov dostupných na serveri Dencun.

```json
{
  "models": [
    {
      "name": "llama3:latest",
      "modified_at": "...",
      "size": ...
    },
    {
      "name": "mistral:latest",
      "modified_at": "...",
      "size": ...
    }
    // ... a ďalšie modely
  ]
}
```

---

### 3. Príklad použitia v Pythone (pomocou litellm)
Knižnica litellm zjednodušuje volanie rôznych API. Keďže ste sa (v oboch scenároch) pripojili k localhost:11434, kód bude pre oba prípady rovnaký.

Uistite sa, že máte knižnicu nainštalovanú:

```bash
pip install litellm
```
Potom ju môžete použiť v Pythone takto:

```python
from litellm import completion
import os


api_base_url = "http://localhost:11434"
model_name = "ollama_chat/llama3.2:3b"  # format : "ollama/MENO_MODELU"

messages = [
    {"content": "respond in 20 words. who are you?", "role": "user"}
]

response = completion(
        model=model_name, 
        messages=messages, 
        api_base=api_base_url
    )
print(response.choices[0].message.content)
```