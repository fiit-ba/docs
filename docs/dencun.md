# Dencun SSH Access Guide

Tento tutorial slúži na nastavenie SSH prístupu k serveru Dencun a následne ako pomocou tohto prístupu používať Ollama service, ktorý využíve na prácu s LLM modelmi.

- SSH prístupu - pomocou terminálu alebo VS Code/iný editor
- Dencun (2x4090) - je názov servera/stroja v 5.44, ku ktorému sa pripájate pomocou SSH alebo fyzicky.
- **Google registračný formulár** na registráciu žiadost o prihlásenie - [link](https://forms.gle/B8Va3AofQr9eNjmq6) (prihlasenie pomocou stuba emailu)
- **Google sheet harmonogram** na rezerváciu času na prácu so serverom - [link](https://docs.google.com/spreadsheets/d/1_PIisa2bJGXeLBm-xElSUzh8ZaSH8xGJC_7-IR2kZgY/edit) (prihlasenie pomocou stuba emailu)

## Dôležité upozornenia

- Výpočtový výkon servera je obmedzený, preto sa snažte optimalizovať vaše požiadavky a nevyťažovať server zbytočne.
- Tento server sa zdiela medzi viacerými používateľmi a preto je potrebné sa prihlasovať/rezervovať si čas na prácu s ním. Dokument cez, ktorý sa registrujete - alokujete si svoj slot je dostupný [tu (google sheet)](https://docs.google.com/spreadsheets/d/1_PIisa2bJGXeLBm-xElSUzh8ZaSH8xGJC_7-IR2kZgY/edit) (prihlasenie pomocou stuba emailu)

## Krok 1: Vyplenenie formulára

Pre získanie prístupu na server je potrebné vyplniť [tento formulár](https://forms.gle/B8Va3AofQr9eNjmq6) (prihlasenie pomocou stuba emailu). Následne vám do pár dní bude vytvorené konto a bude vám bude pridelené prihlasovacie meno (pre študentov je to ais id - xmeno, pre zamestnancov meno.priezvisko).

## Krok 2: Generovanie SSH kľúčov

Na získanie prístupu k serveru potrebujete SSH kľúč, ktoré sa používa na autentifikáciu. Tento kľúč sa generuje pomocou príkazu, ktorý treba spustiť v termináli.

### 1. SSH kľúč pre FIIT
```bash
ssh-keygen -t ed25519 -C "vas_email@stuba.sk" -f ~/.ssh/fiit_internal
```


**Poznámky k SSH kľúčom:**
- Kľúč sa vytvorí v adresári `~/.ssh/`
- Pre kľúč sa vytvoria dva súbory:
  - **Privátny kľúč** (`fiit_internal`) - uchovávajte ho v bezpečí a nikdy ho nezdieľajte
  - **Verejný kľúč** (`fiit_internal.pub`)

## Krok 3: Konfigurácia SSH

Pre jednoduché pripojenie vytvorte alebo upravte konfiguračný súbor SSH:

1. Otvorte alebo vytvorte súbor `~/.ssh/config`:
```bash
vim ~/.ssh/config
```

2. Pridajte nasledujúcu konfiguráciu (nahraďte `[vase_prihlasovacie_meno]` vaším skutočným ais id menom - xmeno (studenti), meno.priezvisko (zamestnanci)):

```bash
Host blockaccess
    Hostname 147.175.150.111
    Port 8022
    User extaccess
    IdentityFile ~/.ssh/fiit_internal
 
Host dencun
    Hostname dencun
    Port 8822
    User [vase_prihlasovacie_meno]
    IdentityFile ~/.ssh/fiit_internal
    ProxyJump blockaccess
```

## Krok 3: Pripojenie na server

### Pomocou terminálu
Po správnej konfigurácii sa môžete pripojiť jednoducho príkazom:
```bash
ssh dencun
```

### Pomocou VS Code
1. Nainštalujte rozšírenie **Remote - SSH** v VS Code
2. Stlačte `Ctrl+Shift+P` (alebo `Cmd+Shift+P` na MacOS)
3. Napíšte "Remote-SSH: Connect to Host..." a zvolte možnosť `Remote-SSH: Connect to Host...`
4. Vyberte `dencun` zo zoznamu
