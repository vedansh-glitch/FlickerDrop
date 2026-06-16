import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import qrcode
import os
import threading
import http.server
import socketserver
import socket
import webbrowser
import re
import base64

class FlickerDropBrandedLiquidSuite:
    def __init__(self, root):
        self.root = root
        self.root.title("FlickerDrop Engine v1.0 - iOS Liquid Core")
        self.root.geometry("1050x970") 
        self.root.configure(bg="#0f172a") 
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(5, weight=1) 

        self.selected_file_path = None
        self.qr_cache = []
        self.raw_qr_imgs = [] 
        self.is_streaming = False
        self.is_receiving = False
        self.is_animating = False
        self.httpd = None  
        self.pulse_radius = 12
        self.pulse_direction = 1
        
        self.local_ip = self._get_local_network_host()
        
        # --- iOS LIQUID CIRCULAR ISLAND CORE (CANVAS BASED RENDERING) ---
        self.island_frame = tk.Frame(root, bg="#0f172a", pady=15)
        self.island_frame.grid(row=0, column=0, sticky="ew")
        
        self.island_canvas = tk.Canvas(self.island_frame, width=450, height=65, bg="#1e293b", bd=0, highlightthickness=0)
        self.island_canvas.pack(anchor="center")
        
        self._draw_rounded_pill(225, 32, 210, 24, "#1e293b", outline="")
        self.island_text = self.island_canvas.create_text(85, 32, text="SYSTEM STANDBY // READY FOR DISPATCH", font=("Segoe UI", 10, "bold"), fill="#38bdf8", anchor="w")

        # --- UI HEADER LAYER ---
        header_frame = tk.Frame(root, bg="#1e293b", pady=15, padx=30)
        header_frame.grid(row=1, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)
        
        title_label = tk.Label(header_frame, text="FLICKERDROP PROTOCOL v1.0", font=("Segoe UI", 16, "bold"), fg="#38bdf8", bg="#1e293b")
        title_label.grid(row=0, column=0, sticky="w")
        
        brand_tag = tk.Label(header_frame, text="© VEDANSH_OG // SUITE", font=("Segoe UI", 10, "bold"), fg="#94a3b8", bg="#1e293b")
        brand_tag.grid(row=0, column=1, sticky="e")
        
        # --- MODE TOGGLE LAYER ---
        mode_frame = tk.Frame(root, bg="#0f172a", pady=15, padx=40)
        mode_frame.grid(row=2, column=0, sticky="ew")
        mode_frame.grid_columnconfigure(0, weight=1)
        mode_frame.grid_columnconfigure(1, weight=1)
        
        self.btn_mode_send = tk.Button(mode_frame, text="SEND MODE (PC -> Phone)", font=("Segoe UI", 11, "bold"), fg="#ffffff", bg="#0284c7", bd=0, activebackground="#0369a1", cursor="hand2", command=self.activate_send_mode, pady=12)
        self.btn_mode_send.grid(row=0, column=0, padx=12, sticky="ew")
        
        self.btn_mode_recv = tk.Button(mode_frame, text="RECEIVE MODE (Phone -> PC)", font=("Segoe UI", 11, "bold"), fg="#ffffff", bg="#334155", bd=0, activebackground="#475569", cursor="hand2", command=self.activate_receive_mode, pady=12)
        self.btn_mode_recv.grid(row=0, column=1, padx=12, sticky="ew")

        # --- SELECTION DRAG AND DROP PANELS ---
        self.drop_zone = tk.Label(root, text="DRAG & DROP ANY FILE HERE FOR HIGH-SPEED TRANSFER", font=("Segoe UI", 10, "bold"), fg="#94a3b8", bg="#1e293b", pady=25)
        self.drop_zone.grid(row=3, column=0, padx=40, pady=12, sticky="ew")
        self.drop_zone.config(highlightbackground="#334155", highlightthickness=2)
        
        self.drop_zone.drop_target_register(DND_FILES)
        self.drop_zone.dnd_bind('<<Drop>>', lambda e: self.process_payload_routing(e.data))
        
        self.btn_browse = tk.Button(root, text="CHOOSE TARGET FILE ASSET", font=("Segoe UI", 11, "bold"), fg="#ffffff", bg="#10b981", bd=0, activebackground="#059669", cursor="hand2", command=self.trigger_fallback_explorer, pady=12)
        self.btn_browse.grid(row=4, column=0, padx=40, sticky="ew")

        self.display_label = tk.Label(root, bg="#0f172a", anchor="center")
        self.display_label.grid(row=5, column=0, pady=15, padx=50, sticky="nsew") 

        threading.Thread(target=self.deploy_global_dual_router, daemon=True).start()

    def _get_local_network_host(self):
        socket_scanner = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            socket_scanner.connect(('8.8.8.8', 1))
            local_ip = socket_scanner.getsockname()[0]
        except Exception:
            local_ip = "127.0.0.1"
        finally:
            socket_scanner.close()
        return local_ip

    def check_network_connection(self):
        self.local_ip = self._get_local_network_host()
        if self.local_ip == "127.0.0.1":
            messagebox.showwarning("Network Sync Notice", "Bhai, PC aur Phone ko same Wi-Fi network par rakho\nya phone ka Hotspot on karke PC connect karo!")
            return False
        return True

    def _draw_rounded_pill(self, x, y, w, h, color, outline=""):
        self.island_canvas.create_oval(x-w, y-h, x-w+2*h, y+h, fill=color, outline=outline, tags="pill")
        self.island_canvas.create_oval(x+w-2*h, y-h, x+w, y+h, fill=color, outline=outline, tags="pill")
        self.island_canvas.create_rectangle(x-w+h, y-h, x+w-h, y+h, fill=color, outline=outline, tags="pill")

    def animate_liquid_pipeline(self):
        if not (self.is_streaming or self.is_receiving):
            self.is_animating = False
            return
            
        self.island_canvas.delete("circular_wave")
        self.pulse_radius += 0.8 * self.pulse_direction
        if self.pulse_radius > 16 or self.pulse_radius < 6: self.pulse_direction *= -1
        
        accent_color = "#a855f7" if self.is_streaming else "#10b981"
        status_msg = "BROADCAST READY // SCAN VIA APP" if self.is_streaming else "GATEWAY ACTIVE // STANDBY FILE DROP"
        
        self.island_canvas.create_oval(45-self.pulse_radius, 32-self.pulse_radius, 45+self.pulse_radius, 32+self.pulse_radius, fill="", outline=accent_color, width=2, tags="circular_wave")
        self.island_canvas.create_oval(41, 28, 49, 36, fill=accent_color, outline="", tags="circular_wave") 
        
        self.island_canvas.itemconfig(self.island_text, text=status_msg, fill=accent_color)
        self.root.after(40, self.animate_liquid_pipeline)

    def trigger_fallback_explorer(self):
        if self.is_receiving: return
        file_path = filedialog.askopenfilename(title="Select Asset")
        if file_path: self.process_payload_routing(file_path)

    def activate_send_mode(self):
        self.is_streaming = False
        self.is_receiving = False
        self.btn_mode_send.config(bg="#0284c7")
        self.btn_mode_recv.config(bg="#334155")
        self.btn_browse.config(state=tk.NORMAL, bg="#10b981")
        self.display_label.config(image='')
        self.drop_zone.config(text="DRAG & DROP ANY FILE HERE FOR HIGH-SPEED TRANSFER", fg="#94a3b8", bg="#1e293b")
        self.island_canvas.delete("circular_wave")
        self.island_canvas.itemconfig(self.island_text, text="SYSTEM STANDBY // AIR-GAPPED CORE", fill="#38bdf8")

    def process_payload_routing(self, path_string):
        if self.is_receiving or not self.check_network_connection(): return
        clean_path = path_string.strip('{}')
        if os.path.exists(clean_path):
            self.selected_file_path = clean_path
            self.drop_zone.config(text=f"FILE ACCEPTED: {os.path.basename(clean_path)}", fg="#34d399", bg="#064e3b")
            
            connection_token = f"http://{self.local_ip}:8080/download"
            qr = qrcode.make(connection_token)
            img = ImageTk.PhotoImage(qr.resize((450, 450)))
            self.display_label.config(image=img)
            self.display_label.image = img
            
            self.is_streaming = True
            if not self.is_animating:
                self.is_animating = True
                self.root.after(0, self.animate_liquid_pipeline)

    def activate_receive_mode(self):
        if not self.check_network_connection(): return
        self.is_streaming = False
        self.is_receiving = True
        self.btn_mode_send.config(bg="#334155")
        self.btn_mode_recv.config(bg="#059669")
        self.btn_browse.config(state=tk.DISABLED, bg="#1e293b", fg="#64748b")
        self.drop_zone.config(text="OFFLINE ROUTER ONLINE: Scan the network link token to drop assets", fg="#64748b", bg="#0f172a")
        
        connection_token = f"http://{self.local_ip}:8080/upload"
        qr = qrcode.make(connection_token)
        img = ImageTk.PhotoImage(qr.resize((450, 450)))
        self.display_label.config(image=img)
        self.display_label.image = img
        
        if not self.is_animating:
            self.is_animating = True
            self.root.after(0, self.animate_liquid_pipeline)

    def deploy_global_dual_router(self):
        outer_context = self
        class CoreDualWebDropRouter(http.server.SimpleHTTPRequestHandler):
            def do_GET(this):
                if this.path == "/download" and outer_context.selected_file_path:
                    try:
                        filename = os.path.basename(outer_context.selected_file_path)
                        with open(outer_context.selected_file_path, "rb") as f:
                            file_data = f.read()
                        this.send_response(200)
                        this.send_header("Content-Type", "application/octet-stream")
                        this.send_header("Content-Disposition", f'attachment; filename="{filename}"')
                        this.send_header("Content-Length", str(len(file_data)))
                        this.end_headers()
                        this.wfile.write(file_data)
                        outer_context.root.after(0, lambda: outer_context.context_banner_update(filename, True))
                    except Exception as e:
                        this.send_response(500)
                        this.end_headers()
                        this.wfile.write(str(e).encode('utf-8'))
                else:
                    this.send_response(200)
                    this.end_headers()
                    this.wfile.write("<h1>FlickerDrop Local Router Suite Ready</h1>".encode('utf-8'))

            def do_POST(this):
                try:
                    content_length = int(this.headers['Content-Length'])
                    boundary = this.headers.get_boundary()
                    if not boundary or this.path != "/upload": return
                    raw_body = this.rfile.read(content_length)
                    parts = raw_body.split(b'--' + boundary.encode('utf-8'))
                    
                    original_filename = "flickerdrop_received.png"
                    file_data = b""

                    for part in parts:
                        if b'name="file"' in part:
                            fn_match = re.search(r'filename="([^"]+)"', part.decode('utf-8', errors='ignore'))
                            if fn_match: original_filename = os.path.basename(fn_match.group(1))
                            head_split = part.split(b'\r\n\r\n', 1)
                            if len(head_split) > 1:
                                data_block = head_split[1]
                                if data_block.endswith(b'\r\n'): data_block = data_block[:-2]
                                file_data = data_block
                                break

                    if file_data:
                        try: file_data = base64.b64decode(file_data)
                        except: pass
                        target_workspace = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                        output_path = os.path.join(target_workspace, original_filename)
                        with open(output_path, "wb") as output_buffer:
                            output_buffer.write(file_data)
                            
                        this.send_response(200)
                        this.end_headers()
                        this.wfile.write(b"SUCCESS")
                        outer_context.root.after(0, lambda: messagebox.showinfo("FlickerDrop Master Success", f"File '{original_filename}' landed flawlessly on Desktop natively!"))
                        outer_context.root.after(0, lambda: outer_context.context_banner_update(original_filename, False))
                except: pass

            def log_message(self, format, *args): return 

        socketserver.TCPServer.allow_reuse_address = True
        try:
            with socketserver.TCPServer(("0.0.0.0", 8080), CoreDualWebDropRouter) as synchronized_server:
                outer_context.httpd = synchronized_server
                synchronized_server.serve_forever()
        except: pass

    def context_banner_update(self, filename, is_send):
        self.is_streaming = False
        self.is_receiving = False
        self.island_canvas.delete("circular_wave")
        self.island_canvas.create_oval(37, 24, 53, 40, fill="#10b981", outline="")
        self.island_canvas.itemconfig(self.island_text, text=f"TRANSACTION SUCCESS // COMPLETED: {filename}", fill="#10b981")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = FlickerDropBrandedLiquidSuite(root)
    root.mainloop()
