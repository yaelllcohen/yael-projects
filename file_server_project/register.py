import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import sqlite3
from login import Login


class Register():
    def __init__(self):

        self.root = tk.Tk()
        self.root.title("register screen")
        self.root.geometry("400x300")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.config(bg = "pink")

        self.label_register = tk.Label(self.root, text="REGISTER", font= ('david', 30, 'bold'))
        self.label_register.config(anchor="center", justify="center", bg='lightblue')
        self.label_register.grid(row=0, column=1, pady=20)

        self.label_user = tk.Label(self.root, text ="enter your username", font=("David", 15, "bold"))
        self.label_user.config(anchor ="center", justify ="center", bg ="pink")
        self.label_user.grid(row = 1, column = 1, pady = 5, sticky ="ew")

        self.username = ttk.Entry(self.root)
        self.username.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        self.label_pass = tk.Label(self.root, text ="enter your password", font=("David", 15, "bold"))
        self.label_pass.config(anchor ="center", justify ="center", bg ="pink")
        self.label_pass.grid(row = 3, column = 1, pady = 5, sticky ="ew")

        self.password = ttk.Entry(self.root)
        self.password.grid(row = 4, column= 1, padx=5, pady=5, sticky= "nsew")
        self.password.bind("<Return>", self.change_to_login_screen)


        self.button_frame = tk.Frame(self.root, bg="pink")
        self.button_frame.grid(row=6, column=1, pady=10)

        self.register_button = ttk.Button(self.button_frame, text="register", command=self.change_to_login_screen)
        self.register_button.grid(row=6, column=1, pady=3, padx=10)

        self.login_button = ttk.Button(self.button_frame, text="back to login", command=self.back_to_login)
        self.login_button.grid(row=6, column=2, pady=3, padx = 10)

        # Label להודעות (שגיאה/הצלחה)
        self.message_label = tk.Label(self.root, text="", fg="red", bg="pink", font=("Arial", 10, "bold"))
        self.message_label.grid(row= 5, column= 1, pady= 5)

        self.root.mainloop()


    def add_to_db_user_and_pass(self):
        try:
            username = self.username.get()

            if not username:
                self.show_message("enter username", "orange")
                return False

            if not self.if_username_uniqe():
                self.show_message("Username already exist", "red")
                return False

            password = self.password.get()

            if len(password) < 8:
                self.show_message("the password length should be at least 8", "orange")
                return False

            if not password:
                self.show_message("enter password", "orange")
                return False


            hash_pass = hashlib.sha1(password.encode()).hexdigest()
            # יוצרים או נפתחים למסד נתונים חדש בשם users.db
            conn = sqlite3.connect("users.db")

            # מצביע לעבודה מול המסד
            cursor = conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                IsAdmin BOOL DEFAULT FALSE
            )
            """)

            sql = "INSERT INTO users (username, password) VALUES (?, ?)"

            values = username, hash_pass

            cursor.execute(sql, values)
            self.show_message("register!", "green")
        except Exception as e:
            print(e)
        conn.commit()
        conn.clofse()
        return True

    def change_to_login_screen(self, event=None):
        if self.add_to_db_user_and_pass():
            self.root.destroy()
            Login()

    def back_to_login(self):
        self.root.destroy()
        Login()


    def if_username_uniqe(self):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        sql = 'select * from users'
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            if result[1] == self.username.get():
                return False
        return True


    def show_message(self, text, color= None):
        self.message_label.config(text= text, fg= color)







if __name__ == "__main__":
    register = Register()
