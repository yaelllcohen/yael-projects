import tkinter as tk
from tkinter import ttk
from tkinter.constants import DISABLED
from client import Client
import threading
from PIL import Image, ImageTk



class GIUClient:
    def __init__(self, client, path):

        self.client = client

        self.root = tk.Tk()
        self.root.title("chat app")
        self.root.geometry("380x430")

        self.path = path
        self.avatar_img = ImageTk.PhotoImage(Image.open(path).resize((30,30)))#מיני אווטאר


        #self.style = ttk.Style()
       # self.style.configure("Send.TButton", background = 'lightblue', foreground = 'green')

        self.frame = ttk.Frame(self.root)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=0)
        self.frame.rowconfigure(0, weight=1)

        #להציג הודעות
        self.chat_length = tk.Text(self.frame, bg='pink', width=43, height=20)
        self.chat_length.config(state=DISABLED)
        self.chat_length.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=6, pady=6)
        #כפתור שליחת ההודעות
        self.send_buttom = tk.Button(self.frame, text="SEND", bg="orange", fg="white", width=10, command = self.client_message)
        self.send_buttom.grid(row=1, column=1, sticky="e", padx=6, pady=6)

        #מקום להקלדת הודעות
        self.text_box = tk.Text(self.frame, bg='lightpink', width=20, height=3)
        self.text_box.grid(row=1, column=0, sticky="ew", padx=6, pady=6)
        self.text_box.bind("<Return>",self.client_message)

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
        else:
            self.client.disconnect()

    def listen_to_server(self):
        while True:
            try:
                message_length_that_came_from_server = self.client.client.recv(self.client.HEADER).decode(self.client.FORMAT)
                if message_length_that_came_from_server:  # האם ההודעה חוקית
                    message_length_that_came_from_server = int(
                        message_length_that_came_from_server)  # ממירים לINT את גודל ההודעה כביטים
                    message_that_came_from_server = self.client.client.recv(message_length_that_came_from_server).decode(
                        self.client.FORMAT)  # ההודעה עצמה בביטים
                    self.chat_length.config(state= 'normal')
                    #self.chat_length.image_create(tk.END, image=self.avatar_img)
                    self.chat_length.insert(tk.END, message_that_came_from_server + '\n')
                    self.chat_length.config(state=DISABLED)


            except:
                print("[ERROR] couldn't get the message from the server")
                break






if __name__ == "__main__":
    client = Client()
    app = GIUClient(client)