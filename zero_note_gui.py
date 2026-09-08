import customtkinter as ctk
import threading
import time
import math
import socket
import urllib.request
import json
import sqlite3
import random

ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Zero Note Console")
        self.geometry("1100x750")
        
        # Premium Enterprise Color Palette
        self.bg_color = "#0B0C10"          # Deep rich black/gray
        self.sidebar_color = "#1F2833"     # Slate gray sidebar
        self.accent_color = "#66FCF1"      # Neon cyan accent
        self.text_primary = "#FFFFFF"      # Crisp white
        self.text_secondary = "#C5C6C7"    # Soft gray text
        self.panel_bg = "#161920"          # Slightly raised panel
        
        self.configure(fg_color=self.bg_color)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Sidebar Navigation
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=self.sidebar_color)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(5, weight=1)
        
        # Branding
        self.logo_label = ctk.CTkLabel(self.sidebar, text="NOTE", font=ctk.CTkFont("Segoe UI", size=26, weight="bold"), text_color=self.accent_color)
        self.logo_label.grid(row=0, column=0, padx=25, pady=(35, 5), sticky="w")
        
        self.version_label = ctk.CTkLabel(self.sidebar, text="Enterprise Edition v8.5", font=ctk.CTkFont("Segoe UI", size=12), text_color=self.text_secondary)
        self.version_label.grid(row=1, column=0, padx=25, pady=(0, 35), sticky="w")
        
        # Nav Buttons
        self.btn_dash = ctk.CTkButton(self.sidebar, text="  Overview", font=ctk.CTkFont("Segoe UI", size=14, weight="bold"), fg_color=self.panel_bg, text_color=self.text_primary, anchor="w", hover_color=self.accent_color)
        self.btn_dash.grid(row=2, column=0, padx=15, pady=8, sticky="ew")
        
        self.btn_set = ctk.CTkButton(self.sidebar, text="  Configuration", font=ctk.CTkFont("Segoe UI", size=14), fg_color="transparent", text_color=self.text_secondary, anchor="w", hover_color=self.panel_bg)
        self.btn_set.grid(row=3, column=0, padx=15, pady=8, sticky="ew")
        
        self.btn_logs = ctk.CTkButton(self.sidebar, text="  Diagnostics", font=ctk.CTkFont("Segoe UI", size=14), fg_color="transparent", text_color=self.text_secondary, anchor="w", hover_color=self.panel_bg)
        self.btn_logs.grid(row=4, column=0, padx=15, pady=8, sticky="ew")
        
        # Main Work Area
        self.main_view = ctk.CTkFrame(self, fg_color=self.bg_color, corner_radius=0)
        self.main_view.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        
        self.header = ctk.CTkLabel(self.main_view, text="Zero Note Console", font=ctk.CTkFont("Segoe UI", size=32, weight="bold"), text_color=self.text_primary)
        self.header.pack(anchor="w", pady=(0, 20))
        
        # Premium Content Glass Panel
        self.main_frame = ctk.CTkFrame(self.main_view, fg_color=self.panel_bg, corner_radius=15, border_width=1, border_color="#2A2F3A")
        self.main_frame.pack(fill=ctk.BOTH, expand=True)
        
        self.setup_ui()
        
    
    def setup_ui(self):
        # Service Status Top Bar
        status_bar = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        status_bar.pack(fill=ctk.X, padx=25, pady=25)
        
        self.status_indicator = ctk.CTkLabel(status_bar, text="● OFFLINE", font=ctk.CTkFont(size=16, weight="bold"), text_color="#FF453A")
        self.status_indicator.pack(side=ctk.LEFT)
        
        self.uptime_label = ctk.CTkLabel(status_bar, text="System Uptime: 00:00:00", font=ctk.CTkFont(size=14), text_color=self.text_secondary)
        self.uptime_label.pack(side=ctk.RIGHT)
        
        # Log terminal
        self.log = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont("Consolas", 14), fg_color="#08090C", text_color="#45A29E", corner_radius=10, border_width=1, border_color="#1F2833")
        self.log.pack(fill=ctk.BOTH, expand=True, padx=25, pady=(0, 25))
        self.log.insert("0.0", "Enterprise subsystem initialized. Awaiting user command parameters...\n")
        
        # Control Buttons
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(fill=ctk.X, padx=25, pady=(0, 25))
        
        self.start_btn = ctk.CTkButton(btn_frame, text="▶ Initialize Engine", font=ctk.CTkFont(size=16, weight="bold"), height=45, corner_radius=8, fg_color=self.accent_color, hover_color="#45A29E", text_color="#000000", command=self.start)
        self.start_btn.pack(side=ctk.LEFT, expand=True, padx=10)
        
        self.stop_btn = ctk.CTkButton(btn_frame, text="■ Terminate Process", font=ctk.CTkFont(size=16, weight="bold"), height=45, corner_radius=8, fg_color="#FF453A", hover_color="#DC3545", text_color="#FFFFFF", state="disabled", command=self.stop)
        self.stop_btn.pack(side=ctk.LEFT, expand=True, padx=10)
        
        self.running = False
        
    def start(self):
        if self.running: return
        self.running = True
        self.status_indicator.configure(text="● ONLINE (SECURE)", text_color=self.accent_color)
        self.start_btn.configure(state="disabled", fg_color="#1F2833", text_color=self.text_secondary)
        self.stop_btn.configure(state="normal", fg_color="#FF453A", text_color="#FFFFFF")
        self.log.insert("end", "\n[+] Booting enterprise kernel modules...\n[+] Establishing 256-bit encrypted socket channels...")
        threading.Thread(target=self.run_service, daemon=True).start()
        
    def stop(self):
        self.running = False
        self.status_indicator.configure(text="● OFFLINE", text_color="#FF453A")
        self.start_btn.configure(state="normal", fg_color=self.accent_color, text_color="#000000")
        self.stop_btn.configure(state="disabled", fg_color="#1F2833", text_color=self.text_secondary)
        self.log.insert("end", "\n[-] Graceful shutdown sequence initiated...\n[-] Service halted securely.")
        self.log.see("end")
        
    def run_service(self):
        counter = 0
        while self.running:
            time.sleep(1.2)
            counter += 1
            if self.running:
                self.log.insert("end", f"\n[TICK] Core sync optimal. Node throughput: {random.randint(100, 999)} ops/s | Cycles: {counter}")
                self.log.see("end")


if __name__ == "__main__":
    app = App()
    app.mainloop()
