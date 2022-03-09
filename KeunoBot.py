from turtle import title
from discord.ext import commands
import discord
from discord.utils import *
import requests
from pyfade import *
import os
from colorama import *
import time
import random





def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn


class KeunoBot():

    def __init__(self):

        self.config_file = open("config.json", "r")
        self.config_content = self.config_file.read()
        self.obj = json.loads(self.config_content)
        self.token = self.obj['token']
        self.prefix = self.obj['prefix']

        self.client = commands.Bot(command_prefix=self.prefix, self_bot= True)
        self.client.remove_command('help')
        self.headers = {'authorization': self.token}
        self.antiGhostPing = False
        self.help = f"""```md
╦╔═╔═╗╦ ╦╔╗╔╔═╗╔╗ ╔═╗╔╦╗
╠╩╗║╣ ║ ║║║║║ ║╠╩╗║ ║ ║ 
╩ ╩╚═╝╚═╝╝╚╝╚═╝╚═╝╚═╝ ╩
[$>help](send this message)

- {self.prefix}ping => calculate self-bot ping
- {self.prefix}dmfriends <message> => Dm all friends list to send message
- {self.prefix}cleardm => delete all Dm message
- {self.prefix}status <activity> => change account activity
- {self.prefix}squad Bravery/Brilliance/Balance => change account HypeSquad
- {self.prefix}lightmode => set discord light Theme
- {self.prefix}darkmode => set discord dark Theme
- {self.prefix}cleargroup => leave all Dms groups
- {self.prefix}antighost on/off => set Anti Ghost Ping Alert
- {self.prefix}clearserver => clear all of channels, server roles
```"""
        intents = discord.Intents.all()
        intents.members = True

        @self.client.event
        async def on_ready():
            print(" [\033[38;2;249;53;248mKeunobot\033[0m] @> Hey Im KeunoBot, Im linked with \033[38;2;0;255;0m{0.user}\033[0m".format(self.client))
            print(f" [\033[38;2;249;53;248mKeunobot\033[0m] @> Guilds : \033[38;2;249;53;248m{len(self.client.guilds)}\033[0m | type : \033[38;2;249;53;248m{self.prefix}help\033[0m ")


        @self.client.event
        async def on_message_delete(message):
            if self.antiGhostPing == True:
                if message.mentions or message.role_mentions or message.mention_everyone:
                    await message.channel.send(f"**GHOST PING ALERT**\nAuthor : `{message.author}`\nContent : {message.content}\nTime : `{time.ctime()}`")
            else:
                pass

        @self.client.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.MissingRequiredArgument):
                mess = f"```diff\n- Failed : give me argument```"
                await ctx.send(mess)

        @self.client.command()
        async def help(ctx):
            await ctx.message.delete()
            await ctx.send(self.help)

        @self.client.command()
        async def ping(ctx):
            await ctx.message.delete()
            time_1 = time.perf_counter()
            await ctx.trigger_typing()
            time_2 = time.perf_counter()
            ping = round((time_2-time_1)*1000)
            mess = f"```diff\n+ My ping is {ping} ms```"
            await ctx.send(mess)

        @self.client.command()
        async def dmfriends(ctx, *, arg):
            await ctx.message.delete()
            num = 0
            fail_num = 0
            for user in self.client.user.friends:
                num = num + 1
                try:
                    await user.send(arg)

                except:
                    fail_num = fail_num + 1
                print(f" [\033[38;2;249;53;248mDMFriends\033[0m] > Success = \033[38;2;0;255;0m{num}\033[0m / failed = \033[38;2;255;0;0m{fail_num}\033[0m", end='\r')
            print(' ')

        @self.client.command()
        async def status(ctx, *, arg):
            await ctx.message.delete()
            try:
                activity = discord.Game(name=arg, type=3)
                await self.client.change_presence(status=discord.Status.idle, activity=activity)
                mess = f"```diff\n+ Success Status changed in : {arg}```"
                
            except:
                mess = f"```diff\n- Failed to change in : {arg}```"

            await ctx.send(mess)
        
        @self.client.command()
        async def cleardm(ctx):
            await ctx.message.delete()
            num_dm = 0
            for channel in self.client.private_channels:
                if isinstance(channel, discord.DMChannel):
                    async for msg in channel.history(limit=9999):
                        try:
                            if msg.author == self.client.user:
                                await msg.delete()
                                num_dm = num_dm + 1
                                print(f" [\033[38;2;249;53;248mClearDms\033[0m] > Clear Messages = \033[38;2;0;255;0m{num_dm}\033[0m", end='\r')
                        except:
                             pass

            print(f" [\033[38;2;249;53;248mClearDms\033[0m] > \033[38;2;0;255;0m{num_dm}\033[0m messages cleared !")

        @self.client.command()
        async def cleargroup(ctx):
            await ctx.message.delete()
            num_grp = 0
            for channel in self.client.private_channels:
                if isinstance(channel, discord.GroupChannel):
                    try:
                        num_grp = num_grp + 1
                        await channel.leave()
                        print(f" [\033[38;2;249;53;248mClearGroups\033[0m] > Clear Groups = \033[38;2;0;255;0m{num_grp}\033[0m", end='\r')
                    except:
                        pass
            print(f" [\033[38;2;249;53;248mClearGroups\033[0m] > \033[38;2;0;255;0m{num_grp}\033[0m groups leaved !")
            
                        
        @self.client.command()
        async def squad(ctx, arg):
            await ctx.message.delete()
            try:
                if arg == "Bravery":
                    body = {'house_id': 1}
                elif arg == "Brilliance":
                    body = {'house_id': 2}
                elif arg == "Balance":
                    body = {'house_id': 3} 
                
                resp = requests.post('https://discord.com/api/v9/hypesquad/online', headers=self.headers, json=body)
                if resp.status_code == 429:
                    mess = f"```diff\n- cannot change hypesquad in {arg} [RateLimited]```"
                elif resp.status_code == 204:
                    mess = f"```diff\n+ Success : Hypesquad changed in {arg}```"
            except:
                mess = f"```diff\n- Failed to change hypesquad in {arg}```"

            await ctx.send(mess)

        @self.client.command()
        async def lightmode(ctx):
            await ctx.message.delete()
            theme = {'theme': 'light'}
            requests.patch("https://discord.com/api/v8/users/@me/settings", headers=self.headers, json=theme)

        @self.client.command()
        async def darkmode(ctx):
            await ctx.message.delete()
            theme = {'theme': 'dark'}
            requests.patch("https://discord.com/api/v8/users/@me/settings", headers=self.headers, json=theme)

        @self.client.command()
        async def antighost(ctx, arg):
            await ctx.message.delete()
            if arg == "on":
                self.antiGhostPing = True
                mess = f"```diff\n+ Anti GhostPing enabled !```"
                await ctx.send(mess)
            elif arg == "off":
                self.antiGhostPing = False
                mess = f"```diff\n+ Anti GhostPing disabled !```"
                await ctx.send(mess)


        @self.client.command()
        async def clearserver(ctx):
            await ctx.message.delete()
            num_channel = 0
            num_roles = 0
            for channel in ctx.guild.channels:
                try:
                    await channel.delete()
                    num_channel = num_channel + 1
                    print(f" [\033[38;2;249;53;248mClearServer\033[0m] > Deleting = \033[38;2;0;255;0m{num_channel}\033[0m", end='\r')
                except:
                    pass
            for role in ctx.guild.roles:
                try:
                    await role.delete()
                    num_roles = num_roles + 1
                    print(f" [\033[38;2;249;53;248mClearServer\033[0m] > Deleting = \033[38;2;0;255;0m{num_roles}\033[0m", end='\r')
                except:
                    pass

            print(f" [\033[38;2;249;53;248mClearServer\033[0m] > \033[38;2;0;255;0m{num_channel}\033[0m channels and \033[38;2;0;255;0m{num_roles}\033[0m roles deleted !")

    def print_brand(self):
        brand = f'''
   ╦╔═╔═╗╦ ╦╔╗╔╔═╗╔╗ ╔═╗╔╦╗
  ╠╩╗║╣ ║ ║║║║║ ║╠╩╗║ ║ ║ 
  ╩ ╩╚═╝╚═╝╝╚╝╚═╝╚═╝╚═╝ ╩ 
   '''
        os.system('mode 100,30')
        os.system('cls')
        print('   ')
        print(Fade.Horizontal(Colors.blue_to_purple, brand))   


    def connect(self):
        self.client.run(self.token, bot= False)


self_bot = KeunoBot()
self_bot.print_brand()
self_bot.connect()

