import discord
from discord.ext import commands
import requests
import estaticos
import os
import webserver

WA_TOKEN = os.getenv("WA_TOKEN")
DS_TOKEN = os.getenv("DS_TOKEN")


def WaApiRefreshToken():
  global WA_TOKEN
  url = f"https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id={estaticos.WA_ID}&client_secret={estaticos.WA_SECRET}&fb_exchange_token={WA_TOKEN}"

  response = requests.get(url)
  data = response.json()

  if "access_token" in data:
      print(f"Viejo Token: {WA_TOKEN}")
      WA_TOKEN = data["access_token"]
      print(f"Nuevo Token: {WA_TOKEN}")
  else:
      print(f"Error al refrescar Token de Whatsapp: {data}")

def WaApiSendMessage(mensaje):
  url = f"https://graph.facebook.com/v18.0/{estaticos.ID_NUM}/messages"

  headers = {
      "Authorization": f"Bearer {WA_TOKEN}",
      "Content-Type": "application/json"
  }

  data = {
      "messaging_product": "whatsapp",
      "to": estaticos.NUMEROS_DESTINO,
      "type": "text",
      "text": {"body": mensaje}
  }

  response = requests.post(url, headers=headers, json=data)
  print(response.json())


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event 
async def on_ready():
  print(f"Estamos dentro! {bot.user}")

@bot.event
async def on_message(message):
  if message.author == bot.user:
        return
  if message.channel.name == "voz-logs":
    await message.channel.send("Alertando...")
    if message.author.name == "Quark Logger":
      WaApiSendMessage(f"Alguien entro o salio de discord")
    else:
       WaApiSendMessage(f"{message.author.name} dice: {message.content}")
  await bot.process_commands(message)

@bot.command()
async def test(ctx, *args):
  respuesta = ''.join(args)
  await ctx.send(respuesta)

webserver.keep_alive()
bot.run(DS_TOKEN)

