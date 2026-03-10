import sqlite3

class DataInDB:
    def __init__(self):
        self.CONNECTION = sqlite3.connect("save_commands.db")
        self.CURSOR = self.CONNECTION.cursor()


    def show_data(self):
        self.CURSOR.execute("SELECT *FROM commands")
        data = self.CURSOR.fetchall()
        for column in data:
            print(column)

    def delete_all_data(self):
        self.CURSOR.execute("DELETE FROM commands")
        self.CONNECTION.commit()
        print("[DB] All data deleted.")


if __name__ == "__main__":
    viewer = DataInDB()
    #viewer.delete_all_data()
    viewer.show_data()


