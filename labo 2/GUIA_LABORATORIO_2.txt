# GUÍA DE EJECUCIÓN - LABORATORIO 02: SOCKETS UDP Y TRACERT
**Curso:** Redes de Computadoras 2  
**Institución:** Universidad Nacional de San Antonio Abad del Cusco (UNSAAC)  
**Sistema Operativo:** Ubuntu (Linux)

---

## 📁 0. UBICACIÓN DE TUS ARCHIVOS

Todos tus programas están listos en la carpeta:
```bash
cd ~/labo2
```
Archivos disponibles:
* `ServidorUDP.py` : Servidor que recibe texto en minúsculas y lo devuelve en mayúsculas.
* `ClienteUDP.py`  : Cliente interactivo que envía texto al servidor.
* `mi_tracert.py`   : Programa que ejecuta la traza y genera el cuadro de resumen con los saltos.

---

## 🚀 1. PRÁCTICA GUIADA: SERVIDOR Y CLIENTE UDP (Python)

Para esta parte necesitas **dos terminales abiertas**:

### Paso 1.1: En la Terminal 1 (Iniciar Servidor)
Copia y pega este comando:
```bash
python3 ~/labo2/ServidorUDP.py
```
> **Salida esperada:**
> ```text
> El servidor está listo para recibir en el puerto 12000
> ```
*(El servidor se queda esperando datagramas. No lo cierres).*

---

### Paso 1.2: En la Terminal 2 (Ejecutar Cliente)
Copia y pega este comando:
```bash
python3 ~/labo2/ClienteUDP.py
```
1. La terminal te pedirá: `Entrar una sentencia en minúsculas: `
2. Escribe una frase, por ejemplo: `redes de computadoras dos` y presiona **Enter**.
3. **Salida esperada en Terminal 2:**
   ```text
   Socket del servidor = ('127.0.0.1', 12000)
   REDES DE COMPUTADORAS DOS
   ```
4. En la **Terminal 1** verás que el servidor registró el mensaje recibido y el envío de la respuesta.

---

## 🧪 2. EJERCICIO PROPUESTO 5.1: PROBAR CON NETCAT (`nc`)

El objetivo es comprobar que el servidor UDP funciona con herramientas estándar de red sin usar el cliente Python.

Con el `ServidorUDP.py` corriendo en la **Terminal 1**, ejecuta en la **Terminal 2**:

```bash
echo "hola servidor" | nc -u -w1 127.0.0.1 12000
```

> **Salida esperada:**
> ```text
> HOLA SERVIDOR
> ```

### ¿Qué hace cada parámetro?
* `echo "hola servidor"`: El texto que enviamos.
* `|`: Tubería que pasa el texto a Netcat.
* `nc`: Comando Netcat.
* `-u`: Modo **UDP** (por defecto netcat usa TCP).
* `-w1`: Tiempo de espera (*timeout*) de 1 segundo para no quedarse colgado esperando más datos.
* `127.0.0.1`: Dirección IP local (localhost).
* `12000`: Puerto del servidor UDP.

---

## 🌐 3. EJERCICIO PROPUESTO 5.2: INVESTIGACIÓN DE TRACERT (> 30 SALTOS)

### A. Ejecutar el Script con Resumen Automático (Recomendado)
Para obtener la traza y el **cuadro de resumen final de saltos** que revisará el docente, ejecuta:

```bash
python3 ~/labo2/mi_tracert.py 202.116.36.58
```

> **Resultado que verás en pantalla:**
> * Mostrará el recorrido de los 34 saltos desde Perú cruzando EE.UU. y el Océano Pacífico hasta China.
> * Al terminar el salto 34, imprimirá el cuadro de resumen:
> ```text
> ======================================================================
>                     RESUMEN FINAL DE LA TRAZA
> ======================================================================
>  • IP Destino consultada:     202.116.36.58
>  • Total de saltos dados:     34 saltos
>  • Límite por defecto (30):   SUPERADO (>30)
>  • IP en la última línea:     202.116.36.58
>  • ¿Coincide última línea?:   SÍ (VÁLIDO SEGÚN DOCENTE)
>  • Estado final de la traza:  EXITOSA - DESTINO ALCANZADO
> ======================================================================
> ```

---

### B. Si el profesor te pide correr el comando NATIVO del sistema

#### En Ubuntu (Linux):
```bash
traceroute -I -m 45 202.116.36.58
```
* `-I`: Usa paquetes **ICMP Echo Request** (exactamente igual que Windows `tracert`).
* `-m 45`: Modifica el máximo de saltos a 45 (superando el límite por defecto de 30).
* `202.116.36.58`: IP del servidor de destino (*South China Normal University*).

#### En Windows (CMD o PowerShell):
```cmd
tracert -h 45 202.116.36.58
```
* `-h 45`: Modifica el número máximo de saltos en Windows (por defecto es 30).

---

### C. Segunda opción de servidor (Respaldo con 33 saltos):
Si deseas mostrar una segunda prueba con otra universidad lejana:
```bash
python3 ~/labo2/mi_tracert.py 222.197.198.203
```
* Destino: *Kunming University of Science and Technology* (China).
* Total de saltos: **33 saltos** (también supera los 30 saltos por defecto).

---

## 🧠 4. PREGUNTAS CLAVE PARA DEFENDER ANTE EL DOCENTE

1. **¿Por qué la última línea tiene que repetir la IP consultada?**  
   Porque demuestra que el paquete llegó efectivamente a la tarjeta de red del servidor destino y que la búsqueda finalizó con éxito en ese salto.

2. **¿Por qué aparecen asteriscos (`* * *`) en los saltos intermedios?**  
   Porque son routers intermedios cuyos administradores deshabilitaron las respuestas ICMP por políticas de seguridad (firewall) para evitar ataques. No significa que la red esté caída, pues el paquete sigue pasando a los siguientes routers.

3. **¿Por qué fue necesario cambiar el comando por defecto?**  
   Porque por defecto `tracert` en Windows y `traceroute` en Linux tienen un límite prefijado de **30 saltos**. Como este destino requiere **34 saltos**, el comando original se habría detenido en el salto 30 con error. Al poner `-h 45` o `-m 45`, le permitimos continuar hasta la meta.

4. **¿Qué significan siglas como `atl`, `nash`, `dls`, `lax` en la traza?**  
   Son las abreviaturas de las ciudades por donde viaja el cable de fibra óptica: Atlanta, Nashville, Dallas y Los Ángeles, antes de salir por el cable submarino hacia Asia.

---

## 💾 5. COPIAR ARCHIVOS A TU DISCO DE WINDOWS (OPCIONAL)

Si deseas pasar estos archivos a tu carpeta en el disco secundario de Windows:

1. Habilita permisos de escritura en el disco:
   ```bash
   sudo mount -o remount,rw "/run/media/he/SSD-W11-SECUNDARIO"
   ```
2. Copia los archivos:
   ```bash
   cp ~/labo2/* "/run/media/he/SSD-W11-SECUNDARIO/unsaac/redes 2/labo 2/"
   ```
