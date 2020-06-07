import discord
from discord.ext import commands
import json

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed=discord.Embed(title="Command not found! <:2446_cursed_flushed:715119563078893609>", description="Type `=help` for a list of all available commands.", color=0xff0000)
            await ctx.send(embed=embed)


    @commands.command()
    async def help(self, ctx, command=''):
        help_emoji = "<:6598_pain:715119563301322752>"
        region_s = ''
        with open('./data/regions.json', 'r') as r:
            regions = json.load(r)
            for region in regions.items():
                region_s += f"`{region[0]}`"+', '
        if command == '':
            embed=discord.Embed(title="Rune Legend Help", description="Type `=help <command>` for detailed help on each command!\n", color=0xff0000)
            embed.add_field(name="`=runes`", value=f"{help_emoji} Get runes for a specified champion and/or role", inline=False)
            embed.add_field(name="`=stats`", value=f"{help_emoji} Information about a specified summoner's level and ranks", inline=False)
            await ctx.send(embed=embed)
        elif command == 'runes':
            embed=discord.Embed(title="Help for \'runes\'", description="`=runes <champion> [role]`", color=0xff0000)
            embed.add_field(name="Tip", value="You can write only a few letters from the beggining of the name as long as they are unique!", inline=True)
            await ctx.send(embed=embed)
        elif command == 'stats':
            embed=discord.Embed(title="Help for \'stats\'", description="`=stats <region> <summoner>`", color=0xff0000)
            embed.add_field(name="Here is a list of all regions:", value=region_s, inline=False)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Command not found! <:2446_cursed_flushed:715119563078893609>", description="Type `=help` for a list of all available commands.", color=0xff0000)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
