import tkinter as tk
from tkinter import ttk
from login import Login
from tkinter import filedialog
#from create_file import CreateFile
from file_name import FileName
import os
from tkinter import messagebox
import sqlite3
from admin_screen import AdminScreen



class FirstScreenAfterLogin():
    def __init__(self, username):

        self.username = username

        self.root = tk.Tk()
        self.root.title("main")
        self.root.geometry("600x500")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(10, weight= 1)
        self.root.config(bg="pink")


        self.welcome_label = tk.Label(self.root, text =f"welcome, {self.username}!", font=("David", 30, "bold"))
        self.welcome_label.config(anchor="center", justify="center", bg='lightblue')
        self.welcome_label.grid(row=1, column=0, columnspan=3, pady=5, sticky="ew")


        self.button_frame = tk.Frame(self.root, bg="pink")
        self.button_frame.grid(row=0, column=2, pady=10,sticky="e")

        self.logout_button = tk.Button(self.button_frame, bg="orange", fg="white", text="log out",width=17, height=2,font=("David", 13, "bold"), command=self.back_to_login)
        self.logout_button.grid(row=0, column=2, pady=5, padx=10,sticky="e")

        self.create_file_button = tk.Button(self.button_frame, bg="orange", fg="white", text= "create file",width=17, height=2,font=("David", 13, "bold"), command = self.create_file_name)
        self.create_file_button.grid(row = 0, column = 1, pady = 10, padx= 10)

        self.admin_button = tk.Button(self.button_frame, bg="orange", fg="white", text="administor", width=17, height=2, font=("David", 13, "bold"), command = self.open_admin_screen)
        self.admin_button.grid(row=0, column=0, pady=10, padx= 10)


        self.files_frame = tk.Frame(self.root, bg="pink")
        self.files_frame.grid(row=2, column=0, columnspan=3, padx=12, pady=10, sticky="nsew")

        self.files_listbox = tk.Listbox(self.files_frame, width=100, height=17)
        self.files_listbox.grid(row=0, column=0, sticky="nsew")
        self.files_listbox.bind("<Double-Button-1>", self.open_selected_file)


        self.upload_file_button = tk.Button(self.root, bg="orange", fg="white", text="upload file", width=20, height=2,font=("David", 13, "bold"), command=self.upload_file)
        self.upload_file_button.grid(row=3, column=0, columnspan=3, padx=12, pady=10, sticky="sew")


        self.root.mainloop()


    def back_to_login(self):
        self.root.destroy()
        Login()

    def create_file_name(self):
        self.root.withdraw()  # מסתיר את החלון
        FileName(self, self.username)


    def add_file(self, filepath):
        self.files_listbox.insert(tk.END, filepath)

    def upload_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title= "Select a file")
        self.files_listbox.insert(tk.END, filename)

    def open_selected_file(self, event= None):
        #הקובץ שבחרנו מהרשימה
        selection = self.files_listbox.curselection()
        if not selection:
            return
        #זה טאפל שמחזיר את האינדקס והנתיב
        file_path = self.files_listbox.get(selection[0])
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"The file no longer exists:\n{file_path}")
            return
        os.startfile(file_path)  # פותח לפי תוכנה ברירת מחדל

    def connect_to_db(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT IsAdmin FROM users WHERE username = ?", (self.username,))
        result = cursor.fetchone()
        return result

    def open_admin_screen(self):

        result = self.connect_to_db()
        if not result:
            messagebox.showinfo("dont exist", f"username {self.username} is not exist")


        is_admin = result[0]
        if is_admin:
            self.root.withdraw()
            AdminScreen(self.username, self)
        else:
            messagebox.showinfo("not admin", f"username {self.username} is not admin")


if __name__ == "__main__":
    screen = FirstScreenAfterLogin("yael")



