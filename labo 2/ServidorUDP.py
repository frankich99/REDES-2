# ServidorUDP.py
from socket import *
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Puerto de escucha del servidor
puertoServidor = 12000

# Crear socket servidor UDP (IPv4, UDP/Datagram)
socketServidor = socket(AF_INET, SOCK_DGRAM)

# Enlazar socket al nro. de puerto local 12000 en todas las interfaces disponibles
socketServidor.bind(('', puertoServidor))

print(f"El servidor está listo para recibir en el puerto {puertoServidor}", flush=True)

# Lazo eterno para recibir datagramas
try:
    while True:
        # Recibir mensaje y la tupla de dirección del cliente (IP, puerto)
        mensaje, direccionCliente = socketServidor.recvfrom(2048)
        
        texto_recibido = mensaje.decode('utf-8')
        print(f"[+] Recibido de {direccionCliente}: '{texto_recibido}'", flush=True)
        
        # Cambiar mensaje a mayúsculas
        mensajeModificado = texto_recibido.upper()
        
        # Enviar mensaje modificado de regreso al cliente
        socketServidor.sendto(mensajeModificado.encode('utf-8'), direccionCliente)
        print(f"[->] Enviado a {direccionCliente}: '{mensajeModificado}'", flush=True)

except KeyboardInterrupt:
    print("\nServidor finalizado por el usuario.")
finally:
    socketServidor.close()
