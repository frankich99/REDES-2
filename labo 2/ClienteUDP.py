# ClienteUDP.py
from socket import *
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Dirección IP del servidor (por defecto 127.0.0.1 para pruebas locales, o pasada como argumento)
idServidor = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
puertoServidor = 12000

# Crear socket cliente UDP (AF_INET = IPv4, SOCK_DGRAM = UDP)
socketCliente = socket(AF_INET, SOCK_DGRAM)

# Tiempo límite de espera (timeout) de 5 segundos para evitar bloqueo indefinido
socketCliente.settimeout(5.0)

# Obtener entrada desde el teclado del usuario
mensaje = input('Entrar una sentencia en minúsculas: ')

# Enviar mensaje al servidor (codificado a bytes)
socketCliente.sendto(mensaje.encode('utf-8'), (idServidor, puertoServidor))
























try:
    # Leer respuesta replicada desde el socket hacia un string
    mensajeModificado, direccionServidor = socketCliente.recvfrom(2048)
    
    # Imprimir string recibido y dirección del servidor
    print('Socket del servidor =', direccionServidor)
    print(mensajeModificado.decode('utf-8'))
except timeout:
    print(f"[!] Error: Tiempo de espera agotado. No se recibió respuesta de {idServidor}:{puertoServidor}")
finally:
    # Cerrar socket
    socketCliente.close()
