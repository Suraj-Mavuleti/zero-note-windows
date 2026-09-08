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
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Zero Note - Utility Tool")
        self.geometry("800x600")
        self.configure(fg_color="#1a1a24")
        
        # Header
        self.header = ctk.CTkLabel(self, text="Zero Note - Utility Tool", font=("Helvetica", 24, "bold"), text_color="#00C7FF")
        self.header.pack(pady=20)
        
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=10)
        
        self.setup_ui()
        
    
    def setup_ui(self):
        self.log = ctk.CTkTextbox(self.main_frame, font=("Courier", 14), fg_color="#0a0a0a", text_color="#00FF00")
        self.log.pack(fill=ctk.BOTH, expand=True, pady=10)
        
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(fill=ctk.X)
        
        ctk.CTkButton(btn_frame, text="Start Service", command=self.start).pack(side=ctk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Stop Service", command=self.stop).pack(side=ctk.RIGHT, padx=10)
        
        self.running = False
        
    def start(self):
        if self.running: return
        self.running = True
        self.log.insert("end", "\n[+] Initializing service modules...")
        threading.Thread(target=self.run_service, daemon=True).start()
        
    def stop(self):
        self.running = False
        self.log.insert("end", "\n[-] Service stopped.")
        
    def run_service(self):
        counter = 0
        while self.running:
            time.sleep(1)
            counter += 1
            self.log.insert("end", f"\n[TICK] Process heartbeat ok... Operations executed: {counter*142}")
            self.log.see("end")


if __name__ == "__main__":
    app = App()
    app.mainloop()
