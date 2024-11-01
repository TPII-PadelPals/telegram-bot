# Bot_telegram

## Instalar dependencias

 para instalar las dependencias con: 

```
pip install -r requirements.txt
```

## Ajustar variables de entorno
Como paso previo a correr el programa es necesario ajustar algunas variables de entorno en un archivo .env

Con las siguientes variables:

```
TOKEN_BOT_TELEGRAM = '<YOUR_TELEGRAM_TOKEN>'
LANGUAGE = 'ES'
URL = 'localhost'
PORT = '8000'
```

## Para Correr bot:

```
python3 padelpals_bot.py
```

## Para crear un bot propio para pruebas locales

1. Crear un nuevo bot utilizando el bot "BotFather" de telegram.

   a. Iniciar solicitud de creacion del bot con el comando "/newbot".

   b. Crearle un nombre al bot, por ejemplo: "padelpals-<your_name>-test".

   c. Asignarle un nombre de usuario al bot, por ejemplo: "padelpals_<your_name>_bot"


2. Una vez creado utilizamos el token dado en nuestro programa de python, y configuramos la variable de entorno `TOKEN_BOT_TELEGRAM` con el valor generado.

## Pruebas de las funciones del bot

Se utiliza un mock para los mensajes que reciben los metodos de nuestro bot y se verifica los resultados obtenidos.
