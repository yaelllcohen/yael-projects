import socket
from idlelib.browser import file_open

class Client:
    def __init__(self,host = socket.gethostbyname(socket.gethostname()),port = 5050):

        self.HEADER = 64 #גודל ההודעה עד 64 ביטים
        self.PORT = port
        self.FORMAT = 'utf-8' #בהמשך הקוד נראה את זה ממיר לביטים, זאת שיטת קידוד
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = host
        self.ADDR = (self.SERVER, self.PORT)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.ADDR)

        self.username = ""

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


    def start(self):
        print("client is running")
        self.upload_file(self.client_socket, r'/file_server_project\avatar.jpeg')


if __name__ == "__main__":
    client = Client()
    client.start()




