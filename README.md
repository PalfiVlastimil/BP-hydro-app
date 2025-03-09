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