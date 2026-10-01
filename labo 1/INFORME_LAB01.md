# INFORME: LABORATORIO 01 - PROGRAMACIÓN DE SOCKETS EN TCP CON PYTHON
**Curso:** Redes de Computadoras 2  
**Institución:** Universidad Nacional de San Antonio Abad del Cusco (UNSAAC)  

---

## 1. Archivos Implementados

### Servidor: `ServidorTCP.py`
```python
from socket import *

puertoServidor = 65432
socketServidor = socket(AF_INET, SOCK_STREAM)
socketServidor.bind(('', puertoServidor))
socketServidor.listen(2)
print('El servidor está listo para escuchar')

while True:
    socketConexion, addr = socketServidor.accept()
    print(f'Conexión de: {addr}')
    sentencia = socketConexion.recv(1024).decode()
    sentenciaCapitalizada = sentencia.upper()
    socketConexion.send(sentenciaCapitalizada.encode())
    socketConexion.close()
```

### Cliente: `ClienteTCP.py`
```python
from socket import *

idServidor = '127.0.0.1'  # o IP LAN del servidor (ej. 192.168.1.X)
puertoServidor = 65432

socketCliente = socket(AF_INET, SOCK_STREAM)
socketCliente.connect((idServidor, puertoServidor))

mensaje = input('Entrar una sentencia en minúsculas: ')
socketCliente.send(mensaje.encode())

mensajeModificado = socketCliente.recv(1024)
print('Desde el servidor:', mensajeModificado.decode())

socketCliente.close()
```

---

## 2. Instrucciones de Ejecución

### Terminal 1 (Servidor)
```powershell
python ServidorTCP.py
```
Salida:
```text
El servidor está listo para escuchar
```

### Terminal 2 (Cliente)
```powershell
python ClienteTCP.py
```
Entrada:
```text
Entrar una sentencia en minúsculas: hola redes 2 unsaac
```
Salida recibida:
```text
Desde el servidor: HOLA REDES 2 UNSAAC
```

---

## 3. Ejercicios Propuestos Resueltos

### 5.1 Filtrado de conexiones por puerto específico

#### En Windows:
```cmd
netstat -aon | findstr :65432
```
*Sintaxis genérica:*
```cmd
netstat -aon | findstr :<PUERTO>
```

#### En Linux:
*Opción A (Filtro nativo `ss`):*
```bash
ss -tuapn '( sport = :65432 or dport = :65432 )'
```
*Opción B (Tubería con grep):*
```bash
ss -tuapn | grep :65432
```

---

## 4. Conceptos Clave
- **Socket:** Endpoint bidireccional (IP + Puerto) para comunicación proceso a proceso.
- **TCP (SOCK_STREAM):** Protocolo confiable, orientado a conexión, full-duplex.
- **Puertos:**
  - *0 - 1023:* Well-Known (servicios estándar)
  - *1024 - 49151:* Registrados
  - *49152 - 65535:* Efímeros / Dinámicos (asignados a clientes)
