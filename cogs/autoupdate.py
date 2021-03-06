import discord
from discord.ext import commands
from evs import default
from evs import permissions, default, http, dataIO
import requests
import os

class Autoupdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    # Commands

    @commands.command()
    @commands.check(permissions.is_owner)
    async def update(self, ctx, filename: str):
        await ctx.trigger_typing()
        await ctx.send("Updating source code...")
        link = "https://raw.githubusercontent.com/Shio7/Keter/master/cogs/" + filename + ".py"
        r = requests.get(link, allow_redirects=True)
        if os.path.isfile('./cogs/' + filename + ".py"):
            try:
                self.bot.unload_extension(f"cogs.{filename}")
            except Exception as e:
                return await ctx.send(default.traceback_maker(e))
            await ctx.send(f"Unloaded extension **{filename}.py**")
            os.remove('./cogs/' + filename + ".py")
            open('./cogs/' + filename + ".py", 'wb').write(r.content)
        else:
            open('./cogs/' + filename + ".py", 'wb').write(r.content)
        await ctx.send("Updated: "+filename+".py")
        """ Loads an extension. """
        try:
            self.bot.load_extension(f"cogs.{filename}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        await ctx.send(f"Loaded extension **{filename}.py**")

    @commands.command()
    @commands.check(permissions.is_owner)
    async def remove(self, ctx, filename: str):
        if os.path.isfile('./cogs/' + filename + ".py"):
            os.remove('./cogs/' + filename + ".py")
            await ctx.send(f"**{filename}.py** removed")
        else:
            await ctx.send(f"Can't find **{filename}.py**")
            
    @commands.command()
    @commands.check(permissions.is_owner)
    async def allupdate(self, ctx):
        await ctx.trigger_typing()
        await ctx.send("Updating source code...")
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                link = "https://raw.githubusercontent.com/Shio7/Keter/master/cogs/" + name + ".py"
                r = requests.get(link, allow_redirects=True)
                if os.path.isfile('./cogs/' + name + ".py"):
                    try:
                        self.bot.unload_extension(f"cogs.{name}")
                    except Exception as e:
                        return await ctx.send(default.traceback_maker(e))
                    await ctx.send(f"Unloaded extension **{name}.py**")
                    os.remove('./cogs/' + name + ".py")
                    open('./cogs/' + name + ".py", 'wb').write(r.content)
                else:
                    open('./cogs/' + name + ".py", 'wb').write(r.content)
                await ctx.send("Updated: "+name+".py")

                try:
                    self.bot.load_extension(f"cogs.{name}")
                except Exception as e:
                    return await ctx.send(default.traceback_maker(e))
                await ctx.send(f"Loaded extension **{name}.py**") 
        await ctx.send("All modules updated")      
            
def setup(bot):
    bot.add_cog(Autoupdate(bot))
