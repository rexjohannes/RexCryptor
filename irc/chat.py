#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import webbrowser
import rsa
import base64

with open('public.pem', mode='rb') as publicfile:
    publicdata = publicfile.read()
with open('private.pem', mode='rb') as privatefile:
    keydata = privatefile.read()

privateKey = rsa.PrivateKey.load_pkcs1(keydata)
publicKey = rsa.PublicKey.load_pkcs1_openssl_pem(publicdata)


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if msg == "{quit}":
                client_socket.close()
                top.quit()
                exit()
            try:
                name, content = msg.split(': ')
                encMessage = base64.b64decode(content)
                decMessage = rsa.decrypt(encMessage, privateKey)
#                print(decMessage.decode())
                msg_list.insert(tkinter.END, name + ": " + str(decMessage.decode()))
            except:
                msg_list.insert(tkinter.END, msg)

        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    if msg == "{quit}":
        client_socket.send(bytes(msg, "utf8"))
        client_socket.close()
        top.quit()
        exit()
    if msg.startswith("auth"):
        auth, msg = msg.split(' ')
        client_socket.send(bytes(msg, "utf8"))
    else:
        encMessage = rsa.encrypt(msg.encode(), publicKey)
        msg = base64.b64encode(encMessage).decode()
        client_socket.send(bytes(msg, "utf8"))

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

top = tkinter.Tk()
top.title("Chat-Client")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
HOST = input('Host: ')
PORT = input('Port: ')
if not PORT:
    PORT = 33001
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
webbrowser.open("https://api.rexum.space/get/key")

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()