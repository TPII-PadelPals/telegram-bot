# Bot_telegram

## Instalar dependencias

 para instalar las dependencias con: 

```
pip install -r requirements.txt
```

## Para Correr bot:

```
python3 padelpals_bot.py
```

## [opcional] Si quisieramos crear un bot propio

1. Crear un nuevo bot utilizando el bot "BotFather" de telegram en telegram.
   a. Iniciar solicitud de creacion del bot con el comando "/newbot".
   b. Crearle un nombre al bot, en este caso "trabajo_profesional_grupo_padelpals_bot".
   c. Asignarle un nombre de usuario al bot, en este caso "PadelPals_bot", por regla el nombre debe terminar en "bot".
2. Una vez creado utilizamos el token dado en nuestro programa de python, haciendo uso de la libreria "pyTelegramBotAPI".

## Pruebas de las funciones del bot

Se utiliza un mock para los mensajes que reciben los metodos de nuestro bot y se verifica los resultados obtenidos.
