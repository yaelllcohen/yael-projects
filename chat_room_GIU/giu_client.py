import tkinter as tk
from tkinter import ttk
from tkinter.constants import DISABLED
from client import Client
import threading
from PIL import Image, ImageTk
from tkinter import filedialog
import base64
from io import BytesIO




class GIUClient:
    def __init__(self, client, path=None):

        self.client = client

        self.root = tk.Tk()
        self.root.title("chat app")
        self.root.geometry("550x430")

        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=0)

        self.path = path
        self.avatar_img = ImageTk.PhotoImage(Image.open(path).resize((30,30)))#מיני אווטאר


        self.frame = ttk.Frame(self.root)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=0)
        self.frame.rowconfigure(0, weight=1)


        #להציג הודעות
        self.chat_length = tk.Text(self.frame, bg='pink', width=43, height=20)
        self.chat_length.config(state=DISABLED)
        self.chat_length.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=6, pady=6)


        #כפתור שליחת ההודעות
        self.send_button = tk.Button(self.frame, text="SEND", bg="orange", fg="white", width=10, command = self.client_message)
        self.send_button.grid(row=1, column=1, sticky="e", padx=6, pady=6)

        self.image_button = tk.Button(self.frame, text="📷", bg="lightblue", fg="black", width=4, command=self.send_image)
        self.image_button.grid(row=1, column=2, sticky="e", padx=3)

        #מקום להקלדת הודעות
        self.text_box = tk.Text(self.frame, bg='lightpink', width=20, height=3)
        self.text_box.grid(row=1, column=0, sticky="ew", padx=6, pady=6)
        self.text_box.bind("<Return>",self.client_message)

        #כל המשתמשים המחוברים
        self.users_listbox = tk.Listbox(self.root, height=20)
        self.users_listbox.grid(row=0, column=1, rowspan=2, sticky="ns", padx=5, pady=5)

        self.image_refs = []

        #דמון אומר שאם כל שאר התהליכונים נסגרים אז הוא ייסגר גם אוטומטית
        threading.Thread(target=self.listen_to_server, daemon=True).start()



        self.root.mainloop()



    def client_message(self, event= None):
        msg = self.text_box.get('1.0', tk.END).strip()
        if msg:
            self.client.send(msg)
            self.chat_length.config(state='normal')
            self.chat_length.image_create(tk.END, image=self.avatar_img)
            self.chat_length.insert(tk.END, f" [{self.client.username}] {msg} {'\n'}")
            self.text_box.delete('1.0', tk.END)
            self.chat_length.config(state=DISABLED)




    def listen_to_server(self):
        while True:
            try:
                message_length_that_came_from_server = self.recv_all(self.client.HEADER).decode(self.client.FORMAT)
                if message_length_that_came_from_server:  # האם ההודעה חוקית
                    message_length_that_came_from_server = int(message_length_that_came_from_server)  # ממירים לINT את גודל ההודעה כביטים

                    cipher_bytes = self.recv_all(message_length_that_came_from_server)

                    plain_text = None

                    try:
                        temp = self.client.keys.decrypt(cipher_bytes, self.client.keys.private_key)#אם זה טקסט זה אמור להחזיר מחרוזת אחרת BOOL
                        if isinstance(temp, str):  # האם זה מחרוזת
                            plain_text = temp
                    except Exception:
                        pass

                    if plain_text is None:
                        try:
                            plain_text = cipher_bytes.decode(self.client.FORMAT)
                        except Exception:
                            print("[ERROR] unreadable/encrypted message")
                            continue


                    if plain_text.startswith("USERS_LIST|"):
                        users_str = plain_text[len("USERS_LIST|"):] #החלק בלי הUSERS_LIST
                        users = [u for u in users_str.split("|") if u]  # מפצל לשמות
                        self.update_users_list(users)

                    elif plain_text.startswith("[IMAGE]|"):

                        try:
                            parts = plain_text.split("|", 2)  # ["[IMAGE]", "username", "<base64>"]
                            if len(parts) < 3:
                                print("[ERROR] bad IMAGE message format:", plain_text)
                                continue

                            _, username, encoded = parts
                            image_data = base64.b64decode(encoded)
                            image = Image.open(BytesIO(image_data)).resize((100, 100)) #פותח את התמונה מתוך הבייטים שבזיכרון
                            img_tk = ImageTk.PhotoImage(image)

                            self.chat_length.config(state='normal')
                            self.chat_length.image_create(tk.END, image=img_tk)
                            self.chat_length.insert(tk.END, "\n")
                            self.chat_length.insert(tk.END, f"[{username}] sent picture\n")

                            self.chat_length.config(state=DISABLED)

                            # לשמור רפרנס לתמונה כדי שלא תיעלם
                            self.image_refs.append(img_tk)


                        except Exception as e:
                            print(f"[ERROR] Failed to show image: {e}")


                    else:

                        self.chat_length.config(state= 'normal')
                        self.chat_length.insert(tk.END, plain_text + '\n')
                        self.chat_length.config(state=DISABLED)


            except:
                print("[ERROR] couldn't get the message from the server")
                break

    def recv_all(self, n):
        data = b""
        while len(data) < n:
            packet = self.client.client.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data


    def update_users_list(self, users):
        self.users_listbox.delete(0, tk.END)
        for u in users:
            self.users_listbox.insert(tk.END, u)

    def send_image(self):
        file_path = filedialog.askopenfilename(
            title="choose picture",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")]
        )
        if not file_path:
            return  # המשתמש ביטל

        try:
            with open(file_path, "rb") as f:
                image_data = f.read()

            encoded = base64.b64encode(image_data).decode("utf-8")

            message = f"[IMAGE]|{encoded}"
            self.client.send(message)


            img = Image.open(file_path).resize((100, 100))
            img_tk = ImageTk.PhotoImage(img)
            self.chat_length.config(state='normal')
            self.chat_length.image_create(tk.END, image=img_tk)
            self.chat_length.insert(tk.END, "\n")
            self.chat_length.image_create(tk.END, image=self.avatar_img)
            self.chat_length.insert(tk.END, f"[{self.client.username}] sent picture \n")
            self.chat_length.config(state=DISABLED)


            self.image_refs.append(img_tk)

        except Exception as e:
            print(f"[ERROR] failed to send image: {e}")






if __name__ == "__main__":
    client = Client()
    # app = GIUClient(client)