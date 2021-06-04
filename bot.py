import discord
import os
import asyncio
import datetime

from discord.ext import commands
from dotenv import load_dotenv
from numpy import apply_along_axis
from mainFunctions import *

load_dotenv()
client = commands.Bot(command_prefix="$", help_command=None)
client.activity = discord.Game(name=f"{client.command_prefix}with my balls")

@client.event
async def on_ready():
    print(f"{client.user} is ready to lose money in {len(client.guilds)} server(s).")
    
@client.event
async def on_disconnect():
    print(f"{client.user} has disconnected at {datetime.datetime.now()}.")

@client.event
async def on_resumed():
    print(f"{client.user} has reconnected at {datetime.datetime.now()}.")

def make_embed(desc=""):
    embed = discord.Embed(color=39679, description=desc) if desc else discord.Embed(color=39679)
    embed.set_author(name="George Street Bets", icon_url=client.user.avatar_url)
    embed.set_footer(text="Disclaimer: Not Financial Advice")
    return embed

async def on_loop():
    # ***** CHANGE INPUT VALUES HERE ***** #
    tickerList = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'LTCUSDT', 'BCHUSDT', 'UNIUSDT', 'ADAUSDT', 'DOTUSDT', 'BATUSDT', 'VETUSDT', 'BTGUSDT', 'ETCUSDT', 'HNTUSDT', 'SHIBUSDT', 'DOGEUSDT', 'SOLUSDT', 'LINKUSDT']
    #tickerList = ['BTCUSDT', 'ETHUSDT', 'DOGEUSDT']
    resolutionInput = ['1d', '15m']
    newDay = True
    init()

    await client.wait_until_ready()
    
    # Replace with channel ID that you want to send to
    # Stonkerlicious:  720525680219127838
    # Wholesome Content: 382893006434336780
    channel = client.get_channel(720525680219127838)    # Wholesome content

    # Intro message
    embed = make_embed("Hi my name is George Street Bets, I am a trading bot that is built different to lose money.")
    embed.add_field(name="Watchlist", value="\n".join(map(lambda symb: symb[0:-4], tickerList)))
    embed.add_field(name="Resolutions", value="\n".join(resolutionInput))
    await channel.send(embed=embed)    

    while True:
        waitTime, tradeList, plResultList, nextDayScanSeconds = mainRoutine(tickerList, resolutionInput)

        if newDay == True:
            newDay = False
            # Await is promise, wait until something finishes before running            
            embed = make_embed("Profit/Loss based on Historical Data using *Strategy V1.1*")
            embed.add_field(name="Fetching...", value="Please wait")
            msg = await channel.send(embed=embed)
            for ticker in plResultList:
                await client.wait_until_ready()
            
                if ticker["plTotal"]:
                    symbol = ticker["Ticker"]
                    resolution = ticker["Resolution"]
                    plTotal = ticker["plTotal"]
                    plMin = round(ticker["plMin"])
                    plMax = round(ticker["plMax"]) 
                    winRate = ticker["winRate"]
                    
                    embed.insert_field_at(index=(len(embed.fields) - 1 if len(embed.fields) >= 1 else 0), name=f"{symbol} - {resolution}", value=f"Total P/L: {plTotal}%\tLowest P/L: {plMin}%\tHighest P/L: {plMax}%\tWR: {winRate}%", inline=False)
                    await msg.edit(embed=embed)
            embed.remove_field(index=(len(embed.fields) - 1))
            await msg.edit(embed=embed)
 

        if tradeList:
            embed = make_embed("Buy/Sell Indicators using *Strategy V1.1*")
            embed.add_field(name="Fetching...", value="Please wait")
            msg = await channel.send(embed=embed)
            for ticker in tradeList:
                await client.wait_until_ready()
            
                if ticker["Time"]:
                    symbol = ticker["Ticker"]
                    resolution = ticker["Resolution"]
                    tradePrice = round(ticker["tradePrice"], 2)
                    tradeTime = ticker["Time"]
                    tradeType = ticker["Trade"] 
                    plAvg = ticker["plAvg"]
                    winRate = ticker["winRate"]
                    latestPrice = apiLatestPrice(symbol + "USDT")

                    embed.insert_field_at(index=(len(embed.fields) - 1 if len(embed.fields) >= 1 else 0), name=f"{symbol} - {resolution} - {tradeTime}", value=f"WR: {winRate}%\nAvg P/L: {plAvg}%\n{tradeType} @ ${tradePrice}\nLatest Price: ${latestPrice}", inline=False)
                    await msg.edit(embed=embed)
            embed.remove_field(index=(len(embed.fields) - 1))
            await msg.edit(embed=embed)   

        await asyncio.sleep(waitTime)  # Seconds 
            
        if nextDayScanSeconds <= refreshSwitch(resolutionInput[-1]):
            resolutionInput = ['1d', '15m']
            newDay = True
        else:
            resolutionInput = ['15m']




client.loop.create_task(on_loop())

client.run(os.getenv("DISCORD_API"))    # Turns on the bot 
