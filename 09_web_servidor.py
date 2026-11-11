import socket
import threading


HOST = "0.0.0.0"
PORT = 8767

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind((HOST, PORT))
servidor.listen()

# Aqui se guardan los clientes conectados, con su nombre y el canal para los mensajes
clientes = {}
lock = threading.Lock()


def enviar_a_todos(mensaje):
    """Enviar mensaje."""
    with lock:
        conexiones = list(clientes.items()) #aqui  se crea una copia de los cliente para evitar condiciones de carrera mientras escriben

    for conexion, datos_cliente in conexiones: #se crea una bucle para que recorra por los clientes y envie el mensaje a todos los clientes conectados
        try:
            canal = datos_cliente[1]
            canal.write((mensaje + "\n").encode("utf-8"))
            canal.flush()
        except OSError:
            eliminar_cliente(conexion)


def eliminar_cliente(conexion):
    # Cuando un cliente se desconecta, se elimina de la lsita de cliente y se libera esa conexion
    with lock:
        datos_cliente = clientes.pop(conexion, None) #se verifica si el cliente esta o no y se elimina.

    nombre = datos_cliente[0] if datos_cliente else None #se deja el nombre para mostrarlo como desconectado

    if nombre:
        print(f"{nombre} se desconecto") #se muestra el cliente desconectado en la consola 

    try:
        conexion.close()
    except OSError:
        pass


def atender_cliente(conexion, direccion):
    # Cada cliente conectado es atendido por un hilo independiente.
    canal = conexion.makefile("rwb") #se crea un canal para el cliente
    nombre = "Desconocido"  #si no hay nombre se le pone un nombre por defecto

    try:
        datos = canal.readline() # se verifica quien se conecto
        if not datos:
            return

        nombre = datos.decode("utf-8").rstrip("\r\n")

        with lock:
            clientes[conexion] = (nombre, canal) #se guarda el cliente en la lista de clientes conectados

        print(f"{nombre} conectado desde {direccion}")
        enviar_a_todos(f"[SERVIDOR]: {nombre} se conecto") #se muestra el nombre del cliente en lista

        while True: #se crea un bucle para el envio de mensajes
            datos = canal.readline()

            if not datos:
                break #si no hay datos se rompe el bucle y se desconecta el cliente

            mensaje = datos.decode("utf-8").rstrip("\r\n")
            print(f"[{nombre}]: {mensaje}")
            enviar_a_todos(f"[{nombre}]: {mensaje}") #se imprimen los mensajes de los clientes y se envia a todos los clientes conectados
    finally:
        canal.close()
        eliminar_cliente(conexion)
        enviar_a_todos(f"[SERVIDOR]: {nombre} se desconecto") #cuando hay una desconexion se muestra el mensaje en la consola y se envia a todos los clientes conectados


def aceptar_clientes():
    # Cuando un cliente se conecta, se crea un hilo para atenderlo
    while True:
        conexion, direccion = servidor.accept() #si hay una conexion se acepta y se crea un hilo para atender al cliente
        hilo = threading.Thread( #se crea un hilo para atender al cliente con target y args, enviamos los datos de conexion
            target=atender_cliente,
            args=(conexion, direccion),
            daemon=True,
        )
        hilo.start()


def main():
    print("Servidor")
    print(f"Servidor escuchando en {HOST}:{PORT}") #para verificar los puertos

    # Aqui estan los hilos que se encargan de aceptar clientes y atenderlos
    hilo_aceptar = threading.Thread(target=aceptar_clientes, daemon=True)
    hilo_aceptar.start()

    try:
        while True: #si el servidor esta corriendo se puede enviar mensajes desde el servidor a todos los clientes conectados
            mensaje = input("[SERVIDOR]: ")

            if mensaje.lower() == "salir": #si el mensaje es salir se cierra el servidor y se desconectan todos los clientes
                break

            enviar_a_todos(f"[SERVIDOR]: {mensaje}") #se envia el mensaje a todos los clientes conectados
    finally:
        servidor.close()


if __name__ == "__main__":
    main()
