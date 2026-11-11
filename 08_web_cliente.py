import socket
import sys
import threading


HOST = "127.0.0.1"
PORT = 8767


cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

print(" CHAT EXAMEN ")

nombre = input("Nombre del cliente: ") #pide el nombre del usuario

canal = cliente.makefile("rwb")
# El mensaje que se envie al servidor es el nombre del cliente (el ya elegido)
canal.write((nombre + "\n").encode("utf-8"))
canal.flush()


def recibir_mensajes():
    # Aqui se reciben los mensajes para que el cliente pueda ver lo que escriben los demas
    # se crea una condicion donde se verifica que hayan datos recibiendose
    while True:
        datos = canal.readline()

        if not datos:
            print("\nServidor desconectado")
            break

        mensaje = datos.decode("utf-8").rstrip("\r\n")
        print(f"\n{mensaje}")


hilo = threading.Thread(target=recibir_mensajes, daemon=True) #inicia el o los hilos
hilo.start()

try:
    # Este es el hilo principal se encarga de leer y enviar los mensajes del cliente.
    while True:
        mensaje = input(f"[{nombre}]: ")

        if mensaje.lower() == "salir":
            break

        canal.write((mensaje + "\n").encode("utf-8")) #recibe el mensaje y lo envia al server para mostrarlo
        canal.flush()
finally:
    cliente.shutdown(socket.SHUT_RDWR) #cierra la conexion del socket es es por que varios clientes pueden unirse al mismo tiempo
    hilo.join(timeout=1) #esperar un segundo para que el hilo termine de recibir mensajes
    canal.close()
    cliente.close()
