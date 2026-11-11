# Examen - Jordy Viscaino 36880

## Contenido

El sistema contiene 3 archivos 2 que hacen referencia al cliente y servidor y uno que es el docker-compose para levantar el contenedor

## Entorno virtual

Es recomendable usar un entorno virtual como buena practica.
### Crear el entorno virtual

Si todavía no existe la carpeta venv, ejecutar desde la raiz el siguiente comando:

- python -m venv venv


### Activar el entorno virtual

En cada terminal donde se ejecutará el sistema, ejecutar lo siguiente:


- .\venv\Scripts\Activate.ps1


### Instalar dependencias

Para este sistema se uso websockets y threading, que son parte de python, lo mas recomendable seria instalarlos
aunque pueden venir por defecto, instalar websockets mediante:
- pip install websockets

## Ejecucion

### Iniciar el server
Antes tener abierto docker desktop
Desde la raiz ejecutar lo siguiente:


- docker compose up servidor
 Esto para que el servidor se ejecute en segundo plano y no ocupar esa terminal

Luego si se desea abrir otra terminal o en la misma ejecutar el comando:
- docker compose attach servidor

Esto para poder ejecutar la terminal del servidor y poder hablar a travez del servidor a los clientes
Luego esperar a que un cliente se conecte

### Iniciar clientes

En otra terminal activar el entorno y luego ejecutar:


- python 08_web_cliente.py 

Pedira el nombre del cliente, luego de eso se podra escribir

En otra terminal activar primero el entorno
virtual y luego ejecutar:


- python 08_web_cliente.py "Cliente 2"

hacemos lo mismo y ponemos otro nombre


## Como funciona

Cada cliente usa un hilo que permite recibir y escribir mensajes sin problemas
 y el server espera los mensajes para reemitirlos a otro cliente

El servidor crea un hilo para cada cliente conectado.

Cuando un cliente envía un mensaje, el servidor lo muestra y lo reenvía a
todos los clientes conectados con el nombre respectivo

para cerrar las terminales ejecutar CTRL + C
