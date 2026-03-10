import socket


# import threading
#
class Server:
    def __init__(self, host = '0.0.0.0', port = 5050):

        #Create a TCP/IP socket
        #AF_INET - IP4
        #SOCK_STREAM - TCP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.PORT = port
        self.HOST = host
        self.ADDR = self.HOST, self.PORT
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.LISTENING_LIMIT = 5
        self.server_socket.bind(self.ADDR)
        self.connections = [] #שיתאים לכמה משתמשים







    def download_file(self, client_socket, destination_file_path):
        """
        קובץ לרוב גדול מ1024 ביטים ולכן צריך לחלק אותו ליחידות מידע
        ולכן נבצע את זה בלולאה. כל עוד יש מידע נמשיך לחלק את הקובץ
        ל1024 ביטים
        """
        chunk = client_socket.recv(1024)
        with open(destination_file_path, 'wb') as file:
            while chunk:
                file.write(chunk)
                chunk = client_socket.recv(1024)
            print("finish getting bytes")


    def upload_file(self, client_socket, file_path):
        """
        קובץ לרוב גדול מ1024 ביטים ולכן צריך לחלק אותו ליחידות מידע
        ולכן נבצע את זה בלולאה. כל עוד יש מידע נמשיך לחלק את הקובץ
        ל1024 ביטים
        """
        with open(file_path, 'rb') as file:
            data = file.read(1024)
            while data:
                client_socket.sendall(data)
                data = file.read(1024)
            print("finish sending bytes")



    def start(self):
        print("[STARTING] server is starting......")
        self.server_socket.listen(self.LISTENING_LIMIT)
        print(f"[LISTENING] listening on server {self.HOST}")
        client_socket, addr = self.server_socket.accept()
        print(addr)
        print("accepted new connection")
        self.download_file(client_socket, r"/file_server_project\avatar_recive.jpeg")





if __name__ == "__main__":

    server = Server()
    server.start()





