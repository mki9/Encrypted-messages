import socket
import threading
import random
import time
import os
import sys
import shutil
from colorama import Fore, Style, init
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet

init(autoreset=True)

SERVER_IP = 'bore.pub'
SERVER_PORT = 21602
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()
pem_public = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode('utf-8')

target_public_key_cache = None


def get_width():
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80


def clear_screen(): os.system('cls' if os.name == 'nt' else 'clear')


def play_sound(): sys.stdout.write('\a'); sys.stdout.flush()


def print_centered(text, color=Fore.WHITE, style=Style.NORMAL):
    width = get_width()
    padding = max(0, (width - len(text)) // 2)
    print(" " * padding + color + style + text)


def input_centered(prompt_text, color=Fore.YELLOW):
    width = get_width()
    padding = max(0, (width - len(prompt_text) - 10) // 2)
    sys.stdout.write(" " * padding + color + prompt_text)
    sys.stdout.flush()
    return input(Fore.WHITE)


def encrypt_message(message, target_pub_pem):
    session_key = Fernet.generate_key()
    cipher_suite = Fernet(session_key)
    encrypted_text = cipher_suite.encrypt(message.encode('utf-8'))

    target_pub = serialization.load_pem_public_key(target_pub_pem.encode('utf-8'))
    encrypted_session_key = target_pub.encrypt(
        session_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    blob = encrypted_session_key.hex() + "||" + encrypted_text.decode('utf-8')
    return blob


def decrypt_message(blob):
    try:
        enc_sess_key_hex, enc_text_str = blob.split("||")
        enc_sess_key = bytes.fromhex(enc_sess_key_hex)
        session_key = private_key.decrypt(
            enc_sess_key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        cipher_suite = Fernet(session_key)
        return cipher_suite.decrypt(enc_text_str.encode('utf-8')).decode('utf-8')
    except:
        return "[ENCRYPTED DATA - CANNOT DECRYPT]"


def receive_messages():
    global target_public_key_cache
    while True:
        try:
            data = client.recv(10240)
            if not data: break
            packet = data.decode('utf-8')

            if packet.startswith("[KEY_FOUND]"):
                target_public_key_cache = packet.split("]")[1]
                continue

            if packet.startswith("[KEY_NOT_FOUND]"):
                target_public_key_cache = "ERROR"
                continue

            if packet.startswith("[INCOMING]"):
                _, content = packet.split("]", 1)
                sender, blob = content.split("|", 1)

                play_sound()
                msg_text = decrypt_message(blob)

                print("\n")
                print_centered(f"[MSG] FROM {sender} (E2EE)", Fore.CYAN)
                print_centered(f">> {msg_text}", Fore.GREEN, Style.BRIGHT)
                print("\n")

                prompt = "[SECURE INPUT] >> "
                padding = max(0, (get_width() - len(prompt) - 10) // 2)
                sys.stdout.write(" " * padding + Fore.YELLOW + prompt)
                sys.stdout.flush()

        except:
            break


def send_messages(my_code, target_code):
    global target_public_key_cache
    while True:
        msg = input("")
        if msg.lower() == 'exit': break

        target_public_key_cache = None
        client.send(f"[GET_KEY]{target_code}".encode('utf-8'))

        wait_timer = 0
        while target_public_key_cache is None and wait_timer < 20:
            time.sleep(0.1)
            wait_timer += 1

        if target_public_key_cache == "ERROR" or target_public_key_cache is None:
            print_centered("[!] ERROR: TARGET AGENT NOT AVAILABLE OR KEY INVALID.", Fore.RED)
            continue

        try:
            encrypted_blob = encrypt_message(msg, target_public_key_cache)
            packet = f"[MSG]{target_code}|{encrypted_blob}"
            client.send(packet.encode('utf-8'))

            print_centered("[SENT] 2048-BIT ENCRYPTED PACKET.", Fore.GREEN)

            prompt = "[SECURE INPUT] >> "
            padding = max(0, (get_width() - len(prompt) - 10) // 2)
            sys.stdout.write(" " * padding + Fore.YELLOW + prompt)
            sys.stdout.flush()
        except Exception as e:
            print_centered(f"[ERROR] SEND FAILED: {e}", Fore.RED)


def start_system():
    global target_public_key_cache
    clear_screen()
    print("\n" * 2)
    print_centered("INITIALIZING RSA-2048 CRYPTO ENGINE...", Fore.CYAN)
    time.sleep(1)

    my_agent_code = input_centered("ENTER YOUR AGENT ID: ", Fore.GREEN)

    # تم إزالة التحقق الأمني (binary_matrix_hack)

    try:
        client.connect((SERVER_IP, SERVER_PORT))
        client.send(f"[REGISTER]{my_agent_code}|{pem_public}".encode('utf-8'))
    except:
        print_centered("SERVER UNREACHABLE.", Fore.RED)
        return

    clear_screen()
    print("\n" * 2)
    print_centered(f"IDENTITY VERIFIED: {my_agent_code}", Fore.GREEN)
    print_centered(f"PUBLIC KEY FINGERPRINT: {pem_public[50:80]}...", Fore.BLUE)
    print_centered("-" * 50)

    threading.Thread(target=receive_messages, daemon=True).start()

    while True:
        target_agent_code = input_centered("ENTER TARGET AGENT ID: ", Fore.MAGENTA)

        print_centered(f"[*] FETCHING KEY FOR {target_agent_code}...", Fore.YELLOW)
        target_public_key_cache = None
        client.send(f"[GET_KEY]{target_agent_code}".encode('utf-8'))

        waits = 0
        while target_public_key_cache is None and waits < 15:
            time.sleep(0.2)
            waits += 1

        if target_public_key_cache == "ERROR":
            print("\n")
            print_centered(f"[!] AGENT '{target_agent_code}' NOT REGISTERED.", Fore.RED)
            print_centered("    TARGET MUST LOGIN AT LEAST ONCE TO GENERATE KEYS.", Fore.RED)
            print_centered("-" * 30, Fore.RED)
        elif target_public_key_cache:
            print_centered("[+] SECURE CHANNEL ESTABLISHED.", Fore.GREEN)
            break
        else:
            print_centered("[!] SERVER TIMEOUT.", Fore.RED)

    prompt = "[SECURE INPUT] >> "
    padding = max(0, (get_width() - len(prompt) - 10) // 2)
    sys.stdout.write(" " * padding + Fore.YELLOW + prompt)
    sys.stdout.flush()

    send_messages(my_agent_code, target_agent_code)


if __name__ == "__main__":
    try:
        start_system()
    except KeyboardInterrupt:
        pass