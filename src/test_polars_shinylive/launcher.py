"""Desktop launcher for the Shiny app.

This script is used by PyInstaller to create a standalone executable.
It starts the Shiny server and opens the app in an embedded webview window.
Falls back to system browser on Linux/WSL where GTK/QT may not be available.
"""

import os
import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError


def find_free_port() -> int:
    """Find a free port to run the server on."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def wait_for_server(url: str, timeout: float = 30.0) -> bool:
    """Wait until the server is responding, or timeout."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            urlopen(url, timeout=1)
            return True
        except URLError:
            time.sleep(0.2)
    return False


def run_server(app_dir: Path, port: int) -> None:
    """Run the Shiny server."""
    os.chdir(app_dir)
    sys.path.insert(0, str(app_dir))

    from shiny._main import run_app

    run_app(
        app="app.py",
        host="localhost",
        port=port,
        reload=False,
        launch_browser=False,
    )


def try_webview(url: str) -> bool:
    """Try to open app in native webview window. Returns False if unavailable."""
    try:
        import webview

        window = webview.create_window(
            title="Penguins Dashboard",
            url=url,
            width=1200,
            height=800,
        )
        webview.start()
        return True
    except Exception:
        return False


def main() -> None:
    # Determine the app directory (works both in dev and when bundled)
    if getattr(sys, "frozen", False):
        # Running as PyInstaller bundle
        app_dir = Path(sys._MEIPASS) / "app"

        # Redirect stdout/stderr to devnull in windowed mode (no console)
        # This prevents pywebview crashes when there's no console to write to
        if sys.stdout is None:
            sys.stdout = open(os.devnull, "w")
        if sys.stderr is None:
            sys.stderr = open(os.devnull, "w")
    else:
        # Running as script
        app_dir = Path(__file__).parent

    port = find_free_port()
    url = f"http://localhost:{port}"

    # Start server in background thread
    server_thread = threading.Thread(
        target=run_server, args=(app_dir, port), daemon=True
    )
    server_thread.start()

    # Wait for server to be ready
    if not wait_for_server(url):
        print("Error: Server failed to start")
        sys.exit(1)

    # Try native window first (works on Windows), fall back to browser
    if not try_webview(url):
        print(f"Opening in browser: {url}")
        print("Press Ctrl+C to stop the server.")
        webbrowser.open(url)
        # Keep main thread alive for browser mode
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")


if __name__ == "__main__":
    main()