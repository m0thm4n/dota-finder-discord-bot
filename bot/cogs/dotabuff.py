import asyncio
import datetime as dt
import enum
import random
import re
import typing as t
from enum import Enum

import aiohttp
import discord
from discord.ext import commands
import requests

class DotaBuff(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.get_player(member.guild).teardown()

    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        else:
            await payload.player.advance()

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Music commands are not available in DMs.")
            return False

        return True

    @commands.command(name="pl", aliases=["lookup"])
    async def players_lookup_command(self, ctx, *, query: t.Optional[str]):
        username = query
        
        mapped_data = {"username": username}
                
        resp = requests.post("http://localhost:8080/playerSearch", json=mapped_data)
        
        print(resp.content)
        
        resp_json = resp.json()
        
        embed = discord.Embed(
            title="Player Profiles",
            description=f"A list of Player Profiles",
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar)
        for value in resp_json["players"]:
            embed.add_field(
                name="Player Name",
                value=value["player"],
                inline=False
            )
            embed.add_field(
                name="Player's URL",
                value=value["playerURL"],
                inline=False
            )
        
        msg = await ctx.send(embed=embed)

    @commands.command(name="l", aliases=["playerLookup"])
    async def player_lookup_command(self, ctx, *, query: t.Optional[str]):
        username = query
        
        mapped_data = {"username": username}
                
        resp = requests.post("http://localhost:8080/playerLookup", json=mapped_data)
        
        print(resp.content)
        
        resp_json = resp.json()
        
        embed = discord.Embed(
            title="Player Profile",
            description=f"Details about a players profile",
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar)
        for value in resp_json["player"]:
            embed.set_image(url=value["rankName"])
        
        msg = await ctx.send(embed=embed)
        
        embed = discord.Embed(
            title="Most Played Heroes",
            description=f"Players most played heroes in DotA 2",
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar)
        for value in resp_json["player"]:
            embed.set_image(url=value["rankName"])
            embed.add_field(name=,value=,inline=)
            
        msg = await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(DotaBuff(bot))
