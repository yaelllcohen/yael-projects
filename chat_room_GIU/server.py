import socket
import threading

class Server:
    def __init__(self, host= '0.0.0.0', port=5050):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HEADER = 64 # גודל ההודעה עד 64 ביטים
        self.PORT = port
        self.SERVER = host
        self.ADDR = (host, port)  # הכתובת המורכבת מפורט וIP בטאפל
        self.FORMAT = 'utf-8'  # בהמשך הקוד נראה את זה ממיר לביטים, זאת שיטת קידוד
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.LISTENING_LIMIT = 5
        """
        יצרתי סוקט 
        AF_INET אומר שזה לפי IPV4
        SOCK_STREAM אומר שזה לפי פרוטוקול TCP
        """
        self.server.bind(self.ADDR)  # הוא מכריז על כתובת, כולמר שקיים כתובת כדי שיגיעו בקשות
        self.connections = []

    def receive_username(self, conn,username):
        is_connected = True
        while is_connected:
            """
            connect.recv(HEADER) מקבל מהלקוח את ההודעה עד גודל HEADER
            HEADER זה גודל ההודעה כ64 ביטים
            decode(FORMAT) ממיר את ההודעה מביטים למחרוזת
            כלומר סהכ אנחנו רוצים את גודל ההודעה
            """
            try:
                message_length = conn.recv(self.HEADER).decode(self.FORMAT)
                if message_length:  # האם ההודעה חוקית
                    message_length = int(message_length)  # ממירים לINT את גודל ההודעה כביטים
                    message = conn.recv(message_length).decode(self.FORMAT)  # ההודעה עצמה בביטים
                    if message == self.DISCONNECT_MESSAGE:
                        is_connected = False
                        print(f"{username} disconnected")

                    print(f"[{username}] {message}")
                    final_msg = f"[{username}]  {message}"
                    self.broadcast(final_msg, conn)
            except:
                print(f"[ERROR] the connection with {username} failed")
                is_connected = False

        conn.close()  # סוגר את החיבור, את הסוקט
        if conn in self.connections:  # כשהלקוח התנתק מהרשימה של החיבורים הפעילים
            self.connections.remove(conn)


    def send_to_client(self, msg, conn):
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
            conn.sendall(send_length)
            conn.sendall(message)
        except:
            print(f"[ERROR] Failed to send message to a client")
            if conn in self.connections:  # כשהלקוח התנתק מהרשימה של החיבורים הפעילים
                self.connections.remove(conn)


    #לקבל הודעה מלקוח אחד ולשלוח אותה לכל הלקוחות המחוברים בשרת
    def broadcast(self, message, source_connection):
            for connection in self.connections:
                if connection != source_connection:
                    self.send_to_client(message,connection)

            print(f"[BROADCAST] Sent to {len(self.connections) - 1} clients")


    "הפונקציה נועדה לטפל בחיבור הבודד בין הלקוח לשרת"
    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTING] {addr} connect")
        # קבלת שם משתמש בהודעה הראשונה
        try:
            username_length = conn.recv(self.HEADER).decode(self.FORMAT)
            if username_length:
                username_length = int(username_length)
                username = conn.recv(username_length).decode(self.FORMAT)
                print(f"[USERNAME RECEIVED] {username} from {addr}")
            else:
                username = f"{addr}"  # fallback אם לא התקבל שם

            self.connections.append(conn)
            thread = threading.Thread(target=self.receive_username, args=(conn, username))
            thread.start()
        except:
            print(f"[ERROR] failed to receive username from {addr}")
            conn.close()


    " הפונקציה נועדה לטפל בחיבורים חדשים ולחלק אותם לאן שהם צריכים להגיע"

    def start(self):
        print("[STARTING] server is starting......")
        self.server.listen(self.LISTENING_LIMIT)  # אנחנו מקשיבים כרגע לחיבורים חדשים, מתחילים להאזין
        print(f"[LISTENING] listening on server {self.SERVER}")
        while True:
            conn, addr = self.server.accept()  # מחכה לחיבור מהלקוח
            """
            במקום שנחכה לקוח לקוח יצרנו THREAD שגורם לכל לקוח להיות בו זמנית
           כלומר לא צריך לחכות לחיבור של לקוח כל פעם מחדש  
            אלא מחכים לחיבור של כל הלקוחות באותו זמן
            """
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[how many threads] {threading.active_count() - 1}")


if __name__ == "__main__":
    server = Server()
    server.start()