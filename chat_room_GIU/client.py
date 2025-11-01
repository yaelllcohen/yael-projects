import socket
import threading
from rsa_keys import RsaKeys
import rsa

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

        self.keys = RsaKeys()

        with open("keys/public_key.pem", "rb") as f:
            self.server_public = rsa.PublicKey.load_pkcs1(f.read())

    def send(self,msg):
        try:
            cipher_text = self.keys.encrypt(msg, self.server_public)
            #message = msg.encode(self.FORMAT)
            message_length = len(cipher_text)
            "ממיר את גודל ההודעה ממחרוזת לביטים"
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
            self.client.sendall(cipher_text)

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

    def send_to_server_public_key(self):
        try:
            public_key_pem = self.keys.public_key.save_pkcs1('PEM')
            public_key_length = str(len(public_key_pem)).encode(self.FORMAT)
            padded_send_length = self.HEADER - len(public_key_length)
            public_key_length += b' ' * padded_send_length
            self.client.sendall(public_key_length)
            self.client.sendall(public_key_pem)
        except:
            print("couldnt send the public key")

    def listen_to_server(self):
        while True:
            try:
                message_length_that_came_from_server = self.client.recv(self.HEADER).decode(self.FORMAT)
                if message_length_that_came_from_server:  # האם ההודעה חוקית
                    message_length_that_came_from_server = int(message_length_that_came_from_server)  # ממירים לINT את גודל ההודעה כביטים

                    cipher_bytes = self.client.recv(message_length_that_came_from_server)# ההודעה המוצפנת בביטים
                    plain_text = self.keys.decrypt(cipher_bytes, self.keys.private_key)

                    print(plain_text)
            except:
                print("[ERROR] couldn't get the message from the server or decrpypt server message")
                break




    def start(self):
        self.send_to_server_username(self.username)
        self.send_to_server_public_key()
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