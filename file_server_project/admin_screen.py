import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class AdminScreen():
    def __init__(self, username, first_screen_after_login):

        self.username = username
        self.first_screen_after_login = first_screen_after_login

        self.root = tk.Tk()
        self.root.title("admin screen")
        self.root.geometry("600x500")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(10, weight= 1)
        self.root.config(bg="pink")

        self.welcome_label = tk.Label(self.root, text=f"welcome, Admin {self.username}!", font=("David", 30, "bold"))
        self.welcome_label.config(anchor="center", justify="center", bg='lightblue')
        self.welcome_label.grid(row=1, column=0, columnspan=3, pady=5, sticky="ew")

        self.text_label = tk.Label(self.root, text= f"all the users: ", font=("David", 20,"bold" ))
        self.text_label.config(bg = "pink")
        self.text_label.grid(row=2, column=0, pady=5)

        self.users_table_treeview = ttk.Treeview(self.root, columns=("username","IsAdmin"),show="headings", height= 15)
        #כותרות
        self.users_table_treeview.heading("username", text="Username")
        self.users_table_treeview.heading("IsAdmin", text="IsAdmin")

        self.users_table_treeview.grid(row= 3, column= 0, columnspan=3,pady=5, sticky = "nesw")

        #סרגל גלילה אם יהיו הרבה משתמשים
        #vertical אומר שהגלילה היא אנכית
        self.scorllbar_for_many_pepole = ttk.Scrollbar(self.root, orient="vertical", command= self.users_table_treeview.yview)
        #זה מציג את התצוגה, כלומר אם את מגלגלת אז מעדכנים את מה שרואים בטבלה
        self.users_table_treeview.configure(yscrollcommand=self.scorllbar_for_many_pepole.set)

        self.add_to_the_users_table_treeview(self.users_table_treeview, self.exclude_the_users())

        self.return_button = tk.Button(self.root, bg="orange", fg="white", text="return",width=17, height=2,font=("David", 13, "bold"), command=self.back_to_main)
        self.return_button.grid(row=4, column=0, columnspan=3, padx=12, pady=10, sticky="sew")

        #בשביל למחוק משתמש בלחיצה על מקש ימני
        self.menu = tk.Menu(self.root, tearoff=0)
        self.users_table_treeview.bind("<Button-3>", self.show_context_menu)

        self.root.mainloop()

    def connect_to_db(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, IsAdmin FROM users")
        # רשימה של טאפלים
        results = cursor.fetchall()
        conn.close()
        return results

    def exclude_the_users(self):
        results = self.connect_to_db()
        dict_of_users = {}
        for result in results:
            dict_of_users[result[0]] = result[1]
        return dict_of_users

    def add_to_the_users_table_treeview(self, users_table, users_dict):
        #get children מחזיר רשימה של כל השורות שנמצאות בטבלה
        rows_table = users_table.get_children()
        #מוחקים את הטבלה בשביל שאוכל להוסיף מחדש
        for row in rows_table:
            users_table.delete(row)

        #הוספה
        #"" אומר שהשורה היא שורה חדשה
        #end נוסף לסוף הטבלה
        for username, is_admin in users_dict.items():
            users_table.insert("", "end", values= (username, self.is_admin(is_admin)) )



    def is_admin(self, is_admin):
        if is_admin:
            return "Yes"
        else:
            return "No"

    def back_to_main(self):
        self.first_screen_after_login.root.deiconify()  # מציג שוב את המסך הראשי
        self.root.destroy()

    def show_context_menu(self, event = None):

        try:
            #המזהה הפנימי של השורה עם הפוקוס
            #פוקוס = הרכיב או השורה שהמשתמש עובד עליה כרגע, זה שקיבל את תשומת הלב עם העכבר
            id = self.users_table_treeview.focus()
            #אם אין פוקוס אולי שורה מסומנת
            if not id:
                #רשימה של כל השורות שנבחרו
                selected = self.users_table_treeview.selection()
                #המזהה הפנימי של השורה
                id = selected[0] if selected else None

            if not id:
                return  # אין על מה לפתוח תפריט

            # מגדיר את השורה שבחרנו
            self.users_table_treeview.selection_set(id)

            username = self.users_table_treeview.set(id, "username")
            is_admin_text = self.users_table_treeview.set(id, "IsAdmin")  # "Yes"/"No"

            # בונה תפריט דינמי
            self.menu.delete(0, "end")
            if is_admin_text == "Yes":
                self.menu.add_command(label="Remove admin", command= self.remove_admin)
            else:
                self.menu.add_command(label="Add admin", command=self.add_admin)

            self.menu.add_separator()

            self.menu.add_command(label="Delete user", command=self.delete_user_from_db)

            # מציג את התפריט באותו המקום
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()







    def selected_user(self):
        selected = self.users_table_treeview.selection()
        if not selected:
            messagebox.showinfo("No selection", "Please select a user to delete.")
            return
        #selected[0] זה המזהה הפנימי של השורה שנבחרה
        #זה לוקח מעמודת USERNAME את הUSERNAME שהמזהה הפנימי של השורה הוא-
        username = self.users_table_treeview.set(selected[0], "username")

        return username

    def add_admin(self):
        username = self.selected_user()
        # הודעת אישור
        answer = messagebox.askyesno("Confirm add admin", f"Are you sure you want to add admin to '{username}'?")
        if not answer:
            return

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET IsAdmin = ? WHERE username = ?",(1, username))
        conn.commit()
        conn.close()

        self.add_to_the_users_table_treeview(self.users_table_treeview, self.exclude_the_users())
        messagebox.showinfo("ADD ADMIN", f"User '{username}' is admin.")

    def remove_admin(self):
        username = self.selected_user()
        if username == self.username:
            messagebox.showinfo("can't remove admin", "you can't remove your admin")
            return

            # הודעת אישור
        answer = messagebox.askyesno("Confirm remove admin", f"Are you sure you want to remove admin to '{username}'?")
        if not answer:
            return
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET IsAdmin = ? WHERE username = ?", (0, username))
        conn.commit()
        conn.close()

        self.add_to_the_users_table_treeview(self.users_table_treeview, self.exclude_the_users())
        messagebox.showinfo("REMOVE ADMIN", f"User '{username}' is not admin anymore")

    def delete_user_from_db(self):
        username = self.selected_user()
        if username == self.username:
            messagebox.showinfo("can't delete", "you can't delete yourself")
            return

            # הודעת אישור
        answer = messagebox.askyesno("Confirm delete", f"Are you sure you want to delete '{username}'?")
        if not answer:
            return
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        conn.close()

        self.add_to_the_users_table_treeview(self.users_table_treeview, self.exclude_the_users())
        messagebox.showinfo("Deleted", f"User '{username}' was deleted successfully.")




if __name__ == "__main__":
    AdminScreen('yael')
