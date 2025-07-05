import socket
import threading

HEADER = 64 #גודל ההודעה עד 64 ביטים
PORT = 5050
FORMAT = 'utf-8' #בהמשך הקוד נראה את זה ממיר לביטים, זאת שיטת קידוד
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    message_length = len(message)
    "ממיר את ההודעה ממחרוזת לביטים"
    send_length = str(message_length).encode(FORMAT)
    """
    ההודעה ששולחים צריכה להיות בגודל HEADER ואם היא לא נצטרך להוסיף
    מקומות ריקים כמו ' ' להודעה שלנו עד שנגיע לHEADER
    ולכן padded_send_length שווה לכמה ביטים, כלומר כמה מקומות ריקים ' '
    צריך להוסיף למחרוזת שלנו
    לאחר מכן נוסיף לsend_length מקומות ריקים ככמות הpadded_send_length
    b' ' מייצג מקום ריק
    """
    padded_send_length = HEADER - len(send_length)
    send_length += b' ' * padded_send_length
    " חייב לשלוח פעמיים כי אחרת השרת לא ידע את גודל ההודעה וזה ייצור קריסה"
    client.send(send_length)
    client.send(message)



def listen_to_server():
    while True:
        try:
            message_length_that_came_from_server = client.recv(HEADER).decode(FORMAT)
            if message_length_that_came_from_server:  # האם ההודעה חוקית
                message_length_that_came_from_server = int(message_length_that_came_from_server)  # ממירים לINT את גודל ההודעה כביטים
                message_that_came_from_server = client.recv(message_length_that_came_from_server).decode(FORMAT)  # ההודעה עצמה בביטים
                print(f" [BOT] {message_that_came_from_server}")
        except:
            print("[ERROR] couldn't get the message from the server")
            break

def start():
    threading.Thread(target=listen_to_server).start()

    while True:
        message = input()
        if message == DISCONNECT_MESSAGE:
            send(DISCONNECT_MESSAGE)
            break
        else:
            send(message)

if __name__ == "__main__":
    start()