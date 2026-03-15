#!/usr/bin/env python3
"""
OSPOS Display - Muestra la IP local y la URL del sistema OSPOS
"""
import socket
import tkinter as tk
from tkinter import ttk, font

def get_local_ip():
    """Obtiene la IP local de la máquina."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def main():
    local_ip = get_local_ip()
    ospos_url = f"http://{local_ip}:8000"
    
    # Crear ventana principal
    root = tk.Tk()
    root.title("OSPOS - Información del Sistema")
    root.geometry("500x250")
    root.resizable(False, False)
    
    # Centrar ventana
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 500) // 2
    y = (screen_height - 250) // 2
    root.geometry(f"500x250+{x}+{y}")
    
    # Colores
    bg_color = "#1a1a2e"
    fg_color = "#eaeaea"
    accent_color = "#00d9ff"
    
    root.configure(bg=bg_color)
    
    # Fuentes
    title_font = font.Font(family="Segoe UI", size=18, weight="bold")
    ip_font = font.Font(family="Consolas", size=22, weight="bold")
    url_font = font.Font(family="Segoe UI", size=14)
    
    # Título
    title_label = tk.Label(
        root,
        text="🖥️ OSPOS System",
        font=title_font,
        bg=bg_color,
        fg=fg_color
    )
    title_label.pack(pady=(30, 10))
    
    # IP Local
    ip_frame = tk.Frame(root, bg=bg_color)
    ip_frame.pack(pady=10)
    
    ip_label = tk.Label(
        ip_frame,
        text="IP Local:",
        font=url_font,
        bg=bg_color,
        fg=fg_color
    )
    ip_label.pack()
    
    ip_value = tk.Label(
        ip_frame,
        text=local_ip,
        font=ip_font,
        bg=bg_color,
        fg=accent_color
    )
    ip_value.pack()
    
    # URL del sistema
    url_frame = tk.Frame(root, bg=bg_color)
    url_frame.pack(pady=20)
    
    url_label = tk.Label(
        url_frame,
        text="El sistema OSPOS está en:",
        font=url_font,
        bg=bg_color,
        fg=fg_color
    )
    url_label.pack()
    
    url_value = tk.Label(
        url_frame,
        text=ospos_url,
        font=ip_font,
        bg=bg_color,
        fg="#00ff88"
    )
    url_value.pack()
    
    # Botón copiar URL
    def copy_url():
        root.clipboard_clear()
        root.clipboard_append(ospos_url)
        copy_btn.config(text="✓ Copiado!")
        root.after(2000, lambda: copy_btn.config(text="📋 Copiar URL"))
    
    copy_btn = tk.Button(
        root,
        text="📋 Copiar URL",
        font=font.Font(family="Segoe UI", size=10),
        bg="#2d2d44",
        fg=fg_color,
        activebackground="#3d3d5c",
        activeforeground=fg_color,
        command=copy_url,
        relief="flat",
        cursor="hand2"
    )
    copy_btn.pack(pady=10)
    
    # Ejecutar
    root.mainloop()

if __name__ == "__main__":
    main()
