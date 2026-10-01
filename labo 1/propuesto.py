# propuesto.py - UNSAAC Redes 2 - Lab 01
# Ejercicio Propuesto 5.1: Filtrado de conexiones por puerto y comunicacion TCP persistente

import sys
import socket
import subprocess
import platform

PUERTO_DEFECTO = 65432
IP_DEFECTO = '127.0.0.1'

def filtrar(puerto=PUERTO_DEFECTO):
    os_name = platform.system()
    print(f"[*] Filtrando conexiones puerto {puerto} ({os_name}):")
    if os_name == 'Windows':
        cmd = f"netstat -aon | findstr :{puerto}"
    else:
        cmd = f"ss -tuapn '( sport = :{puerto} or dport = :{puerto} )'"
    print(f"Comando: {cmd}\n")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    salida = res.stdout.strip()
    if salida:
        print(salida)
    else:
        print(f"[!] Sin conexiones activas en puerto :{puerto}")

def servidor(puerto=PUERTO_DEFECTO):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(('', puerto))
    except OSError as e:
        print(f"[ERROR BIND] Puerto {puerto} ocupado: {e}")
        return
    s.listen(2)
    print(f"[*] Servidor escuchando en :{puerto} (Ctrl+C para parar)")
    try:
        while True:
            conn, addr = s.accept()
            print(f"[+] Conectado: {addr}")
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    txt = data.decode('utf-8', errors='replace').strip()
                    print(f"Recibido: {txt}")
                    if txt.lower() == 'salir':
                        conn.send(b"BYE\n")
                        break
                    conn.send(f"{txt.upper()}\n".encode('utf-8'))
                except ConnectionResetError:
                    print("[-] Cliente desconectado abruptamente")
                    break
            conn.close()
            print(f"[-] Desconectado: {addr}")
    except KeyboardInterrupt:
        print("\n[*] Servidor cerrado")
    finally:
        s.close()

def cliente(ip=IP_DEFECTO, puerto=PUERTO_DEFECTO):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, puerto))
    except ConnectionRefusedError:
        print(f"[ERROR CONEXION] Servidor no activo en {ip}:{puerto}. Iniciar servidor primero.")
        return
    print(f"[*] Conectado a {ip}:{puerto}. Enviar texto ('salir' para cerrar):")
    try:
        while True:
            msg = input("> ")
            if not msg.strip():
                continue
            s.send(msg.encode('utf-8'))
            if msg.strip().lower() == 'salir':
                break
            res = s.recv(1024).decode('utf-8', errors='replace')
            print(f"Servidor: {res.strip()}")
    except KeyboardInterrupt:
        print("\n[*] Cliente finalizado")
    finally:
        s.close()

if __name__ == '__main__':
    arg1 = sys.argv[1].lower() if len(sys.argv) > 1 else 'f'
    if arg1 in ('s', 'server', 'servidor'):
        p = int(sys.argv[2]) if len(sys.argv) > 2 else PUERTO_DEFECTO
        servidor(p)
    elif arg1 in ('c', 'client', 'cliente'):
        ip = sys.argv[2] if len(sys.argv) > 2 else IP_DEFECTO
        p = int(sys.argv[3]) if len(sys.argv) > 3 else PUERTO_DEFECTO
        cliente(ip, p)
    elif arg1 in ('f', 'filtro', 'filtrar'):
        p = int(sys.argv[2]) if len(sys.argv) > 2 else PUERTO_DEFECTO
        filtrar(p)
    elif arg1.isdigit():
        filtrar(int(arg1))
    else:
        print("Uso:")
        print("  python propuesto.py            -> Filtra conexiones puerto 65432")
        print("  python propuesto.py <puerto>   -> Filtra conexiones puerto N")
        print("  python propuesto.py s [puerto] -> Servidor persistente (para probar netstat)")
        print("  python propuesto.py c [ip] [p] -> Cliente persistente (mantiene ESTABLISHED)")
