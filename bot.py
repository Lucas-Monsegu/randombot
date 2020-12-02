#!/usr/bin/python3.8
import discord
import random
import asyncio

TOKEN = 'NTE4NTY0MTY1NDA5OTY0MDM3.Dzd8EA._X-hRwmJ4pZQoLN3QZ865Nlcg-I'
SYMBOL = '!'
CHANNELS = {}
client = discord.Client()


async def randduel(message, words):
    if len(words) == 1 and words[0] == 'channel':
        if message.author.voice is None or message.author.voice.channel is None:
            await message.channel.send('You are not in any voice channel')
            return
        li = list(map(lambda x: x.display_name, message.author.voice.channel.members))
        if len(li) < 2:
            await message.channel.send('You are alone.')
            return
        p1 = li.pop(random.randint(0, len(li)-1))
        p2 = li.pop(random.randint(0, len(li)-1))
        await message.channel.send(f'{p1} vs {p2}')
        return
    if len(words) < 2:
        await message.channel.send('Not enough arguments')
        return
    p1 = words.pop(random.randint(0, len(words)-1))
    p2 = words.pop(random.randint(0, len(words)-1))
    await message.channel.send(f'{p1} vs {p2}')


async def rand(message, words):
    if len(words) == 1 and words[0] == 'channel':
        if message.voice is not None and message.voice.channel is not None:
            await message.channel.send('You are not in any voice channel')
            return
        li = list(map(message.voice.channel.members, lambda x: x.display_name))
        r = li[random.randint(0, len(li)-1)]
        await message.channel.send(r)
        return

    if len(words) == 2 and words[0].isdigit() and words[1].isdigit():
        await message.channel.send(str(random.randint(*sorted([int(words[0]), int(words[1])]))))
    else:
        await message.channel.send(words[1:][random.randint(0, len(words)-1)])


async def helpmessage(message, words):
    m = ''
    await message.channel.send(m)
COMMANDS = {
    "random": rand,
    "randomduel": randduel
}


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user or len(message.content) <= 0 or message.content[0] != SYMBOL:
        return
    words = message.content[1:].split()
    print("Receive:", words)
    if words[0] in COMMANDS.keys():
        await COMMANDS[words[0]](message, words[1:])


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

try:
    loop = asyncio.get_event_loop()
    client.run(TOKEN)
except KeyboardInterrupt:
    print("Received exit, exiting")
