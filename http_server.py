#!/usr/bin/env python3
"""
Servidor HTTP para descargar el OSPOS Display.exe y ver la IP
"""
import http.server
import socketserver
import os
import socket

PORT = 8081
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            local_ip = get_local_ip()
            exe_files = [f for f in os.listdir(DIRECTORY)
                         if f.endswith('.exe') or (os.path.isfile(os.path.join(DIRECTORY, f)) and os.access(os.path.join(DIRECTORY, f), os.X_OK) and '.' not in f)]
            
            files_html = ""
            for f in exe_files:
                files_html += f'''
                <div class="file-item">
                    <span class="file-name">📦 {f}</span>
                    <a href="/download/{f}" class="download-btn">⬇️ Descargar</a>
                </div>'''
            
            if not files_html:
                files_html = "<p><em>No hay archivos .exe disponibles</em></p>"
            
            html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>OSPOS - Descarga</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #eaeaea;
        }}
        .container {{
            background: rgba(255,255,255,0.05);
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 90%;
        }}
        h1 {{ color: #00d9ff; margin-bottom: 10px; }}
        .ip-box {{
            background: #2d2d44;
            padding: 15px 20px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
        }}
        .ip-label {{ font-size: 14px; color: #aaa; }}
        .ip-value {{ font-size: 28px; color: #00ff88; font-weight: bold; font-family: Consolas, monospace; }}
        .files {{ margin-top: 25px; }}
        .file-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #2d2d44;
            padding: 15px 20px;
            border-radius: 8px;
            margin: 10px 0;
        }}
        .file-name {{ font-size: 14px; }}
        .download-btn {{
            background: #00d9ff;
            color: #1a1a2e;
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s;
        }}
        .download-btn:hover {{ background: #00ff88; transform: scale(1.05); }}
        .url-box {{
            margin-top: 20px;
            padding: 10px;
            background: #1a1a2e;
            border-radius: 6px;
            font-size: 12px;
            color: #888;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🖥️ OSPOS Display</h1>
        <p>Descarga la aplicación para ver la IP y URL del sistema</p>
        
        <div class="ip-box">
            <div class="ip-label">IP Local del Servidor</div>
            <div class="ip-value">{local_ip}</div>
        </div>
        
        <div class="files">
            <h3>📥 Archivos disponibles:</h3>
            {files_html}
        </div>
        
        <div class="url-box">
            Servidor en puerto {PORT}
        </div>
    </div>
</body>
</html>'''
            self.wfile.write(html.encode())
        elif self.path.startswith("/download/"):
            from urllib.parse import unquote
            filename = unquote(self.path.replace("/download/", ""))
            filepath = os.path.join(DIRECTORY, filename)
            if os.path.exists(filepath):
                self.send_response(200)
                self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
                self.send_header("Content-Length", os.path.getsize(filepath))
                self.end_headers()
                with open(filepath, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "Archivo no encontrado")
        else:
            super().do_GET()

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Servidor HTTP en http://0.0.0.0:{PORT}")
        print(f"IP local: {get_local_ip()}")
        print(f"Directorio: {DIRECTORY}")
        httpd.serve_forever()
