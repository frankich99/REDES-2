# ClienteTCP_MC.py
from socket import *

# Modificar aqui la direccion IP del Servidor ('127.0.0.1' para local, o la IP de la otra maquina)
idServidor = '192.168.125.120'
puertoServidor = 12000

socketCliente = socket(AF_INET, SOCK_STREAM)
socketCliente.connect((idServidor, puertoServidor))

mensaje = input('Entrar un mensaje en minusculas: ')

while mensaje != "":
    # Requerimiento 4.3: Informacion TCP de la peticion en el cliente
    print("\n[Peticion]")
    print(f"  Socket Cliente (Local)  : {socketCliente.getsockname()}")
    print(f"  Socket Servidor (Remoto): {socketCliente.getpeername()}")

    socketCliente.send(mensaje.encode())

    mensajeModificado = socketCliente.recv(1024)
    print('Respuesta del servidor:', mensajeModificado.decode())

    # Requerimiento 4.3: Informacion TCP de la respuesta en el cliente
    print("[Respuesta]")
    print(f"  Socket Cliente (Local)  : {socketCliente.getsockname()}")
    print(f"  Socket Servidor (Remoto): {socketCliente.getpeername()}\n")

    mensaje = input('Entrar un mensaje en minusculas: ')

socketCliente.close()
