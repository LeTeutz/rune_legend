import discord
import os
from discord.ext import commands, tasks
import io
import json

token = ''

with open('config.json', 'r') as f:
    config_dict = json.load(f)
    token = config_dict["token"]

prefix = '='

client = commands.Bot(command_prefix = prefix)

client.remove_command('help')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=f'{prefix}help'))
    print('Bot is online')

@client.command(hidden=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    print (f'loaded {extension}')


@client.command(hidden=True)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    print (f'reloaded {extension}')

@client.command(hidden=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    print (f'unloaded {extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(token)
