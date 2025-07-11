from login_screen import LoginScreen
from server import Server
from client import Client
import threading
import subprocess
import os
import time
import socket


#מודה שצאט יצר

def start_server_if_not_running():
    def is_server_up():
        try:
            with socket.create_connection(("127.0.0.1", 5050), timeout=1):
                return True
        except:
            return False

    if not is_server_up():
        print("🚀 Starting server...")
        subprocess.Popen(['python', 'server.py'], cwd=os.getcwd())

        # נחכה בלולאה עד שהוא באמת עלה
        for _ in range(20):  # עד 10 שניות (כי יש 0.5 שניות בין כל ניסיון)
            time.sleep(0.5)
            if is_server_up():
                print("✅ Server is now running")
                return
        raise RuntimeError("❌ Failed to start the server")
    else:
        print("✅ Server already running")


if __name__ == "__main__":
    # לפני שמתחילים את הלקוח:
    start_server_if_not_running()
    client = Client()
    app = LoginScreen(client)
