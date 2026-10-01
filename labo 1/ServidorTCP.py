# ServidorTCP.py
from socket import *

puertoServidor = 65433

# Crear socket TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
socketServidor = socket(AF_INET, SOCK_STREAM)
socketServidor.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Asociar puerto al socket en todas las interfaces locales ('')
socketServidor.bind(('', puertoServidor))

# Escuchar peticiones TCP (cola max 2)
socketServidor.listen(2)
print('El servidor está listo para escuchar')

# Bucle infinito
while True:
    # Espera y acepta conexion entrante
    socketConexion, addr = socketServidor.accept()
    print(f'Conexión recibida de {addr}')
    
    # Recibir hasta 1024 bytes y decodificar a string
    sentencia = socketConexion.recv(1024).decode()
    
    # Transformar a mayusculas
    sentenciaCapitalizada = sentencia.upper()
    
    # Enviar respuesta al cliente
    socketConexion.send(sentenciaCapitalizada.encode())
    
    # Cerrar socket de conexion de este cliente
    socketConexion.close()
