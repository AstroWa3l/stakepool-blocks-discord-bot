# bot.py
from email import message
import os
from webbrowser import get
import discord
import pandas as pd
from discord.ext import tasks
from dotenv import load_dotenv
load_dotenv()
import koios_python
import requests

TOKEN = os.getenv('TEST_DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
POOL = os.getenv('POOL_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Create Koios Object 
# Not working consistently so using my own function for latest blocks for now
kp = koios_python.URLs()

# Look up pool info
pool_info = kp.get_pool_info(POOL)
ticker = pool_info[0]['meta_json']['ticker']

# Get the latest blocks list
def get_block_list(content_range="0-999"):
        
        headers = {'Range': content_range}
        reqs = requests.get('https://api.koios.rest/api/v0/blocks', headers=headers)
        print(reqs.status_code)
        # add try/except api error handling
        try:
                block_info = reqs.json()
                pd_block_info = pd.DataFrame(block_info)
                return pd_block_info
        
        except ApiError as e:
                print(e)
        
##################################################################################################

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@tasks.loop(seconds=22)
async def main():
        
        channel = client.get_channel(int(CHANNEL_ID))
        messages = [msg async for msg in channel.history(limit=1)]
        contents = [message.content for message in messages]
        
        
        # Get Data of last 3 blocks every few seconds
        # latest_3_blocks = kp.get_blocks(content_range="0-2")
        latest_3_blocks = get_block_list(content_range="0-2")
        latest_3_blocks = pd.DataFrame(latest_3_blocks)

        
        if type(latest_3_blocks) == type(pd.DataFrame()):
                
                if len(latest_3_blocks) > 0:
                        print("Latest Block Hash: {}\nBlock Height No: {}\nMade By Pool: {}"
                              .format(latest_3_blocks.hash[0],latest_3_blocks.block_height[0],latest_3_blocks.pool[0]))
                
                        for block in range(len(latest_3_blocks)):
                                if latest_3_blocks.pool[block] == POOL:
                                        print("AHOY!")
                                        
                                        message="""
                                        **Ahoy! More Plunder** 🏴‍☠️
                                        \n**New Block** 🧱 **added to** ***{}*** **pool's treasure chest**💰
                                        \n🪪 **Pool ID:** ***{}***
                                        \n#️⃣ **Hash:** ***{}***
                                        \n🕰 **Epoch:** ***{}***   🔢**Height_No:** ***{}***
                                        \n📏 **Size**: ***{}*** kB  🔢**Number of Tx:** ***{}***
                                        \n⚙️ **Total Blocks:** ***{}***
                                        \n🧱**Info:** https://cexplorer.io/block/{}
                                        """.format(ticker,
                                                   latest_3_blocks.pool[block],
                                                   latest_3_blocks.hash[block],
                                                   latest_3_blocks.epoch_no[block],
                                                   latest_3_blocks.block_height[block],
                                                   round(latest_3_blocks.block_size[block].astype(int)/1000, 2),
                                                   latest_3_blocks.tx_count[block],
                                                   pool_info[0]['block_count'],
                                                   latest_3_blocks.hash[block],
                                                   )
                                        for i in contents:
                                                if i.__contains__(latest_3_blocks.hash[block]) == False:
                                                        await channel.send(message)
                                                        print("Discord Message Sent")
                                                        

@client.event
async def on_ready():
        if not main.is_running():
                main.start()



client.run(TOKEN)