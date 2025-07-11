import socket
import threading

class Client:
    def __init__(self,host = socket.gethostbyname(socket.gethostname()),port = 5050):

        self.HEADER = 64 #גודל ההודעה עד 64 ביטים
        self.PORT = port
        self.FORMAT = 'utf-8' #בהמשך הקוד נראה את זה ממיר לביטים, זאת שיטת קידוד
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = host
        self.ADDR = (self.SERVER, self.PORT)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)

        self.username = ""


    def send(self,msg):
        try:
            message = msg.encode(self.FORMAT)
            message_length = len(message)
            "ממיר את ההודעה ממחרוזת לביטים"
            send_length = str(message_length).encode(self.FORMAT)
            """
            ההודעה ששולחים צריכה להיות בגודל HEADER ואם היא לא נצטרך להוסיף
            מקומות ריקים כמו ' ' להודעה שלנו עד שנגיע לHEADER
            ולכן padded_send_length שווה לכמה ביטים, כלומר כמה מקומות ריקים ' '
            צריך להוסיף למחרוזת שלנו
            לאחר מכן נוסיף לsend_length מקומות ריקים ככמות הpadded_send_length
            b' ' מייצג מקום ריק
            """
            padded_send_length = self.HEADER - len(send_length)
            send_length += b' ' * padded_send_length
            " חייב לשלוח פעמיים כי אחרת השרת לא ידע את גודל ההודעה וזה ייצור קריסה"
            self.client.sendall(send_length)
            self.client.sendall(message)

        except:
            print("[ERROR] couldn't send the message")



    def send_to_server_username(self,user):
        try:
            self.username = user
            #username = input("Enter your username: ")
            if self.username:
                self.send(self.username)
        except:
            print("[ERROR] couldn't send username")

    def listen_to_server(self):
        while True:
            try:
                message_length_that_came_from_server = self.client.recv(self.HEADER).decode(self.FORMAT)
                if message_length_that_came_from_server:  # האם ההודעה חוקית
                    message_length_that_came_from_server = int(message_length_that_came_from_server)  # ממירים לINT את גודל ההודעה כביטים
                    message_that_came_from_server = self.client.recv(message_length_that_came_from_server).decode(self.FORMAT)  # ההודעה עצמה בביטים
                    print(message_that_came_from_server)
            except:
                print("[ERROR] couldn't get the message from the server")
                break




    def start(self):
        self.send_to_server_username()
        threading.Thread(target=self.listen_to_server).start()

        while True:
            msg = input()
            if msg == self.DISCONNECT_MESSAGE:
                self.disconnect()
                break
            else:
                self.send(msg)


    def disconnect(self):
        self.send(self.DISCONNECT_MESSAGE)
        self.client.close()

if __name__ == "__main__":
    client = Client()
    client.start()