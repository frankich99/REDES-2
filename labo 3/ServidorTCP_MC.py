# ServidorTCP_MC.py
import socket
import threading
import HiloClienteTCP

idServidor = ''
puertoServidor = 12000

socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socketServidor.bind((idServidor, puertoServidor))
socketServidor.listen(5)

print('El servidor esta listo para escuchar')

try:
    while True:
        (socketConexion, (ipCliente, puertoCliente)) = socketServidor.accept()
        hilo = HiloClienteTCP.HiloCliente(ipCliente, puertoCliente, socketConexion)
        hilo.start()
except KeyboardInterrupt:
    print('\nServidor detenido.')
finally:
    socketServidor.close()
