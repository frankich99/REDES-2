# GUIA DE EJECUCION: LABORATORIO 03 - SOCKETS E HILOS (TCP)
**Redes de Computadoras 2 - UNSAAC**

---

## 1. ARCHIVOS EN LA CARPETA
- **`ServidorTCP_MC.py`**: Servidor concurrente en puerto 12000.
- **`HiloClienteTCP.py`**: Gestión de hilos (debe estar en el mismo directorio del servidor).
- **`ClienteTCP_MC.py`**: Cliente interactivo TCP.

---

## 2. EJECUCION EN WINDOWS 11

### Modo 1: Prueba Local (1 PC con 3 Terminales)

Abra 3 ventanas de PowerShell o CMD en `F:\unsaac\redes 2\labo 3`:

#### Ventana 1 (Servidor):
```powershell
python ServidorTCP_MC.py
```
> Para detener el servidor presione **`Ctrl + C`**.

#### Ventana 2 (Cliente 1):
*(Verificar que en `ClienteTCP_MC.py` esté `idServidor = '127.0.0.1'`)*:
```powershell
python ClienteTCP_MC.py
```
Ingrese una cadena en minúsculas y presione `Enter`. Para salir presione `Enter` sin texto.

#### Ventana 3 (Cliente 2):
```powershell
python ClienteTCP_MC.py
```
Ingrese otra cadena en minúsculas en paralelo para probar la concurrencia multihilo.

---

### Modo 2: Prueba en Red LAN (3 PCs Diferentes)

1. **En la PC Servidor**:
   - Obtener la IP local con:
     ```powershell
     ipconfig
     ```
     *(Anotar la Dirección IPv4, ej: `192.168.1.50`)*.
   - Ejecutar:
     ```powershell
     python ServidorTCP_MC.py
     ```
   - Si el Firewall de Windows muestra una alerta, seleccionar **"Permitir acceso"**.

2. **En las PCs Clientes**:
   - Abrir `ClienteTCP_MC.py` y cambiar únicamente la línea 4 con la IP del Servidor:
     ```python
     idServidor = '192.168.1.50' # Modificar aqui la direccion IP del Servidor
     ```
   - Ejecutar:
     ```powershell
     python ClienteTCP_MC.py
     ```

---

## 3. RESULTADOS ESPERADOS EN PANTALLA

### En el Cliente (Cliente 1 o 2):
```text
Entrar un mensaje en minusculas: unsaac redes 2

[Peticion]
  Socket Cliente (Local)  : ('127.0.0.1', 54210)
  Socket Servidor (Remoto): ('127.0.0.1', 12000)
Respuesta del servidor: UNSAAC REDES 2
[Respuesta]
  Socket Cliente (Local)  : ('127.0.0.1', 54210)
  Socket Servidor (Remoto): ('127.0.0.1', 12000)

Entrar un mensaje en minusculas:
```

### En el Servidor:
```text
El servidor esta listo para escuchar

[Peticion Recibida]
  Mensaje         : unsaac redes 2
  Socket Cliente  : ('127.0.0.1', 54210)
  Socket Servidor : ('127.0.0.1', 12000)
  Hilo            : Thread-1 (ID: 15420) | Activos: 2
[Respuesta Enviada]
  Mensaje         : UNSAAC REDES 2
  Destino Cliente : ('127.0.0.1', 54210)
  Origen Servidor : ('127.0.0.1', 12000)
  Hilo            : Thread-1

[Peticion Recibida]
  Mensaje         : prueba multihilo
  Socket Cliente  : ('127.0.0.1', 54211)
  Socket Servidor : ('127.0.0.1', 12000)
  Hilo            : Thread-2 (ID: 18232) | Activos: 3
[Respuesta Enviada]
  Mensaje         : PRUEBA MULTIHILO
  Destino Cliente : ('127.0.0.1', 54211)
  Origen Servidor : ('127.0.0.1', 12000)
  Hilo            : Thread-2
```

---

## 4. RESPUESTA AL EJERCICIO PROPUESTO 5.1

> **Pregunta 5.1:** *Averiguar el valor de la dirección IP Pública de la UNSAAC, i.e., la dirección IP con la que la Red Institucional es vista desde el Internet.*

- **Dirección IP Pública Principal:** `200.48.82.143` (Portal oficial `unsaac.edu.pe`).
- **Subred Pública Institucional:** `200.48.82.0/24`.
- **Servidores en el mismo bloque:**
  - `ns1.unsaac.edu.pe` (DNS Primario): `200.48.82.4`
  - `mail.unsaac.edu.pe` (Correo): `200.48.82.8`
  - `aulavirtual.unsaac.edu.pe` (Moodle): `200.48.82.132`
- **Comandos de verificacion en Windows 11 (PowerShell):**
  - Desde cualquier red (via DNS):
    ```powershell
    Resolve-DnsName unsaac.edu.pe
    ```
  - Estando en la PC del laboratorio UNSAAC (IP publica de salida via NAT):
    ```powershell
    curl.exe ifconfig.me
    ```
- **Mecanismo en Red de Laboratorios UNSAAC:**
  Las computadoras de los laboratorios poseen direccionamiento privado (RFC 1918) y salen hacia Internet mediante **NAT/PAT**, compartiendo la IP publica del gateway institucional.
