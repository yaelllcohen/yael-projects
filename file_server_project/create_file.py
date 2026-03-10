import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from tkinter import messagebox



class CreateFile():
    def __init__(self, first_screen_after_login, name, username):

        self.root = tk.Tk()
        self.root.title("create_file")
        self.root.geometry("600x460")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.config(bg="pink")


        self.save_button = tk.Button(self.root, bg="orange", fg="white", text="save",width=17, height=2,font=("David", 13, "bold"), command=self.save_file)
        self.save_button.grid(row=0, column=0, pady=5, padx=10,sticky="n")

        self.text = tk.Text(self.root)
        self.text.grid(row=1, column=0, sticky="nsew")

        self.first_screen_after_login = first_screen_after_login
        self.name = name
        self.username = username

        self.root.mainloop()


    def save_file(self):
        save_folder = r'C:\Users\USER\PycharmProjects\Git_Projects\file_server_project\files_created'
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        folder_username = os.path.join(save_folder,f"{self.username}")
        if not os.path.exists(folder_username):
            os.makedirs(folder_username)
        file_path = os.path.join(folder_username, f"{self.name}.txt")
        file_text = str(self.text.get(1.0,tk.END))
        with open(file_path, 'w') as file:
            file.write(file_text)

        messagebox.showinfo("Saved", f"File '{self.name}.txt' saved successfully!")

        self.first_screen_after_login.add_file(file_path)
        self.first_screen_after_login.root.deiconify()  # מציג שוב את המסך הראשי
        self.root.destroy()



if __name__ == "__main__":
    CreateFile()