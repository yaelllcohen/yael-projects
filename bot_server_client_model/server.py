import socket
import threading
import sqlite3

HEADER = 64 #גודל ההודעה עד 64 ביטים
PORT = 5050
"""
אפשר למצוא את כתובת הIP המקומית! LAN דרך הCMD עם IPCONFIG
ובנוסף בשיטה הבאה:
"""
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)  #הכתובת המורכבת מפורט וIP בטאפל
FORMAT = 'utf-8' #בהמשך הקוד נראה את זה ממיר לביטים, זאת שיטת קידוד
DISCONNECT_MESSAGE = "!DISCONNECT"
"""
יצרתי סוקט 
AF_INET אומר שזה לפי IPV4
SOCK_STREAM אומר שזה לפי פרוטוקול TCP
"""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR) # הוא מכריז על כתובת, כולמר שקיים כתובת כדי שיגיעו בקשות


#השרת מחזיר את ההודעה המתאימה מהDB
def get_response_from_db(msg,connect):
    connection = sqlite3.connect(r'C:\Users\USER\SQLITE\bot_data_base.db')
    cursor = connection.cursor()
    sql = 'select * from commands'
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        if msg == result[0]:
            bot_massage = result[1]
            break
    else:
        bot_massage = "unknown command"

    send_bot_msg = bot_massage.encode(FORMAT)
    bot_message_length = len(send_bot_msg)
    "ממיר את ההודעה ממחרוזת לביטים"
    send_length = str(bot_message_length).encode(FORMAT)
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
    connect.send(send_length)
    connect.send(send_bot_msg)


"הפונקציה נועדה לטפל בחיבור הבודד בין הלקוח לשרת"
def handle_client(connect, addr):
    print(f"[NEW CONNECTING] {addr} connect")
    is_connected = True
    while is_connected:
        """
        connect.recv(HEADER) מקבל מהלקוח את ההודעה עד גודל HEADER
        HEADER זה גודל ההודעה כ64 ביטים
        decode(FORMAT) ממיר את ההודעה מביטים למחרוזת
        כלומר סהכ אנחנו רוצים את גודל ההודעה
        """
        message_length = connect.recv(HEADER).decode(FORMAT)
        if message_length: #האם ההודעה חוקית
            message_length = int(message_length) #ממירים לINT את גודל ההודעה כביטים
            message = connect.recv(message_length).decode(FORMAT) #ההודעה עצמה בביטים
            if message == DISCONNECT_MESSAGE:
                is_connected = False

            print(f"[{addr}] {message}")
            get_response_from_db(message,connect)

    connect.close() #סוגר את החיבור, את הסוקט

" הפונקציה נועדה לטפל בחיבורים חדשים ולחק אותם לאן שהם צריכים להגיע"
def start():
    print("[STARTING] server is starting......")
    server.listen() # אנחנו מקשיבים כרגע לחיבורים חדשים, מתחילים להאזין
    print(f"[LISTENING] listening on server {SERVER}")
    while True:
        connect, addr = server.accept() #מחכה לחיבור מהלקוח
        """
        במקום שנחכה לקוח לקוח יצרנו THREAD שגורם לכל לקוח להיות בו זמנית
       כלומר לא צריך לחכות לחיבור של לקוח כל פעם מחדש  
        אלא מחכים לחיבור של כל הלקוחות באותו זמן
        """
        thread = threading.Thread(target=handle_client,args= (connect,addr))
        thread.start()
        print(f"[how many threads] {threading.active_count() - 1}")

if __name__ == "__main__":


    start()
