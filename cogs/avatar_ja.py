import discord
from discord.ext import commands
from evs import default

class Avatar_Ja(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    # Commands
    @commands.command(name='アバター')
    async def __avatar(self, ctx):
        if (ctx.message.mentions.__len__() > 0):
            for user in ctx.message.mentions:
                pfp = str(user.avatar_url)
                embed = discord.Embed(title="**" +user.name + "**さんのアバター", description="[Link]" + "(" + pfp + ")",
                                      color=0xeff0f1)
                embed.set_image(url=pfp)
                await ctx.trigger_typing()
                await ctx.send(embed=embed)
        else:
            pfp = ctx.author.avatar_url
            embed = discord.Embed(title="**" + ctx.author.name + "**さんのアバター", description="[Link]" + "(" + str(pfp) + ")",
                                color=0xeff0f1)
            embed.set_image(url=pfp)
            await ctx.trigger_typing()
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Avatar_Ja(bot))
