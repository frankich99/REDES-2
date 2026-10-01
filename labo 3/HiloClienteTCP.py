# HiloClienteTCP.py
import socket
import threading

class HiloCliente(threading.Thread):
    def __init__(self, ip, puerto, socket):
        threading.Thread.__init__(self)
        self.nroIP = ip
        self.nroPuerto = puerto
        self.socketCnx = socket

    def run(self):
        mensaje = 'xxxx'
        while len(mensaje):
            try:
                mensaje = self.socketCnx.recv(1024).decode()
                if not mensaje:
                    break

                # Requerimiento 4.2: Informacion en el extremo del host servidor
                print(f"\n[Peticion Recibida]")
                print(f"  Mensaje         : {mensaje}")
                print(f"  Socket Cliente  : {self.socketCnx.getpeername()}")
                print(f"  Socket Servidor : {self.socketCnx.getsockname()}")
                print(f"  Hilo            : {self.name} (ID: {self.ident}) | Activos: {threading.active_count()}")

                mensajeCapitalizado = mensaje.upper()
                self.socketCnx.send(mensajeCapitalizado.encode())

                print(f"[Respuesta Enviada]")
                print(f"  Mensaje         : {mensajeCapitalizado}")
                print(f"  Destino Cliente : {self.socketCnx.getpeername()}")
                print(f"  Origen Servidor : {self.socketCnx.getsockname()}")
                print(f"  Hilo            : {self.name}\n")
            except ConnectionResetError:
                break

        self.socketCnx.close()
