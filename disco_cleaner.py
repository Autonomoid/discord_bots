import discord
from datetime import datetime, timedelta

API_TOKEN = 'ABCDEFGHIJKLMNOP'
SERVER_ID = 123456789
RETENTION_PERIOD = 90 # days
BOT_CHANNEL_ID = 987654321

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def delete_old_messages(messages):  
    for msg in messages:
        print(f"Deleting message created at {msg.created_at} by user '{msg.author}'.")
        await msg.delete()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    server = client.get_guild(SERVER_ID)
    if not server:
        print(f"Server with ID {SERVER_ID} not found.")
        return
    else:
        print(f"Cleaning server '{server.name}'.") 

    bot_channel = server.get_channel(BOT_CHANNEL_ID)
    await bot_channel.send(f"Cleanup started. Retention period is {RETENTION_PERIOD} days.")

    now = datetime.utcnow()
    cutoff_date = now - timedelta(days=RETENTION_PERIOD)

    text_channels = [channel for channel in server.channels if str(channel.type) == 'text']
    for channel in text_channels:
        print(f"Found channel: '{channel.name}'.")
        old_messages = [message async for message in channel.history(limit=None, before=cutoff_date)]
        message_count = len(old_messages)
        if message_count > 0:
            await delete_old_messages(old_messages)
            await bot_channel.send(f"{message_count} messages deleted from channel '{channel.name}'.")
    
    await bot_channel.send(f"Cleanup completed.")
    await client.close()

client.run(API_TOKEN)
