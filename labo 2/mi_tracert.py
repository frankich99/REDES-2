#!/usr/bin/env python3
import subprocess
import sys
import re

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def ejecutar_traza(ip_destino="202.116.36.58", max_saltos=45):
    print("=" * 70)
    print(f" INICIANDO TRAZA HACIA: {ip_destino} (Máximo {max_saltos} saltos)")
    print(" Protocolo: ICMP Echo Request (idéntico a Windows tracert)")
    print("=" * 70 + "\n")
    
    # En Windows se usa tracert; en Linux traceroute
    if sys.platform == "win32":
        comando = ["tracert", "-d", "-h", str(max_saltos), ip_destino]
    else:
        comando = ["traceroute", "-I", "-m", str(max_saltos), ip_destino]
    
    proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    saltos = []
    
    for linea in proceso.stdout:
        print(linea, end="")
        linea_limpia = linea.strip()
        # Verificar si la línea comienza con un número de salto
        if linea_limpia and re.match(r"^\d+\s+", linea_limpia):
            partes = linea_limpia.split()
            numero_salto = partes[0]
            saltos.append((numero_salto, linea_limpia))
            
    proceso.wait()
    
    if not saltos:
        print("\n[!] No se pudieron registrar saltos.")
        return

    ultimo_num, ultima_linea = saltos[-1]
    coincide = ip_destino in ultima_linea
    
    print("\n" + "=" * 70)
    print("                    RESUMEN FINAL DE LA TRAZA")
    print("=" * 70)
    print(f" • IP Destino consultada:     {ip_destino}")
    print(f" • Total de saltos dados:     {ultimo_num} saltos")
    print(f" • Límite por defecto (30):   {'SUPERADO (>30)' if int(ultimo_num) > 30 else 'NO SUPERADO (<=30)'}")
    print(f" • IP en la última línea:     {ip_destino if coincide else 'NO ENCONTRADA'}")
    print(f" • ¿Coincide última línea?:   {'SÍ (VÁLIDO SEGÚN DOCENTE)' if coincide else 'NO COINCIDE'}")
    print(f" • Estado final de la traza:  {'EXITOSA - DESTINO ALCANZADO' if coincide else 'INCOMPLETA'}")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    # Si el usuario no pasa argumentos, usa por defecto la IP con el récord de 34 saltos
    destino = sys.argv[1] if len(sys.argv) > 1 else "202.116.36.58"
    saltos = int(sys.argv[2]) if len(sys.argv) > 2 else 45
    ejecutar_traza(destino, saltos)
