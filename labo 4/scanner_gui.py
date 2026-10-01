"""
Aplicación Gráfica del Escáner de Puertos TCP y UDP
Curso: Redes de Computadoras 2 - UNSAAC
Laboratorio 04: Scanner de Puertos TCP, UDP
Autor: Aplicación para Evaluación de Laboratorio
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import csv
import os

from scanner_core import resolve_host, scan_tcp_port, scan_udp_port, get_service_name, COMMON_SERVICES

class PortScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Escáner de Puertos TCP / UDP - UNSAAC Redes 2")
        self.root.geometry("880x680")
        self.root.minsize(780, 560)
        
        # Estado del escáner
        self.is_scanning = False
        self.stop_requested = False
        self.scan_thread = None
        self.results_data = [] # Almacena diccionarios con cada resultado

        # Configurar estilos visuales
        self.setup_styles()
        
        # Construir Interfaz
        self.build_ui()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configuración de colores
        self.bg_color = "#f4f6f9"
        self.card_bg = "#ffffff"
        self.primary_color = "#1a73e8"
        self.success_color = "#2e7d32"
        self.danger_color = "#d32f2f"
        self.text_color = "#202124"
        
        self.root.configure(bg=self.bg_color)
        
        # Estilos ttk
        self.style.configure(".", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 9))
        self.style.configure("TLabel", background=self.bg_color, font=("Segoe UI", 9))
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#0d47a1", background=self.bg_color)
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 9), foreground="#5f6368", background=self.bg_color)
        self.style.configure("Card.TFrame", background=self.card_bg, relief="solid", borderwidth=1)
        self.style.configure("CardLabel.TLabel", background=self.card_bg, font=("Segoe UI", 9, "bold"))
        
        # Botones
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), background=self.primary_color, foreground="white")
        self.style.map("Primary.TButton", background=[("active", "#1557b0"), ("disabled", "#b0bec5")])
        
        self.style.configure("Danger.TButton", font=("Segoe UI", 10, "bold"), background=self.danger_color, foreground="white")
        self.style.map("Danger.TButton", background=[("active", "#b71c1c"), ("disabled", "#b0bec5")])

        # Treeview (Tabla de resultados)
        self.style.configure("Treeview", 
                             background="#ffffff", 
                             foreground=self.text_color, 
                             rowheight=26, 
                             font=("Segoe UI", 9), 
                             fieldbackground="#ffffff")
        self.style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#e8f0fe", foreground="#1a73e8")
        self.style.map("Treeview.Heading", background=[("active", "#d2e3fc")])

    def build_ui(self):
        # 1. ENCABEZADO
        header_frame = ttk.Frame(self.root, padding=(16, 12, 16, 8))
        header_frame.pack(fill="x")
        
        lbl_title = ttk.Label(header_frame, text="Escáner de Puertos TCP y UDP", style="Header.TLabel")
        lbl_title.pack(anchor="w")
        
        lbl_sub = ttk.Label(header_frame, 
                             text="Laboratorio 04 | Redes de Computadoras 2 - UNSAAC | Evaluación en Tiempo Real", 
                             style="SubHeader.TLabel")
        lbl_sub.pack(anchor="w")

        # 2. PANEL DE CONFIGURACIÓN (CARD)
        card_frame = ttk.Frame(self.root, padding=12, style="Card.TFrame")
        card_frame.pack(fill="x", padx=16, pady=6)
        
        # Fila 1: Host / IP y botones de acceso rápido
        row1 = tk.Frame(card_frame, bg=self.card_bg)
        row1.pack(fill="x", pady=4)
        
        tk.Label(row1, text="Host Servidor / Dirección IP:", bg=self.card_bg, font=("Segoe UI", 9, "bold")).pack(side="left")
        
        self.entry_host = ttk.Entry(row1, font=("Segoe UI", 9), width=28)
        self.entry_host.pack(side="left", padx=8)
        self.entry_host.insert(0, "127.0.0.1")
        
        btn_local = tk.Button(row1, text="Localhost (127.0.0.1)", font=("Segoe UI", 8),
                              command=lambda: self.set_host("127.0.0.1"), bg="#e8eaed", relief="flat", cursor="hand2")
        btn_local.pack(side="left", padx=2)
        
        btn_nmap = tk.Button(row1, text="scanme.nmap.org", font=("Segoe UI", 8),
                             command=lambda: self.set_host("scanme.nmap.org"), bg="#e8eaed", relief="flat", cursor="hand2")
        btn_nmap.pack(side="left", padx=4)

        # Fila 2: Rango de Puertos y Protocolo
        row2 = tk.Frame(card_frame, bg=self.card_bg)
        row2.pack(fill="x", pady=6)
        
        tk.Label(row2, text="Puerto Inicial:", bg=self.card_bg, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.entry_port_start = ttk.Entry(row2, font=("Segoe UI", 9), width=8)
        self.entry_port_start.pack(side="left", padx=(6, 16))
        self.entry_port_start.insert(0, "5020")
        
        tk.Label(row2, text="Puerto Final:", bg=self.card_bg, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.entry_port_end = ttk.Entry(row2, font=("Segoe UI", 9), width=8)
        self.entry_port_end.pack(side="left", padx=(6, 20))
        self.entry_port_end.insert(0, "5040")
        
        # Selector de Protocolo
        tk.Label(row2, text="Protocolo:", bg=self.card_bg, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.protocol_var = tk.StringVar(value="TCP")
        
        rb_tcp = tk.Radiobutton(row2, text="TCP", variable=self.protocol_var, value="TCP", bg=self.card_bg, font=("Segoe UI", 9))
        rb_tcp.pack(side="left", padx=4)
        
        rb_udp = tk.Radiobutton(row2, text="UDP", variable=self.protocol_var, value="UDP", bg=self.card_bg, font=("Segoe UI", 9))
        rb_udp.pack(side="left", padx=4)
        
        rb_both = tk.Radiobutton(row2, text="Ambos (TCP y UDP)", variable=self.protocol_var, value="AMBOS", bg=self.card_bg, font=("Segoe UI", 9))
        rb_both.pack(side="left", padx=4)

        # Fila 3: Opciones Avanzadas (Timeout, Concurrencia e Hilos)
        row3 = tk.Frame(card_frame, bg=self.card_bg)
        row3.pack(fill="x", pady=4)
        
        tk.Label(row3, text="Timeout (seg):", bg=self.card_bg).pack(side="left")
        self.combo_timeout = ttk.Combobox(row3, values=["0.3", "0.5", "0.8", "1.0", "1.5", "2.0"], width=5, state="readonly")
        self.combo_timeout.set("0.8")
        self.combo_timeout.pack(side="left", padx=(4, 16))
        
        tk.Label(row3, text="Hilos paralelos:", bg=self.card_bg).pack(side="left")
        self.spin_threads = ttk.Spinbox(row3, from_=1, to=100, width=5)
        self.spin_threads.set("20")
        self.spin_threads.pack(side="left", padx=(4, 20))
        
        self.check_only_open = tk.BooleanVar(value=False)
        chk_open = tk.Checkbutton(row3, text="Ocultar cerrados (Mostrar solo abiertos)", 
                                  variable=self.check_only_open, bg=self.card_bg, 
                                  command=self.refresh_table_view)
        chk_open.pack(side="left", padx=8)

        # 3. BARRA DE BOTONES DE ACCIÓN
        action_frame = ttk.Frame(self.root, padding=(16, 4, 16, 4))
        action_frame.pack(fill="x")
        
        self.btn_start = ttk.Button(action_frame, text="▶ Iniciar Escaneo", style="Primary.TButton", command=self.start_scan)
        self.btn_start.pack(side="left", padx=(0, 8), ipadx=10, ipady=4)
        
        self.btn_stop = ttk.Button(action_frame, text="⏹ Detener", style="Danger.TButton", command=self.stop_scan, state="disabled")
        self.btn_stop.pack(side="left", padx=4, ipadx=8, ipady=4)
        
        self.btn_clear = ttk.Button(action_frame, text="🧹 Limpiar", command=self.clear_results)
        self.btn_clear.pack(side="left", padx=4, ipady=4)
        
        self.btn_export = ttk.Button(action_frame, text="💾 Exportar Resultados (.txt / .csv)", command=self.export_results)
        self.btn_export.pack(side="right", padx=0, ipady=4)

        # 4. BARRA DE PROGRESO Y BANNER DE ESTADO EN VIVO
        progress_frame = ttk.Frame(self.root, padding=(16, 6, 16, 4))
        progress_frame.pack(fill="x")
        
        self.prog_bar = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate")
        self.prog_bar.pack(fill="x", pady=2)
        
        # Banner de estado dinámico y elegante (sin popups bloqueantes)
        self.status_banner = tk.Frame(progress_frame, bg="#ffffff", bd=1, relief="solid", padx=10, pady=6)
        self.status_banner.pack(fill="x", pady=4)
        
        self.lbl_status = tk.Label(self.status_banner, 
                                   text="Listo para escanear. Ingrese los datos del servidor y presione 'Iniciar Escaneo'.", 
                                   bg="#ffffff", fg="#3c4043", font=("Segoe UI", 9, "bold"), anchor="w")
        self.lbl_status.pack(fill="x")

        # 5. TABLA DE RESULTADOS (TREEVIEW)
        table_frame = ttk.Frame(self.root, padding=(16, 4, 16, 12))
        table_frame.pack(fill="both", expand=True)
        
        columns = ("puerto", "protocolo", "estado", "servicio", "tiempo", "detalle")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("puerto", text="Puerto", command=lambda: self.sort_column("puerto", False))
        self.tree.heading("protocolo", text="Protocolo", command=lambda: self.sort_column("protocolo", False))
        self.tree.heading("estado", text="Estado", command=lambda: self.sort_column("estado", False))
        self.tree.heading("servicio", text="Servicio Conocido", command=lambda: self.sort_column("servicio", False))
        self.tree.heading("tiempo", text="Latencia (ms)", command=lambda: self.sort_column("tiempo", False))
        self.tree.heading("detalle", text="Detalle Técnico de Respuesta")
        
        self.tree.column("puerto", width=80, anchor="center")
        self.tree.column("protocolo", width=85, anchor="center")
        self.tree.column("estado", width=130, anchor="center")
        self.tree.column("servicio", width=140, anchor="w")
        self.tree.column("tiempo", width=95, anchor="e")
        self.tree.column("detalle", width=290, anchor="w")
        
        # Tags de colores para las filas
        self.tree.tag_configure("ABIERTO", background="#e6f4ea", foreground="#137333")          # Verde claro
        self.tree.tag_configure("FILTRADO", background="#fef7e0", foreground="#b06000")         # Ámbar/Amarillo
        self.tree.tag_configure("CERRADO", background="#fdf2f2", foreground="#c5221f")          # Rojo claro / Gris
        self.tree.tag_configure("ERROR", background="#fce8e6", foreground="#d93025")
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # 6. PIE DE PÁGINA (ESTADÍSTICAS EN TIEMPO REAL)
        footer_frame = ttk.Frame(self.root, padding=(16, 2, 16, 8))
        footer_frame.pack(fill="x")
        
        self.lbl_stats = ttk.Label(footer_frame, 
                                   text="Puertos totales: 0 | Abiertos: 0 | Cerrados/Filtrados: 0 | Duración: 0.0s", 
                                   font=("Segoe UI", 9, "bold"), foreground="#3c4043")
        self.lbl_stats.pack(anchor="w")

    def set_host(self, host_val):
        self.entry_host.delete(0, tk.END)
        self.entry_host.insert(0, host_val)

    def validate_inputs(self):
        host = self.entry_host.get().strip()
        if not host:
            messagebox.showerror("Dato Inválido", "Por favor ingrese el nombre del Host o la dirección IP.")
            return None

        try:
            p_start = int(self.entry_port_start.get().strip())
            p_end = int(self.entry_port_end.get().strip())
        except ValueError:
            messagebox.showerror("Dato Inválido", "Los números de puerto deben ser valores numéricos enteros.")
            return None

        if not (1 <= p_start <= 65535) or not (1 <= p_end <= 65535):
            messagebox.showerror("Rango Inválido", "Los puertos deben estar en el rango válido entre 1 y 65535.")
            return None

        if p_start > p_end:
            messagebox.showerror("Rango Inválido", "El puerto inicial no puede ser mayor que el puerto final.")
            return None

        total_ports = p_end - p_start + 1
        if total_ports > 5000:
            if not messagebox.askyesno("Rango Amplio", f"Ha seleccionado escanear {total_ports} puertos. Esto puede tardar varios minutos. ¿Desea continuar?"):
                return None

        try:
            timeout_val = float(self.combo_timeout.get())
        except ValueError:
            timeout_val = 0.8

        try:
            threads_val = int(self.spin_threads.get())
            if threads_val < 1:
                threads_val = 1
        except ValueError:
            threads_val = 20

        return {
            "host": host,
            "start": p_start,
            "end": p_end,
            "protocol": self.protocol_var.get(),
            "timeout": timeout_val,
            "threads": threads_val
        }

    def start_scan(self):
        config = self.validate_inputs()
        if not config:
            return

        # Limpiar resultados anteriores
        self.results_data.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.is_scanning = True
        self.stop_requested = False
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.prog_bar["value"] = 0

        # Lanzar escaneo en hilo de fondo para mantener la GUI interactiva
        self.status_banner.configure(bg="#e8f0fe")
        self.lbl_status.configure(
            text="⚡ Iniciando motor de escaneo... Preparando sockets.", 
            bg="#e8f0fe", fg="#1a73e8"
        )
        self.scan_thread = threading.Thread(target=self._scan_worker, args=(config,), daemon=True)
        self.scan_thread.start()

    def stop_scan(self):
        if self.is_scanning:
            self.stop_requested = True
            self.status_banner.configure(bg="#fef7e0")
            self.lbl_status.configure(
                text="⏳ Deteniendo escaneo... Finalizando hilos activos.", 
                bg="#fef7e0", fg="#b06000"
            )
            self.btn_stop.configure(state="disabled")

    def _scan_worker(self, config):
        host = config["host"]
        p_start = config["start"]
        p_end = config["end"]
        proto = config["protocol"]
        timeout_val = config["timeout"]
        threads_count = config["threads"]

        self.root.after(0, lambda: self.lbl_status.configure(
            text=f"🔍 Resolviendo host '{host}'...", 
            bg="#e8f0fe", fg="#1a73e8"
        ))
        target_ip, err = resolve_host(host)
        if err:
            self.root.after(0, lambda: messagebox.showerror("Error de Red", err))
            self.root.after(0, self._on_scan_finished, False)
            return

        self.root.after(0, lambda: self.lbl_status.configure(
            text=f"⚡ Analizando objetivo {target_ip} ({host}) | Rango: {p_start} a {p_end} | Protocolo: {proto}",
            bg="#e8f0fe", fg="#1a73e8"
        ))

        # Crear lista ordenada de tareas
        task_list = []
        for port in range(p_start, p_end + 1):
            if proto in ("TCP", "AMBOS"):
                task_list.append((port, "TCP"))
            if proto in ("UDP", "AMBOS"):
                task_list.append((port, "UDP"))

        total_tasks = len(task_list)
        completed = 0
        open_count = 0
        t_start = time.time()

        from concurrent.futures import ThreadPoolExecutor, as_completed

        def execute_probe(item):
            if self.stop_requested:
                return None
            port_num, protocol_name = item
            if protocol_name == "TCP":
                return scan_tcp_port(target_ip, port_num, timeout_val)
            else:
                return scan_udp_port(target_ip, port_num, timeout_val)

        with ThreadPoolExecutor(max_workers=threads_count) as executor:
            future_to_task = {executor.submit(execute_probe, task): task for task in task_list}
            
            for future in as_completed(future_to_task):
                if self.stop_requested:
                    break
                try:
                    res = future.result()
                    if res:
                        completed += 1
                        if res["estado"] == "ABIERTO":
                            open_count += 1
                        
                        self.root.after(0, self._add_result_row, res, completed, total_tasks, t_start, open_count)
                except Exception:
                    completed += 1

        was_cancelled = self.stop_requested
        elapsed = time.time() - t_start
        self.root.after(0, self._on_scan_finished, True, was_cancelled, total_tasks, completed, open_count, elapsed)

    def _add_result_row(self, res, current, total, t_start, open_count):
        self.results_data.append(res)
        
        pct = (current / total) * 100 if total > 0 else 0
        self.prog_bar["value"] = pct
        
        elapsed = time.time() - t_start
        cerrados = current - open_count
        self.lbl_stats.configure(
            text=f"Puertos analizados: {current}/{total} ({pct:.1f}%) | Abiertos confirmados: {open_count} | Cerrados/Filtrados: {cerrados} | Tiempo: {elapsed:.1f}s"
        )
        self.lbl_status.configure(
            text=f"⚡ Analizando: Puerto {res['puerto']} {res['protocolo']} -> {res['estado']} ({current}/{total})",
            bg="#e8f0fe", fg="#1a73e8"
        )

        if self.check_only_open.get() and res["estado"] != "ABIERTO":
            return

        tag = "ABIERTO" if res["estado"] == "ABIERTO" else ("FILTRADO" if "FILTRADO" in res["estado"] else "CERRADO")
        self.tree.insert("", "end", values=(
            res["puerto"],
            res["protocolo"],
            res["estado"],
            res["servicio"],
            f"{res['tiempo_ms']:.1f}",
            res["detalle"]
        ), tags=(tag,))

    def _on_scan_finished(self, success, was_cancelled=False, total=0, completed=0, open_count=0, elapsed=0.0):
        self.is_scanning = False
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")

        if not success:
            self.status_banner.configure(bg="#fce8e6")
            self.lbl_status.configure(
                text="❌ Error: El escaneo no pudo completarse. Verifique la dirección del Host.",
                bg="#fce8e6", fg="#c5221f"
            )
            return

        cerrados = completed - open_count
        if was_cancelled:
            self.status_banner.configure(bg="#fef7e0")
            self.lbl_status.configure(
                text=f"⏹ Escaneo detenido por el usuario | {completed} de {total} puertos analizados | {open_count} Abiertos confirmados | {cerrados} Cerrados/Filtrados",
                bg="#fef7e0", fg="#b06000"
            )
        else:
            self.prog_bar["value"] = 100
            self.status_banner.configure(bg="#e6f4ea")
            self.lbl_status.configure(
                text=f"✔ Escaneo completado: {completed} puertos analizados | {open_count} ABIERTOS confirmados | {cerrados} CERRADOS/FILTRADOS | Duración: {elapsed:.2f} s",
                bg="#e6f4ea", fg="#137333"
            )
            self.refresh_table_view()

    def refresh_table_view(self):
        # Limpiar treeview y repoblar según el filtro y ordenados numéricamente
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Ordenar por puerto numéricamente
        sorted_data = sorted(self.results_data, key=lambda x: (x["puerto"], x["protocolo"]))
        
        for res in sorted_data:
            if self.check_only_open.get() and res["estado"] != "ABIERTO":
                continue
            tag = "ABIERTO" if res["estado"] == "ABIERTO" else ("FILTRADO" if "FILTRADO" in res["estado"] else "CERRADO")
            self.tree.insert("", "end", values=(
                res["puerto"],
                res["protocolo"],
                res["estado"],
                res["servicio"],
                f"{res['tiempo_ms']:.1f}",
                res["detalle"]
            ), tags=(tag,))

    def sort_column(self, col, reverse):
        # Permitir ordenar haciendo clic en los encabezados
        data_list = []
        for child in self.tree.get_children(''):
            val = self.tree.set(child, col)
            if col in ("puerto", "tiempo"):
                try:
                    val = float(val)
                except ValueError:
                    pass
            data_list.append((val, child))

        data_list.sort(reverse=reverse)
        for index, (_, child) in enumerate(data_list):
            self.tree.move(child, '', index)

        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def clear_results(self):
        if self.is_scanning:
            messagebox.showwarning("Atención", "No se puede limpiar la tabla mientras el escaneo está en ejecución.")
            return
        self.results_data.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.status_banner.configure(bg="#ffffff")
        self.lbl_status.configure(
            text="Listo para escanear. Ingrese los datos del servidor y presione 'Iniciar Escaneo'.",
            bg="#ffffff", fg="#3c4043"
        )
        self.lbl_stats.configure(text="Puertos totales: 0 | Abiertos: 0 | Cerrados/Filtrados: 0 | Duración: 0.0s")

    def export_results(self):
        if not self.results_data:
            messagebox.showwarning("Sin Datos", "No hay resultados para exportar. Realice un escaneo primero.")
            return

        file_types = [("Archivo de Texto (*.txt)", "*.txt"), ("Archivo CSV (*.csv)", "*.csv")]
        file_path = filedialog.asksaveasfilename(
            title="Guardar Resultados del Escaneo",
            defaultextension=".txt",
            filetypes=file_types,
            initialfile=f"escaneo_reporte_{int(time.time())}.txt"
        )

        if not file_path:
            return

        try:
            sorted_data = sorted(self.results_data, key=lambda x: (x["puerto"], x["protocolo"]))
            if file_path.endswith(".csv"):
                with open(file_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Puerto", "Protocolo", "Estado", "Servicio", "Tiempo_ms", "Detalle"])
                    for r in sorted_data:
                        writer.writerow([r["puerto"], r["protocolo"], r["estado"], r["servicio"], r["tiempo_ms"], r["detalle"]])
            else:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("=" * 70 + "\n")
                    f.write("   UNSAAC - REDES DE COMPUTADORAS 2 - REPORTE DE ESCANEO DE PUERTOS\n")
                    f.write("=" * 70 + "\n")
                    f.write(f"Fecha de reporte : {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Host analizado   : {self.entry_host.get().strip()}\n")
                    f.write(f"Rango de puertos : {self.entry_port_start.get().strip()} a {self.entry_port_end.get().strip()}\n")
                    f.write(f"Protocolo        : {self.protocol_var.get()}\n")
                    f.write("-" * 70 + "\n")
                    f.write(f"{'PUERTO':<10}{'PROTO':<10}{'ESTADO':<20}{'SERVICIO':<18}{'DETALLE'}\n")
                    f.write("-" * 70 + "\n")
                    for r in sorted_data:
                        f.write(f"{r['puerto']:<10}{r['protocolo']:<10}{r['estado']:<20}{r['servicio']:<18}{r['detalle']}\n")
                    f.write("=" * 70 + "\n")

            messagebox.showinfo("Exportación Exitosa", f"Los resultados han sido guardados correctamente en:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error al Exportar", f"Ocurrió un error al guardar el archivo: {str(e)}")

def main():
    root = tk.Tk()
    app = PortScannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
