import tkinter as tk
from tkinter import  ttk
import os
from client_side import Client


class FileTransferApp:
    def __init__(self, client):

        self.client = client
        #self.server = server

        self.CLIENT_FOLDER = r'C:\Users\USER\PycharmProjects\Git_Projects\file_server_project\client_folder'
        self.SERVER_FOLDER = r'C:\Users\USER\PycharmProjects\Git_Projects\file_server_project\server_folder'

        self.root = tk.Tk()
        self.root.title("file system")

        self.client_listbox = tk.Listbox(self.root, width = 80, height= 30)
        self.server_listbox = tk.Listbox(self.root, width = 80, height= 30)

        self.client_listbox.grid(row= 1, column= 0, padx= 10, pady = 10)
        self.server_listbox.grid(row= 1, column = 2, padx = 10, pady = 10)

        tk.Label(self.root, text= "קבצים בלקוח").grid(row= 0, column = 0)
        tk.Label(self.root, text = "קבצים בשרת").grid(row= 0, column= 2)

        self.list_files()

        self.upload_button = ttk.Button(self.root, text= "העלאה לשרת", command= self.upload_file)
        self.upload_button.grid(row= 2, column= 0, pady= 5)

        self.download_button = ttk.Button(self.root, text= "הורדה ללקוח", command= self.download_file )
        self.download_button.grid(row= 2, column= 2, pady= 5)


        self.root.mainloop()

    def list_files(self):
        for file in os.listdir(self.SERVER_FOLDER):
            self.server_listbox.insert(0, file)

        for file in os.listdir(self.CLIENT_FOLDER):
            self.client_listbox.insert(0, file)

    def upload_file(self):
        selected_tuple = self.client_listbox.curselection()
        if not selected_tuple:
            print("No file selected")
            return
        file_name = self.server_listbox.get(selected_tuple[0])
        full_path = os.path.join(self.CLIENT_FOLDER, file_name)  # ✅ נתיב נכון
        print("uploading ", file_name)
        self.client.upload_file(self.client.client_socket, full_path)
        self.list_files()  # ✅ רענון


    def download_file(self):
        selected_tuple = self.server_listbox.curselection()
        if not selected_tuple:
            print("No file selected")
            return
        file_name = self.server_listbox.get(selected_tuple[0])
        dest_path = os.path.join(self.CLIENT_FOLDER, file_name)
        print("downloading ", file_name)
        self.client.download_file(self.client.client_socket, dest_path)
        self.list_files()  # ✅ רענון



if __name__ == "__main__":
    client = Client()
    #server = Server()
    app = FileTransferApp(client)


