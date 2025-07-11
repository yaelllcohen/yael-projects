import tkinter as tk
from tkinter import ttk
from client import Client
from pick_your_image import PickYourImage



class LoginScreen:

    def __init__(self,client):
        self.client = client

        self.root = tk.Tk()
        self.root.title("login screen")
        self.root.geometry("300x200")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.config(bg = "pink")

        self.labal_login = tk.Label(self.root, text="LOGIN", font = ('david', 30, 'bold'))
        self.labal_login.config(anchor="center", justify="center", bg='lightblue')
        self.labal_login.grid(row=0, column=1, pady=20, sticky="nsew")

        self.labal_user = tk.Label(self.root, text ="enter your username")
        self.labal_user.config(anchor ="center", justify ="center", bg ="pink")
        self.labal_user.grid(row = 1, column = 1, pady = 5, sticky ="ew")

        self.frame = ttk.Frame(self.root)
        self.frame.grid(row = 2, column = 0, columnspan = 3, pady = 5)

        self.username = ttk.Entry(self.frame)
        #self.password.config(anchor="center", justify="center")
        self.username.grid(row = 2, column = 1, padx = 5, pady = 5, sticky ="nsew")
        self.username.bind("<Return>", self.move_to_chat_screen)

        self.buttom = tk.Button(self.frame, text="login", bg="orange", fg="white", width=8, command = self.move_to_chat_screen)
        self.buttom.grid(row=2, column=2, sticky="e",padx = 5, pady=5)

        self.root.mainloop()


    def move_to_chat_screen(self, event = None):
        self.client.username = self.username.get()  # שמירת שם המשתמש באובייקט client
        self.root.destroy()
        PickYourImage(self.client)



if __name__ == "__main__":
    client = Client()
    login = LoginScreen(client)