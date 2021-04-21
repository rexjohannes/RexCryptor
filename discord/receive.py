import discord
import rsa
import base64

bot = discord.Client()

with open('private.pem', mode='rb') as privatefile:
    keydata = privatefile.read()

privateKey = rsa.PrivateKey.load_pkcs1(keydata)


@bot.event
async def on_ready():
    print("Logged in as " + str(bot.user))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.id == your-friends-id:
        try:
            encMessage = base64.b64decode(message.content)
            decMessage = rsa.decrypt(encMessage, privateKey).decode()
            print(decMessage)
        except:
            return
    else:
        return

bot.run("token", bot=False)