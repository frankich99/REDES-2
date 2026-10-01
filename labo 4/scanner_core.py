"""
Módulo del Motor de Escaneo de Puertos TCP y UDP
Curso: Redes de Computadoras 2 - UNSAAC
Laboratorio 04: Scanner de Puertos TCP, UDP
"""

import socket
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Mapeo común de servicios conocidos en caso de que socket.getservbyport no los tenga registrados
COMMON_SERVICES = {
    20: "FTP-Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP",
    68: "DHCP",
    69: "TFTP",
    80: "HTTP",
    110: "POP3",
    123: "NTP",
    135: "MS-RPC",
    137: "NetBIOS-NS",
    138: "NetBIOS-DGM",
    139: "NetBIOS-SSN",
    143: "IMAP",
    161: "SNMP",
    162: "SNMP-Trap",
    443: "HTTPS",
    445: "SMB / Microsoft-DS",
    993: "IMAPS",
    995: "POP3S",
    1433: "MS-SQL",
    1521: "Oracle DB",
    3306: "MySQL",
    3389: "RDP (Escritorio Remoto)",
    5432: "PostgreSQL",
    8080: "HTTP-Proxy / Alt",
    8443: "HTTPS-Alt"
}

def resolve_host(host_str):
    """
    Resuelve el nombre de host o dominio a dirección IPv4.
    Retorna (ip_valida, mensaje_error)
    """
    host_str = host_str.strip()
    if not host_str:
        return None, "El nombre de host o dirección IP no puede estar vacío."
    try:
        ip = socket.gethostbyname(host_str)
        return ip, None
    except socket.gaierror:
        return None, f"No se pudo resolver el host '{host_str}'. Verifica el dominio o la IP."
    except Exception as e:
        return None, f"Error al resolver host: {str(e)}"

def get_service_name(port, protocol="tcp"):
    """
    Retorna el nombre del servicio asociado al puerto y protocolo.
    """
    try:
        return socket.getservbyport(port, protocol.lower()).upper()
    except (OSError, socket.error):
        return COMMON_SERVICES.get(port, "Desconocido")

def scan_tcp_port(target_ip, port, timeout=1.0):
    """
    Escanea un puerto TCP individual utilizando three-way handshake (connect).
    Retorna un diccionario con los resultados.
    """
    t_start = time.perf_counter()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    
    estado = "CERRADO"
    detalle = ""
    
    try:
        # connect() intenta el 3-way handshake (SYN, SYN-ACK, ACK)
        sock.connect((target_ip, port))
        elapsed_ms = (time.perf_counter() - t_start) * 1000
        estado = "ABIERTO"
        detalle = f"Conexión aceptada ({elapsed_ms:.1f} ms)"
    except ConnectionRefusedError:
        elapsed_ms = (time.perf_counter() - t_start) * 1000
        estado = "CERRADO"
        detalle = "Puerto inactivo (Rechazo RST)"
    except socket.timeout:
        elapsed_ms = (time.perf_counter() - t_start) * 1000
        estado = "CERRADO"
        detalle = "Sin respuesta (Filtrado / Timeout)"
    except OSError as e:
        elapsed_ms = (time.perf_counter() - t_start) * 1000
        if getattr(e, 'winerror', None) == 10061:
            estado = "CERRADO"
            detalle = "Puerto inactivo (Rechazo RST)"
        else:
            estado = "CERRADO"
            detalle = f"Error: {e}"
    except Exception as e:
        elapsed_ms = (time.perf_counter() - t_start) * 1000
        estado = "CERRADO"
        detalle = f"Error: {e}"
    finally:
        try:
            sock.close()
        except:
            pass

    return {
        "puerto": port,
        "protocolo": "TCP",
        "estado": estado,
        "servicio": get_service_name(port, "tcp"),
        "tiempo_ms": round(elapsed_ms, 2),
        "detalle": detalle
    }

