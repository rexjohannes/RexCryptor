import rsa
import tkinter
import base64

#publicKey, privateKey = rsa.newkeys(512)
with open('public.pem', mode='rb') as publicfile:
    publicdata = publicfile.read()
with open('private.pem', mode='rb') as privatefile:
    keydata = privatefile.read()

privateKey = rsa.PrivateKey.load_pkcs1(keydata)
publicKey = rsa.PublicKey.load_pkcs1_openssl_pem(publicdata)

def send(event=None):
    message = my_msg.get()
    my_msg.set("")  # Clears input field.
    encMessage = rsa.encrypt(message.encode(), publicKey)
    msg = base64.b64encode(encMessage)
    top.clipboard_clear()
    top.clipboard_append(msg)
    msg_list.insert(tkinter.END, msg)

def decrypt(event=None):
    message = my_msg.get()
    my_msg.set("")
    encMessage = base64.b64decode(message)
    decMessage = rsa.decrypt(encMessage, privateKey)
    msg_list.insert(tkinter.END, decMessage)

def exit(event=None):
    exit()

top = tkinter.Tk()
top.title("RSA-Chat")
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

messages_frame.pack()
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.bind("<Escape>", decrypt)
entry_field.pack()
send_button = tkinter.Button(top, text="Encrypt", command=send).pack(side=tkinter.LEFT)
decrypt_button = tkinter.Button(top, text="Decrypt", command=decrypt).pack(side=tkinter.RIGHT)
tkinter.Button(top, text="Exit", command=exit).pack(side=tkinter.TOP)

top.mainloop()