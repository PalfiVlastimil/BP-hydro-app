# Hydroponics sensors app

- Start virtual environment for testing locally without Docker:
```shell
cd backend/lib/grove.py/
virtualenv -p python3 backend/venv --system-site-packages #for grove.py
pip install grove.py
source backend/venv/bin/activate
deactivate
```
Testing script:
```shell
python backend/main.py
```

Other useful commands to recognize circuits
```shell
sudo i2cdetect -y 1
sudo i2cget -y 1 0x08

iwgetid -r
sudo nmtui
```

## To start a Docker
- Be sure to run Docker Desktop and Docker Compose
- build with .env file:
```bash
docker-compose --env-file config.env up --build #for Windows docker engine
docker compose --env-file config.env up --build #for Linux docker engine
```

## For backend
- backend's docker was removed due to error that couldn't be resolved in time
- to use it anyway, these are commands to initialize backend:
```bash
python -m venv venv --system-site-packages

source backend/venv/bin/activate
pip3 install -r backend/requirements.txt
gunicorn -w 4 --preload  -b 0.0.0.0:5000 app:app
deactivate
```

## Triggering data sending:
```bash
curl -X POST http://localhost:5000/save_sensor_data -H "Content-Type: application/json"
```