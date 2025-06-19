#!/bin/bash

if [ -z "$1" ]; then
  echo "Uso: $0 <URL_EC2>"
  exit 1
fi

URL_EC2=$1

# Mata procesos previos de ngrok (opcional)
killall ngrok > /dev/null 2>&1

# Inicia ngrok en segundo plano (ajusta el puerto según tu servicio)
nohup ngrok http http://$URL_EC2:8000 > /dev/null 2>&1 &

# Espera a que ngrok levante
sleep 3

# Obtiene la URL HTTPS desde el API local de ngrok
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url')

if [ -z "$NGROK_URL" ]; then
  echo "No se pudo obtener la URL de ngrok"
  killall ngrok > /dev/null 2>&1
  exit 1
fi

# Actualiza o agrega la variable en el .env
if grep -q "USERS_SERVICE_HOST_PROD=" .env; then
  sed -i "s|USERS_SERVICE_HOST_PROD=.*|USERS_SERVICE_HOST_PROD=$NGROK_URL|" .env
else
  echo "USERS_SERVICE_HOST_PROD=$NGROK_URL" >> .env
fi

echo "USERS_SERVICE_HOST_PROD actualizado en .env con: $NGROK_URL"
