#!/usr/bin/python3.8
import asyncio
import os
import random as rand

import discord
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv
from tabulate import tabulate

from utils import args_to_words

load_dotenv()
TOKEN = os.getenv("TOKEN")
SYMBOL = "!"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    intents=intents, command_prefix=SYMBOL, description="I make randomness"
)


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.command()
async def dmrandom(ctx: Context, *args):
    """
    Select someone in private message then send him direct message
    [@people]
    """
    try:
        users = [await commands.UserConverter().convert(ctx, people) for people in args]
    except commands.errors.UserNotFound as e:
        await ctx.send(str(e))
    await users[rand.randint(0, len(users)-1)].send(f"You have been chosen !")


@bot.command()
async def coinflip(ctx: Context, *args):
    """
    Flip a coin
    *no words
    """
    await ctx.send(["Heads", "Tails"][rand.randint(0,1)])


@bot.command()
async def shuffle(ctx: Context, *args):
    """
    Shuffle words
    [words] -> shuffle the words
    """
    words = await args_to_words(ctx, args)
    rand.shuffle(words)
    await ctx.send(" ".join(words))


@bot.command()
async def randomteam(ctx: Context, *args):
    """
    Create random teams
    (number of teams) [words]

    """
    if len(args) < 1:
        return await ctx.send("You need to provide at least one team")
    nb_teams = "".join(args[0])
    if not nb_teams.isdigit():
        return await ctx.send("Number of teams must be a number")
    nb_teams = int(args[0])
    words = await args_to_words(ctx, args[1:])
    rand.shuffle(words)
    teams = [[] for _ in range(nb_teams)]
    c = 0
    for word in words:
        teams[c].append(word)
        c = (c + 1) % nb_teams
    headers = [f"Team {i}" for i in range(nb_teams)]
    await ctx.send(
        f"```{tabulate(list(zip(*teams)),headers=headers,tablefmt='fancy_grid')}```"
    )


@bot.command()
async def randomduel(ctx: Context, *args: list[str]):
    """
    Creates a duel between two people
    [words] -> random between all your words that are space separated
    """

    words = list(map(lambda li: "".join(li), args))

    if len(words) == 0:
        if not ctx.author.voice or not ctx.author.voice:
            return await ctx.send("You are not in any voice channel")
        words = list(
            map(lambda x: x.display_name, message.author.voice.channel.members)
        )

    if len(words) < 2:
        return await message.channel.send("Need at least 2 words")
    p1 = words.pop(rand.randint(0, len(words) - 1))
    p2 = words.pop(rand.randint(0, len(words) - 1))
    await ctx.send(f"{p1} vs {p2}")


@bot.command()
async def random(ctx: Context, *args: list[str]):
    """
    make a random between your words
    (number) (number) -> random between those two numbers
    [words] -> random between all your words that are space seperated

    """
    words = await args_to_words(ctx, args)

    if len(words) == 2 and words[0].isdigit() and words[1].isdigit():
        await ctx.send(str(rand.randint(*sorted(map(int, words)))))
    else:
        await ctx.send(words[rand.randint(0, len(words) - 1)])


bot.run(TOKEN, reconnect=True)