def scan_udp_port(target_ip, port, timeout=1.0):
    """
    Escanea un puerto UDP individual.
    UDP es un protocolo sin conexión (connectionless).
    - Si se recibe respuesta de datos -> ABIERTO
    - Si el sistema remoto responde con ICMP Port Unreachable (WSAECONNRESET en Windows) -> CERRADO
    - Si no hay respuesta tras timeout -> ABIERTO | FILTRADO (o ABIERTO sin respuesta según RFC 792)
    """
    t_start = time.perf_counter()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    
    # Cargas de prueba (payloads) específicas para servicios comunes UDP
    if port == 53:
        # Consulta DNS estándar para 'google.com' (Type A, Class IN) reconocida universalmente por todos los servidores DNS
        payload = b'\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06google\x03com\x00\x00\x01\x00\x01'
    elif port == 123:
        # NTP v3 request packet
        payload = b'\x1b' + 47 * b'\0'
    elif port == 137:
        # NetBIOS Name Query
        payload = b'\x80\xf0\x00\x10\x00\x01\x00\x00\x00\x00\x00\x00\x20\x43\x4b\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x00\x00\x21\x00\x01'
    elif port == 161:
        # SNMP v1 Get-Next-Request community "public"
        payload = b'\x30\x26\x02\x01\x00\x04\x06\x70\x75\x62\x6c\x69\x63\xa1\x19\x02\x04\x12\x34\x56\x78\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00'
    else:
        # Datagrama de prueba estándar
        payload = b'UNSAAC_PORT_SCAN_PROBE\x00\r\n'

    estado = "CERRADO"
    detalle = ""

    try:
        # connect() en un socket UDP asocia la dirección para recibir errores ICMP (WSAECONNRESET en Windows)
        sock.connect((target_ip, port))
        sock.send(payload)
        
        # Intentamos leer si el servicio responde
        data = sock.recv(1024)
        elapsed_ms = (time.perf_counter() - t_start) * 1000
        estado = "ABIERTO"
        detalle = f"Servicio activo (Respondió {len(data)} bytes)"
        
    except ConnectionResetError:
        # En Windows: WSAECONNRESET (10054) - Se recibió ICMP Port Unreachable Type 3 Code 3
        elapsed_ms = (time.perf_counter() - t_start) * 1000
        estado = "CERRADO"
        detalle = "Puerto inactivo (ICMP Port Unreachable)"
        
    except socket.timeout:
        elapsed_ms = (time.perf_counter() - t_start) * 1000
        estado = "ABIERTO | FILTRADO"
        detalle = "Sin respuesta (Abierto o Filtrado)"
        
    except Exception as e:
        elapsed_ms = (time.perf_counter() - t_start) * 1000
        estado = "CERRADO"
        detalle = f"Error: {str(e)}"
    finally:
        try:
            sock.close()
        except:
            pass

    return {
        "puerto": port,
        "protocolo": "UDP",
        "estado": estado,
        "servicio": get_service_name(port, "udp"),
        "tiempo_ms": round(elapsed_ms, 2),
        "detalle": detalle
    }

class PortScannerManager:
    """
    Gestor de escaneo concurrente con soporte para cancelación,
    hilos de trabajo y callbacks en tiempo real para la interfaz gráfica.
    """
    def __init__(self):
        self.stop_requested = threading.Event()
        self.is_running = False

    def stop(self):
        self.stop_requested.set()

    def run_scan(self, target_host, start_port, end_port, protocol_choice, timeout=0.8, max_threads=20, on_result=None, on_progress=None, on_complete=None):
        """
        Ejecuta el escaneo en un hilo de fondo.
        - target_host: IP o nombre de dominio
        - start_port, end_port: rango de puertos [inicio, fin]
        - protocol_choice: 'TCP', 'UDP' o 'AMBOS'
        - on_result(result_dict): llamado por cada puerto escaneado
        - on_progress(current, total, current_port): llamado para actualizar la barra de progreso
        - on_complete(summary_dict): llamado al finalizar el escaneo
        """
        self.stop_requested.clear()
        self.is_running = True
        
        target_ip, err = resolve_host(target_host)
        if err:
            self.is_running = False
            if on_complete:
                on_complete({"error": err, "total": 0, "open_count": 0, "elapsed": 0})
            return

        tasks = []
        for port in range(start_port, end_port + 1):
            if protocol_choice in ("TCP", "AMBOS"):
                tasks.append((port, "TCP"))
            if protocol_choice in ("UDP", "AMBOS"):
                tasks.append((port, "UDP"))

        total_tasks = len(tasks)
        completed = 0
        open_count = 0
        t0 = time.time()

        # Ordenar las tareas para escanear secuencialmente o mantener orden de reporte
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            future_to_task = {}
            for port, proto in tasks:
                if self.stop_requested.is_set():
                    break
                if proto == "TCP":
                    f = executor.submit(scan_tcp_port, target_ip, port, timeout)
                else:
                    f = executor.submit(scan_udp_port, target_ip, port, timeout)
                future_to_task[f] = (port, proto)

            for future in as_completed(future_to_task):
                if self.stop_requested.is_set():
                    break
                try:
                    res = future.result()
                    completed += 1
                    if "ABIERTO" in res["estado"]:
                        open_count += 1
                    
                    if on_result:
                        on_result(res)
                    if on_progress:
                        on_progress(completed, total_tasks, res["puerto"], res["protocolo"])
                except Exception as e:
                    completed += 1
                    port, proto = future_to_task[future]
                    if on_result:
                        on_result({
                            "puerto": port,
                            "protocolo": proto,
                            "estado": "ERROR",
                            "servicio": "Desconocido",
                            "tiempo_ms": 0,
                            "detalle": str(e)
                        })

        elapsed_total = round(time.time() - t0, 2)
        self.is_running = False
        was_stopped = self.stop_requested.is_set()

        if on_complete:
            on_complete({
                "target_host": target_host,
                "target_ip": target_ip,
                "total": total_tasks,
                "completed": completed,
                "open_count": open_count,
                "elapsed": elapsed_total,
                "cancelled": was_stopped
            })
