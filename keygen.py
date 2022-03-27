import time
import hashlib
import string
import random
import pexpect
import time
from pyfiglet import figlet_format
from termcolor import colored
from itertools import product

SHA1 = "b39f0b47f6e314599975efb850ec8a58032f0919"
URL = "https://crackmes.one/crackme/61c8b23a33c5d413767ca0de"

def print_banner():
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    title = "KeyGen v1.0"
    figtxt = figlet_format(title, font="chunky")
    banner = str()
    i = 0

    for c in range(len(figtxt)):
        banner += colored(str(figtxt)[c], colors[i], attrs=['bold'])
        i = 0 if i == len(colors) - 1 else i + 1

    msg = "\n+-------------------------------+\n"
    msg += "| written with <3 and coffee by |\n"
    msg += "| Twitter - @systemcra_sh       |\n"
    msg += "| https://blog.systemcra.sh     |\n"
    msg += "| March 2022                    |\n"
    msg += "+-------------------------------+\n"
    cred = colored(msg, 'yellow', attrs=['bold'])
    print(banner+cred)

def print_target_info():
    sha = "[*] target SHA1 : {}\n".format(SHA1)
    url = "[*] target URL  : {}\n".format(URL)

    print(sha+url)

def gen_username_value(username):
    xor_key = 0x0185

    username_bytes = bytearray()
    username_bytes.extend(map(ord, username))

    ret = 0
    for idx,byte in enumerate(username_bytes):
        if idx % 2 != 0:
            byte += 0x100
        ret += byte ^ xor_key
    return ret

def gen_serial_value(serial):
    static_add = 0xFFFFFFD0
    static_mul = 0xA
    BITMASK = 0xFFFF

    serial_bytes = bytearray()
    serial_bytes.extend(map(ord, serial))

    for idx,byte in enumerate(serial_bytes):
        if idx == 0:
            tmp = (byte + static_add) & BITMASK
            if len(serial_bytes) == 1:
                return tmp
            continue
        ret = tmp * static_mul
        ret += (byte + static_add) & BITMASK
        tmp = ret

    return hex(ret)

def derive_key(value):
    quotient = 0
    remainder = 0
    ascii_start = 0x30
    ascii_end = 0x7E
    static_div = 0xA
    key = []
     
    while (value + ascii_start) > ascii_end:
        quotient = int(value / static_div)
        remainder = int(value % static_div)
        key.append(remainder + ascii_start)
        value = quotient

    last_char = value + ascii_start
    key.append(last_char)
    key = key[::-1]

    ret = ""
    for s in key:
        ret += chr(s)

    return ret


if __name__ == "__main__":
    print_banner()
    print_target_info()

    try:
        print("[*] generating solutions, abort with CTRL+C")
        while True:
            username = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=5))
            username_value = gen_username_value(username)
            key = derive_key(username_value)

            print(f"[+] generated random username   '{username}'")
            print(f"[+] generated key \t\t'{key}'")

            child = pexpect.spawn("./crack")
            child.expect("Enter your name:")
            child.sendline(username)
            child.expect("Enter your serial:")
            child.sendline(key)
            child.readline()
            out = child.readline()
            out = out.decode('utf-8').strip()

            print(f"[+] checking username and key   '{out}'")
            print("[*]-----------------------------------------")

            time.sleep(1)
    except KeyboardInterrupt:
        exit()
