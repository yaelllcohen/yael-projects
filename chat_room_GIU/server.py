import os.path
import socket
import threading
import hashlib

from rsa_keys import RsaKeys

import rsa

class Server:
    def __init__(self, host= '0.0.0.0', port=5050):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HEADER = 64 # גודל ההודעה עד 64 ביטים
        self.PORT = port
        self.SERVER = host
        self.ADDR = (host, port)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.LISTENING_LIMIT = 5
        """
        יצרתי סוקט 
        AF_INET אומר שזה לפי IPV4
        SOCK_STREAM אומר שזה לפי פרוטוקול TCP
        """
        self.server.bind(self.ADDR)  # הוא מכריז על כתובת, כולמר שקיים כתובת כדי שיגיעו בקשות
        self.connections = []

        self.conn_to_username = {}  #  חיבור -> שם משתמש

        server_keys_path = os.path.join("keys", "server")
        self.keys = RsaKeys(base_path=server_keys_path)

        priv_exists = os.path.exists(os.path.join(server_keys_path, "private_key.pem"))
        pub_exists = os.path.exists(os.path.join(server_keys_path, "public_key.pem"))
        if not (priv_exists and pub_exists):
            self.keys.generate_keys()
        else:
            self.keys.load_keys()

        self.client_keys = {}


    def receive_message(self, conn, username):
        is_connected = True
        while is_connected:
            """
            connect.recv(HEADER) מקבל מהלקוח את ההודעה עד גודל HEADER
            HEADER זה גודל ההודעה כ64 ביטים
            decode(FORMAT) ממיר את ההודעה מביטים למחרוזת
            כלומר סהכ אנחנו רוצים את גודל ההודעה
            """
            try:
                message_length = self.recv_all(conn, self.HEADER)
                if message_length:  # האם ההודעה חוקית
                    message_length = int(message_length.decode(self.FORMAT))  # ממירים לINT את גודל ההודעה כביטים
                    plain_bytes = self.recv_all(conn, message_length)

                    #קודם מנסים לקרוא כטקסט רגיל
                    text_try = None
                    try:
                        text_try = plain_bytes.decode(self.FORMAT)
                    except Exception:
                        pass

                    if text_try is not None and text_try.startswith("[IMAGE]|"):
                        # מלקוח לשרת: [IMAGE]|<base64>
                        encoded = text_try[len("[IMAGE]|"):]
                        # מהשרת לכל הלקוחות: [IMAGE]|username|<base64>
                        final_msg = f"[IMAGE]|{username}|{encoded}"
                        self.broadcast(final_msg, conn)
                        continue
                    else:

                        try:
                            plain_text = self.keys.decrypt(plain_bytes, self.keys.private_key)
                        except Exception:
                            if  text_try is not None:
                                plain_text = text_try
                            else:
                                print("[ERROR] unreadable message from client")
                                continue  # עוברים להודעה הבאה


                        if plain_text == self.DISCONNECT_MESSAGE:
                            is_connected = False
                            print(f"{username} disconnected")

                        print(f"[{username}] {plain_text}")
                        final_msg = f"[{username}]  {plain_text}"
                        self.broadcast(final_msg, conn)
            except:
                print(f"[ERROR] the connection with {username} failed")
                is_connected = False

        conn.close()  # סוגר את החיבור, את הסוקט
        if conn in self.connections:  # כשהלקוח התנתק מהרשימה של החיבורים הפעילים
            self.connections.remove(conn)
        if conn in self.client_keys:
            del self.client_keys[conn]

        self.broadcast_users_list()  # שולח רשימה מעודכנת אחרי ניתוק

        if conn in self.client_keys:
            del self.client_keys[conn]


    def send_to_client(self, msg, conn):
        try:
            if msg.startswith("[IMAGE]|"):
                # לא מצפינים תמונות
                message = msg.encode(self.FORMAT)
            elif conn in self.client_keys:
                message = self.keys.encrypt(msg, self.client_keys[conn])
            else:
                message = msg.encode(self.FORMAT)#לא מוצפן
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
            if conn in self.client_keys:
                del self.client_keys[conn]


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
                plain_bytes_username = conn.recv(username_length)
                plain_text_username = self.keys.decrypt(plain_bytes_username, self.keys.private_key)

                print(f"[USERNAME RECEIVED] {plain_text_username} from {addr}")
            else:
                plain_text_username = f"{addr}"  # fallback אם לא התקבל שם

            client_public_key_length_string = conn.recv(self.HEADER).decode(self.FORMAT)
            if not client_public_key_length_string:
                raise Exception("missing client public key header")

            client_public_key_length = int(client_public_key_length_string)
            client_public_key = conn.recv(client_public_key_length)
            client_public_key_pem = rsa.PublicKey.load_pkcs1(client_public_key) #ממיר לאובייקט של PUBLICKEY שהספרייה RSA תדע להשתמש
            self.client_keys[conn] = client_public_key_pem


            self.connections.append(conn)
            self.conn_to_username[conn] = plain_text_username

            # מיד אחרי שהתחבר – נעדכן את כל הלקוחות ברשימת המשתמשים
            self.broadcast_users_list()

            thread = threading.Thread(target=self.receive_message, args=(conn, plain_text_username))
            thread.start()
        except:
            print(f"[ERROR] failed to receive username from {addr}")
            conn.close()

    def broadcast_users_list(self):
        users = []
        for conn in self.connections:
            username = self.conn_to_username.get(conn)
            if username:
                users.append(username)

        msg = "USERS_LIST|" + "|".join(users)
        print(f"[USERS LIST] {users}")

        for conn in self.connections:
            self.send_to_client(msg, conn)


    def recv_all(self, conn, n):
        data = b""
        while len(data) < n:
            packet = conn.recv(n - len(data))
            if not packet:  # הלקוח התנתק באמצע
                return None
            data += packet
        return data


    " הפונקציה נועדה לטפל בחיבורים חדשים ולחלק אותם לאן שהם צריכים להגיע"

    def start(self):
        print("[STARTING] server is starting......")
        self.server.listen(self.LISTENING_LIMIT)
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