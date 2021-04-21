import discord
import rsa
import base64

bot = discord.Client()

with open('public.pem', mode='rb') as publicfile:
    publicdata = publicfile.read()

publicKey = rsa.PublicKey.load_pkcs1_openssl_pem(publicdata)

@bot.event
async def on_ready():
    print("Logged in as " + str(bot.user))
    while True:
        msg = input("Message: ")
        encMessage = rsa.encrypt(msg.encode(), publicKey)
        channel = bot.get_channel(834432850882592878)
        if channel:
            await channel.send(base64.b64encode(encMessage).decode())


bot.run("token", bot=False)