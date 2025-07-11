import tkinter as tk
from PIL import Image, ImageTk
from client import Client
from giu_client import GIUClient


class PickYourImage:
    def __init__(self, client):

        self.client = client

        self.root = tk.Tk()
        self.root.title("pick your avatar")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.geometry('295x350')
        self.root.config(bg = 'yellow')


        # נטען כל תמונה בנפרד
        self.avatar1_img = ImageTk.PhotoImage(Image.open("avatars/avatar1_cat.png").resize((100, 100)))
        self.avatar2_img = ImageTk.PhotoImage(Image.open("avatars/avatar2_fox.png").resize((100, 100)))
        self.avatar3_img = ImageTk.PhotoImage(Image.open("avatars/avatar3_girl.png").resize((100, 100)))
        self.avatar4_img = ImageTk.PhotoImage(Image.open("avatars/avatar4_witch.png").resize((100, 100)))

        self.labal = tk.Label(self.root, text="Pick your AVATAR!", font = ('david', 20, 'bold'))
        self.labal.config(anchor="center", justify="center", bg='lightblue')
        self.labal.grid(row=0, column=0, pady=10,columnspan=2, padx=20, sticky="nsew")

        btn1 = tk.Button(self.root, image=self.avatar1_img, command=self.select_avatar1)
        btn1.grid(row=1, column=0, padx=20, pady=20)

        btn2 = tk.Button(self.root, image=self.avatar2_img, command=self.select_avatar2)
        btn2.grid(row=1, column=1, padx=20, pady=20)

        btn3 = tk.Button(self.root, image=self.avatar3_img, command=self.select_avatar3)
        btn3.grid(row=2, column=0, padx=20, pady=20)

        btn4 = tk.Button(self.root, image=self.avatar4_img, command=self.select_avatar4)
        btn4.grid(row=2, column=1, padx=20, pady=20)

        self.selected = ""

        self.root.mainloop()



    # לכל כפתור פונקציה נפרדת
    def select_avatar1(self):
        self.avatar_selected("avatars/avatar1_cat.png")

    def select_avatar2(self):
        self.avatar_selected("avatars/avatar2_fox.png")

    def select_avatar3(self):
        self.avatar_selected("avatars/avatar3_girl.png")

    def select_avatar4(self):
        self.avatar_selected("avatars/avatar4_witch.png")


    # הפונקציה שמעבירה לצ'אט
    def avatar_selected(self, path):
        self.selected = path
        print(f"Avatar selected: {path}")
        self.client.send_to_server_username(self.client.username)
        self.root.destroy()
        GIUClient(self.client,path)


if __name__ == "__main__":
    client = Client()
    PickYourImage(client)