import functools
from functools import wraps

from discord.ext.commands import Context

from exceptions import NotInAVoiceChannel


async def args_to_words(ctx: Context, args):
    words = list(map(lambda li: "".join(li), args))
    if len(words) == 0:
        if not ctx.author.voice or not ctx.author.voice:
            await ctx.send("You are not in any voice channel")
            raise NotInAVoiceChannel()
        words = list(map(lambda x: x.display_name, ctx.author.voice.channel.members))

    return words
