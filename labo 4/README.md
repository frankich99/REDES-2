# Laboratorio 04: Scanner de Puertos TCP y UDP
**Asignatura:** Redes de Computadoras 2  
**Institución:** Universidad Nacional de San Antonio Abad del Cusco (UNSAAC)  
**Entorno de desarrollo:** Python 3.12+ (Windows 10 / Ubuntu)  

---

## 📁 Estructura del Proyecto

```text
├── scanner_core.py        # Motor de escaneo (Sockets TCP/UDP, hilos, resolución DNS, payloads)
├── scanner_gui.py         # Interfaz Gráfica interactiva (Tkinter, tabla en vivo, filtros, exportación)
├── test_server.py         # Servidor local para simular la evaluación del docente (Puertos 5020-5040)
└── INFORME_LAB04...md     # Estructura completa del Informe para entrega en PDF
```

---

## 🚀 Guía Rápida de Ejecución

### 1. Ejecutar el Escáner con Interfaz Gráfica (GUI)
Abre una terminal (PowerShell o CMD) en esta carpeta y ejecuta:

```powershell
python scanner_gui.py
```

### 2. Simular la Evaluación del Docente en Localhost
Para entrenar antes de la clase y verificar que tu programa acierte el 100% de los puertos del docente:

1. **Terminal 1 (Servidor de prueba):**
   ```powershell
   python test_server.py
   ```
   *Este servidor abrirá deliberadamente:*
   * **TCP:** 5024, 5026, 5030, 5035
   * **UDP:** 5024, 5028, 5032
   * *Todos los demás puertos entre 5020 y 5040 permanecerán cerrados.*

2. **Terminal 2 (Escáner Gráfico):**
   ```powershell
   python scanner_gui.py
   ```
   * En Host coloca: `127.0.0.1`
   * Rango: `5020` a `5040`
   * Prueba primero seleccionando **TCP** y pulsa **Iniciar Escaneo**.
   * Luego prueba seleccionando **UDP** y pulsa **Iniciar Escaneo**.
   * Verifica cómo la tabla muestra exactamente los puertos abiertos en verde y los cerrados en rojo.
