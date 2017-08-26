import discord
import logging
import time
import os
import arcorun
import auth

# Enable logging
logging.basicConfig(level=logging.INFO)

# Generate client
client = discord.Client()

@client.event
async def on_ready():
    """Outputs some info at the console and sets the game of the bot."""

    await client.change_presence(game=discord.Game(name="Mention me for instructions!"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(msg):
    """Logs the discord chat and makes the bot react to some keywords."""

    while True:
        try:
            with open(os.path.dirname(os.path.realpath(__file__)) + "/logs/" + time.strftime("%d-%m-%Y", time.localtime(time.time())), "a") as log: # Open log file at /path/to/arcoexbot/logs
                timenow = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(time.time())) #Ex: 14-04-1990 15:23:52
                log.write("%s %s [%s -> %s]: %s\n" % (timenow, msg.author, msg.server, msg.channel, msg.content))
                print("%s %s [%s -> %s]: %s\n" % (timenow, msg.author, msg.server, msg.channel, msg.content))
                #TODO: Add support for the logging module instead to writing to a file.
                break 
        except FileNotFoundError: # If there's no /logs folder
            os.mkdir(os.path.dirname(os.path.realpath(__file__)) + "/logs") # Create it and try again
            
    if msg.content.startswith("<@%s>" % client.user.id) and msg.author != (client.user.name):  # Toggled when the bot is mentioned, but not by itself.
        await arcorun.code(msg, client)

# Start Bot
client.run(auth.bot_token)
