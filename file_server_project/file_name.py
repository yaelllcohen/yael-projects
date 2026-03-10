import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from create_file import CreateFile


class FileName():
    def __init__(self, first_screen_after_login, username):

        self.root = tk.Tk()
        self.root.title("file_name")
        self.root.geometry("300x200")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.config(bg="pink")

        self.name_label = tk.Label(self.root, text="enter file name", font=('david', 30, 'bold'))
        self.name_label.config(anchor="center", justify="center", bg='lightblue')
        self.name_label.grid(row=0, column=1, pady=20)

        self.name = ttk.Entry(self.root)
        self.name.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.name.bind("<Return>", self.change_to_create_file)

        self.save_button = ttk.Button(self.root, text="save", command=self.change_to_create_file)
        self.save_button.grid(row=2, column=1, pady=10, padx=10)

        self.first_screen_after_login = first_screen_after_login
        self.username = username




        self.root.mainloop()


    def change_to_create_file(self, event= None):
        name = self.name.get()
        self.root.destroy()
        CreateFile(self.first_screen_after_login, name, self.username)




if __name__ == "__main__":
    FileName()