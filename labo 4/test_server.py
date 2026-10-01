"""
Servidor de Prueba Local para Simular la Evaluación del Docente
Curso: Redes de Computadoras 2 - UNSAAC
Laboratorio 04: Scanner de Puertos TCP, UDP

Permite abrir puertos específicos TCP y UDP en localhost (127.0.0.1)
para verificar que el escáner detecte con 100% de precisión
cuáles están ABIERTOS y cuáles CERRADOS.
"""

import socket
import threading
import time
import sys

# Puertos que se abrirán expresamente para la simulación
TCP_OPEN_PORTS = [5024, 5026, 5030, 5035]
UDP_OPEN_PORTS = [5024, 5028, 5032]

running = True
sockets_list = []

def tcp_worker(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', port))
        s.listen(5)
        sockets_list.append(s)
        while running:
            try:
                s.settimeout(1.0)
                conn, addr = s.accept()
                conn.sendall(b"UNSAAC_TCP_OK\n")
                conn.close()
            except socket.timeout:
                continue
            except:
                break
    except Exception as e:
        print(f"[-] No se pudo abrir TCP {port}: {e}")

def udp_worker(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('127.0.0.1', port))
        sockets_list.append(s)
        while running:
            try:
                s.settimeout(1.0)
                data, addr = s.recvfrom(1024)
                s.sendto(b"UNSAAC_UDP_REPLY", addr)
            except socket.timeout:
                continue
            except:
                break
    except Exception as e:
        print(f"[-] No se pudo abrir UDP {port}: {e}")

def main():
    print("=" * 65)
    print("   SERVIDOR DE PRUEBA LOCAL - SIMULADOR DOCENTE REDES 2")
    print("=" * 65)
    print(f"[*] Rango sugerido de prueba: 5020 a 5040 en IP: 127.0.0.1")
    print(f"[+] Puertos TCP configurados como ABIERTOS : {TCP_OPEN_PORTS}")
    print(f"[+] Puertos UDP configurados como ABIERTOS : {UDP_OPEN_PORTS}")
    print("[*] Todos los demás puertos del rango responderán como CERRADOS.")
    print("=" * 65)
    print("Presiona Ctrl+C en esta terminal para detener el servidor.\n")

    threads = []
    for p in TCP_OPEN_PORTS:
        t = threading.Thread(target=tcp_worker, args=(p,), daemon=True)
        t.start()
        threads.append(t)

    for p in UDP_OPEN_PORTS:
        t = threading.Thread(target=udp_worker, args=(p,), daemon=True)
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Deteniendo servidor de prueba...")
        global running
        running = False
        for s in sockets_list:
            try:
                s.close()
            except:
                pass
        print("[✓] Servidor detenido con éxito.")

if __name__ == "__main__":
    main()
