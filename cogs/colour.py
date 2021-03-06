import time
import aiohttp
import discord
import openpyxl
import importlib
import os
import sys

from discord.ext import commands
from evs import permissions, default, http, dataIO
from discord.ext.commands import has_permissions


class Colour(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    @commands.command(aliases=['import colour'])
    @has_permissions(administrator=True, manage_messages=True, manage_roles=True)
    async def import_color(self, ctx, *, content: str):
        """ Loads color roles. <content> is a cirteria role\n* Alert : Don't use it double."""
        roles = ctx.guild.roles
        position = 0
        for i in range(0, len(roles)):
            if roles[i].name == content:
                position = roles[i].position + 1
        if position == 0:
            return await ctx.send("I can't understand of position ;-;")
        filename = "lib/color.xlsx"
        book = openpyxl.load_workbook(filename)
        sheet = book.active
        embed = discord.Embed(title='**Import**', description='Started to import whole roles.', colour=0xeff0f1)
        await ctx.send(embed=embed)
        for i in range(3, 137):
            name = sheet["B" + str(i)].value
            color_code = sheet["C" + str(i)].value.replace("#", "")
            colors = discord.Colour(int(color_code, 16))
            role = await ctx.guild.create_role(name=name, colour=colors)
            positions = {role: position}
            await ctx.guild.edit_role_positions(positions=positions)
        embed = discord.Embed(title='**Import**', description='Completely imported whole roles.', colour=0xeff0f1)
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['remove colour'])
    @has_permissions(administrator=True, manage_messages=True, manage_roles=True)
    async def remove_color(self, ctx):
        """ Removes color roles. """
        roles = ctx.guild.roles
        position = 0
        filename = "lib/color.xlsx"
        book = openpyxl.load_workbook(filename)
        sheet = book.active
        colors = []
        for i in range(3, 137):
            colors.append(sheet["B" + str(i)].value)
        embed = discord.Embed(title='**Remove**', description='Trying to remove whole roles.', colour=0xeff0f1)
        await ctx.send(embed=embed)
        for i in range(0, len(roles)):
            if roles[i].name in colors:
                await roles[i].delete(reason='refra')
        embed = discord.Embed(title='**Remove**', description='Completely Removed whole roles.', colour=0xeff0f1)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Colour(bot))
