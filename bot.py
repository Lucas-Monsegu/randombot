import discord
import random
import os
import asyncio

TOKEN = 'NTE4NTY0MTY1NDA5OTY0MDM3.Dzd8EA._X-hRwmJ4pZQoLN3QZ865Nlcg-I'
SYMBOL = '!'
CHANNELS = {}
client = discord.Client()

async def timeout():
    while True:
        li = []
        for chan in CHANNELS.values():
            if chan[0].is_connected() and not chan[1].is_playing():
                li.append(chan)
        await asyncio.sleep(20)
        for chan in li:
            if chan[0].is_connected() and not chan[1].is_playing():
                if chan in CHANNELS.values():
                    print('Timeout', chan.server.name)
                    await chan[1].stop()
                    await chan[0].disconnect()
                    CHANNELS.pop(chan[0].server.id, None)
async def stop(message, words):
    if not CHANNELS.get(message.server.id) or not CHANNELS.get(message.server.id)[1].is_playing():
        await client.send_message(message.channel, "Billy is not doing anything")
    else:
        CHANNELS.get(message.server.id)[1].stop()
        await client.send_message(message.channel, "Billy stopped")

async def music(message, words):
    if message.author.voice.voice_channel == None or message.author.voice.voice_channel == client.server_voice_state:
        await client.send_message(message.channel, "User not in voice channel")
        return
    
    if not CHANNELS.get(message.server.id):
        voice = await client.join_voice_channel(message.author.voice_channel)
    else:
        voice = CHANNELS[message.server.id][0]
    if voice.channel != message.author.voice_channel:
        if voice.is_connected:
            await voice.move_to(message.author.voice_channel)
        else:
            CHANNELS.pop(message.server.id, None)
            music(message, words)
            return
    if CHANNELS.get(message.server.id) and CHANNELS[message.server.id][1].is_playing():
        await client.send_message(message.channel, "Billy is already playing")
        return
    url = words[1]
    try:
        beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5" 
        player = await voice.create_ytdl_player(url=url, before_options=beforeArgs)
    except Exception as e:
        await client.send_message(message.channel, "Billy do not recognize this URL because he only knows YOUTUBE !")
        await voice.disconnect()
        print(e)
        return
    player.volume = 0.1
    player.start()
    CHANNELS[message.server.id] = (voice, player)

async def rand(message, words):
    if len(words) < 2:
        return
    if words[1] == 'sc2':
        await client.send_message(message.channel, ['Lucas', 'Theo', 'Adrien'][random.randint(0, 2)])
        return
    if len(words) < 3:
        return
    if words[1].isdigit() and words[2].isdigit():
        await client.send_message(message.channel, str(random.randint(*sorted([int(words[1]), int(words[2])]))))
    else:
        await client.send_message(message.channel, words[1:][random.randint(0, len(words)-2)])

async def botCom(message):
    if message.author.name != 'Itectobot':
        return
    if 'a gagné.' in message.content and '@Luka' in message.content:
        victorycount = 0
        if os.path.exists('lukascore.txt'):
            with open('lukascore.txt', 'r') as f:
                victorycount = int(f.read())
        victorycount += 1
        await client.send_message(message.channel, 'Luka\'s victory count:'+ str(victorycount))
        with open('lukascore.txt', 'w+') as f:
            f.write(str(victorycount))
COMMANDS =  {
            'play': music,
            'random': rand,
            'stop': stop,
            }
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user or len(message.content) <= 0 or message.content[0] != SYMBOL:
        return
    words = message.content[1:].split()
    print("Receive:", words)
    if words[0] in COMMANDS.keys():
        await COMMANDS[words[0]](message, words)

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
loop = asyncio.get_event_loop()
asyncio.ensure_future(timeout() ,loop=loop)
client.run(TOKEN)