---
# Hydroponics sensors app
Aplikace slouží k ukládání informací ze senzorů na Raspberry PI 4/5 pro monitorování vlastností hydroponického květinače. Na zařízení RPI je nastaven crontab pro automatické ukládání informací do databáze pomocí API v backendu. Ten samý backend poté posílá informace na React frontend. Uživatel má možnost si požádat of fotku květináče či informace ze senzorů.
- Aplikace se skládá ze tří částí:
	- Backend - Flask API
	- Frontend - React aplikace
	- Databáze - MongoDB



## Spuštění aplikace
### Backend
```bash
cd backend
source venv/bin/activate
pip install requirements.txt
python main.py 

```

### Databáze
- Používá se Docker a docker-compose
- build s pomocí .env souboru
- v .env se vyskytuje defaultní heslo, které se musí poté změnit
- v rootu projektu:
```bash
docker compose --env-file .env up --build # pro Linux docker engine
```
### Frontend
- React aplikace
```bash
cd frontend
npm install
npm run dev -- --host
```
### Testovací skript:
- Tento skript se používal na začátku projektu pro otestovaní funkčnosti senzorů
- Poté se přestal používat, skript nebyl nijak měněn
- Pro odpojené senzory nebude fungovat
```bash
python backend/main.py
```


## Známé limity projektu
- Raspberry PI se nenabootuje, pokud se neodpojí kabel od ADS1115, jakmile kontrolka svítí zeleně, lze znovu připojit
- Problém s knihovnou grove.py, kdy komponenta Grove Base Hat for Raspberry PI nemusí fungovat kvůli jiné adrese v adc.py skriptu, musí se v baličku manuálně změnit. Podrobněji [zde](https://wiki.seeedstudio.com/Grove_Base_Hat_for_Raspberry_Pi/#software)
