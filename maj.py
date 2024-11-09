import datetime,os,sys
import discord
from discord import Option
import google.generativeai as genai
import dotenv
from dotenv import load_dotenv
load_dotenv()

geminikey = os.environ.get('APIKEY1') #GEMINIのAPIキー
bottoken = os.environ.get("TOKEN2") #ボットのトークン
translateChID = 1296696402742611979 #翻訳チャンネルの指定

genai.configure(api_key=geminikey)
model = genai.GenerativeModel('gemini-1.5-flash')

client = discord.Bot()
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"Last on_ready executed:{datetime.datetime.now()}(+9:00 JST)"))
    print(f"{datetime.datetime.now()}:on_ready  client.user:{client.user} ")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    elif message.channel.id == translateChID:
        print(f"{datetime.datetime.now()}:on_message:{message.content}")
        response = model.generate_content(f"次の文章をカジュアルな感じで英語に翻訳してその文章だけ返してください。また日本語にもカジュアルな感じで翻訳してその文章だけ返してください。：{message.content}")
        print(f"response:\ntext={response.text}done={response._done}\niterator={response._iterator}\nerror={response._error} \nusage_metadata:\n{response.usage_metadata}")
        if response._done!="Tlue":
            await message.channel.send(response.text)
            print("Done")
        else:
            await message.channel.send(f'The response appears to have failed. \nPlease contact your administrator.\ndone={response._done}\niterator={response._iterator}\nerror={response._error} ')
            print("Error")
        return

client.run(f"{bottoken}")
