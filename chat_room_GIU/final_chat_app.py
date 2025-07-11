from login_screen import LoginScreen
from client import Client



if __name__ == "__main__":
    client = Client()
    app = LoginScreen(client)
