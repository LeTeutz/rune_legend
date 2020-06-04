import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def help(self, ctx, command=''):
        print(command)
        if command == '':
            embed=discord.Embed(title="Help Page", description="Type `=help <command>` for detailed help on each command", color=0xff0000)
            embed.add_field(name="General:", value="`runes`", inline=True)
            await ctx.send(embed=embed)
        elif command == 'runes':
            embed=discord.Embed(title="Help \'runes\'", description="`=runes <champion> [role]`", color=0xff0000)
            embed.add_field(name="Tip", value="You can write only a few letters from the beggining of the name as long as they are unique!", inline=True)
            await ctx.send(embed=embed)
            print('alo')

def setup(client):
    client.add_cog(Help(client))
