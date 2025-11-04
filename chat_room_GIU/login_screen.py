import tkinter as tk
from tkinter import ttk
from client import Client
from pick_your_image import PickYourImage
from tkinter import messagebox
import sqlite3
import hashlib



class LoginScreen:

    def __init__(self,client):
        self.client = client

        self.root = tk.Tk()
        self.root.title("login screen")
        self.root.geometry("400x300")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.config(bg="pink")

        self.label_login = tk.Label(self.root, text="LOGIN", font=('david', 30, 'bold'))
        self.label_login.config(anchor="center", justify="center", bg='lightblue')
        self.label_login.grid(row=0, column=1, pady=20)

        self.label_user = tk.Label(self.root, text="enter your username", font=("David", 15, "bold"))
        self.label_user.config(anchor="center", justify="center", bg="pink")
        self.label_user.grid(row=1, column=1, pady=5, sticky="ew")

        self.username = ttk.Entry(self.root)
        # self.password.config(anchor="center", justify="center")
        self.username.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        self.label_pass = tk.Label(self.root, text="enter your password", font=("David", 15, "bold"))
        self.label_pass.config(anchor="center", justify="center", bg="pink")
        self.label_pass.grid(row=3, column=1, pady=5, sticky="ew")

        self.password = ttk.Entry(self.root, show="*")
        self.password.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")
        self.password.bind("<Return>", self.if_pass_true_change_to_avatars_screen)

        self.button_frame = tk.Frame(self.root, bg="pink")
        self.button_frame.grid(row=6, column=1, pady=10)

        self.register_button = ttk.Button(self.button_frame, text="register", command=self.change_to_register)
        self.register_button.grid(row=6, column=1, pady=3, padx=10)

        self.login_button = ttk.Button(self.button_frame, text="login", command=self.if_pass_true_change_to_avatars_screen)
        self.login_button.grid(row=6, column=2, pady=3, padx=10)

        # Label להודעות
        self.message_label = tk.Label(self.root, text="", fg="red", bg="pink", font=("Arial", 10, "bold"))
        self.message_label.grid(row=5, column=1, pady=5)
        self.root.mainloop()

    def move_to_pick_your_image_screen(self, event=None):
        username = self.username.get()
        if username:
            self.client.username = username
            self.root.destroy()
            PickYourImage(self.client)
        else:
            messagebox.showinfo("no username", "enter a username to continue")

    def connect_to_the_db(self):
        # מתחברת בו לתוך הDB
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        sql = 'select * from users'
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        return results

    def if_pass_true_change_to_avatars_screen(self, event=None):
        results = self.connect_to_the_db()
        isFound = False
        username = self.username.get()
        for result in results:
            if result[1] == username:
                password = self.password.get()
                hash_pass = hashlib.sha1(password.encode()).hexdigest()
                if result[2] == hash_pass:
                    self.show_message("logining...", "green")
                    isFound = True
                    self.move_to_pick_your_image_screen()
                    return

        if isFound == False:
            self.show_message("the password or username is incorrect", "red")



    def show_message(self, text, color= None):
        self.message_label.config(text= text, fg= color)

    def change_to_register(self):
        self.root.destroy()
        from Register import Register
        Register(self.client)











if __name__ == "__main__":
    client = Client()
    login = LoginScreen(client)