# SSH prístup na servery Dencun a Pectra

Tento návod popisuje, ako si nastaviť SSH prístup na GPU servery **Dencun** a **Pectra**. K obom serverom sa pripájate cez spoločný prístupový server `blockaccess`.

| Server     | GPU                                                                     | SSH alias |
| ---------- | ----------------------------------------------------------------------- | --------- |
| **Dencun** | 2× NVIDIA GeForce RTX 4090 (24 GB)                                      | `dencun`  |
| **Pectra** | NVIDIA RTX PRO 6000 Blackwell (96 GB) + NVIDIA GeForce RTX 5090 (32 GB) | `pectra`  |

- **Google registračný formulár** na žiadosť o prístup: [link](https://forms.gle/B8Va3AofQr9eNjmq6) (prihlásenie pomocou STU emailu)
- **Google sheet harmonogram** na rezerváciu času na serveri: [link](https://docs.google.com/spreadsheets/d/1_PIisa2bJGXeLBm-xElSUzh8ZaSH8xGJC_7-IR2kZgY/edit) (prihlásenie pomocou STU emailu)

Formulár aj harmonogram sú spoločné pre oba servery.

## Dôležité upozornenia

- Výpočtový výkon serverov je obmedzený. Optimalizujte svoje úlohy a nevyťažujte servery zbytočne.
- Servery zdieľa viacero používateľov. Pred prácou si rezervujte čas v [harmonograme](https://docs.google.com/spreadsheets/d/1_PIisa2bJGXeLBm-xElSUzh8ZaSH8xGJC_7-IR2kZgY/edit) a uveďte, na ktorom serveri pracujete.
- Pred spustením úlohy skontrolujte, či GPU nevyužíva niekto iný: `nvidia-smi`.

## Krok 1: Vyplnenie formulára

Pre získanie prístupu vyplňte [tento formulár](https://forms.gle/B8Va3AofQr9eNjmq6) (prihlásenie pomocou STU emailu). Do pár dní vám vytvoríme konto a pridelíme prihlasovacie meno (študenti: AIS ID, napr. `xmeno`; zamestnanci: `meno.priezvisko`).

## Krok 2: Generovanie SSH kľúča

Na prihlásenie potrebujete SSH kľúč. Vygenerujete ho týmto príkazom v termináli:

```
ssh-keygen -t ed25519 -C "vas_email@stuba.sk" -f ~/.ssh/fiit_internal
```

**Poznámky k SSH kľúčom:**

- Kľúč sa vytvorí v adresári `~/.ssh/` ako dva súbory:
  - **Privátny kľúč** (`fiit_internal`): uchovávajte ho v bezpečí a nikdy ho nezdieľajte.
  - **Verejný kľúč** (`fiit_internal.pub`)

## Krok 3: Konfigurácia SSH

1. Otvorte alebo vytvorte súbor `~/.ssh/config`:

   ```
   vim ~/.ssh/config
   ```

1. Pridajte nasledujúcu konfiguráciu. `[vase_prihlasovacie_meno]` nahraďte vaším prihlasovacím menom (študenti: `xmeno`, zamestnanci: `meno.priezvisko`):

```
Host blockaccess
    Hostname 147.175.150.111
    Port 8022
    User extaccess
    IdentityFile ~/.ssh/fiit_internal

Host dencun
    Hostname dencun
    Port 22
    User [vase_prihlasovacie_meno]
    IdentityFile ~/.ssh/fiit_internal
    ProxyJump blockaccess

Host pectra
    Hostname pectra
    Port 22
    User [vase_prihlasovacie_meno]
    IdentityFile ~/.ssh/fiit_internal
    ProxyJump blockaccess
```

## Krok 4: Pripojenie na server

### Pomocou terminálu

```
ssh dencun
```

alebo

```
ssh pectra
```

### Pomocou VS Code

1. Nainštalujte rozšírenie **Remote - SSH** vo VS Code.
1. Stlačte `Ctrl+Shift+P` (alebo `Cmd+Shift+P` na macOS).
1. Napíšte „Remote-SSH: Connect to Host...“ a zvoľte túto možnosť.
1. Vyberte `dencun` alebo `pectra` zo zoznamu.

## Port forwarding

Ak na serveri spustíte službu (napr. Jupyter alebo vlastný model na porte `8000`) a chcete ju otvoriť zo svojho počítača, presmerujte si port:

```
ssh -L 8000:localhost:8000 pectra
```

Služba je potom dostupná na `http://localhost:8000` na vašom počítači, kým je terminál otvorený.

## LLM modely

Na serveroch nebeží zdieľaný LLM server (Ollama). Na prácu s LLM používajte [LiteLLM proxy](https://fiit-ba.github.io/docs/litellm-quickstart/index.md). Zoznam modelov nájdete v [LiteLLM modely](https://fiit-ba.github.io/docs/litellm-models/index.md).
