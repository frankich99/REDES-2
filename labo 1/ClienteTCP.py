# ClienteTCP.py
from socket import *

# '127.0.0.1' para prueba local en misma PC; cambiar por IP del servidor si esta en red LAN
idServidor = '127.0.0.1'
puertoServidor = 65433

# Crear socket TCP
socketCliente = socket(AF_INET, SOCK_STREAM)

# Conectar al servidor
socketCliente.connect((idServidor, puertoServidor))

# Capturar entrada usuario
mensaje = input('Entrar una sentencia en minúsculas: ')

# Enviar bytes codificados
socketCliente.send(mensaje.encode())

# Esperar y recibir respuesta del servidor (max 1024 bytes)
mensajeModificado = socketCliente.recv(1024)

# Imprimir resultado decodificado
print('Desde el servidor:', mensajeModificado.decode())

# Cerrar conexion
socketCliente.close()
