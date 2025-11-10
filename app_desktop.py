import time
import webview
import threading
import os
import sys
import subprocess
from pathlib import Path

def run_streamlit():
    base_dir = Path(__file__).resolve().parent
    script_path = base_dir / "app.py"
    
    # Configurar variable de entorno para detectar WebView
    os.environ['STREAMLIT_IN_WEBVIEW'] = 'true'
    
    # Crear archivo marker en temp para detección más confiable
    import tempfile
    marker_file = Path(tempfile.gettempdir()) / '.streamlit_webview_marker'
    try:
        marker_file.touch()
    except:
        pass

    # Asegúrate de usar el mismo Python
    cmd = [
        sys.executable, "-m", "streamlit", "run", str(script_path),
        "--server.headless=true",
        "--server.port=8501",
        "--server.address=127.0.0.1",
        "--browser.gatherUsageStats=false"
    ]
    
    # Pasar la variable de entorno al subproceso
    env = os.environ.copy()
    env['STREAMLIT_IN_WEBVIEW'] = 'true'
    
    # Establece cwd para que los paths relativos funcionen
    subprocess.Popen(cmd, cwd=str(base_dir), shell=False, env=env)

# Inicia Streamlit en un hilo
threading.Thread(target=run_streamlit, daemon=True).start()

# Espera unos segundos para asegurarse de que Streamlit arranque
time.sleep(2)

# Crea la ventana de escritorio con pywebview
webview.create_window("Mi App Streamlit", "http://localhost:8501")
webview.start()