# Hydroponics sensors app

- Start virtual environment:
```shell


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
docker-compose --env-file .env up --build
```