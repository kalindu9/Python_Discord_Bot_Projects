import discord
import json
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_member_join(member):
    role = member.guild.get_role(222222222)      #Chnage Your Member Role Id

    if role:
        await member.add_roles(role)
 

#Customize Your Welcome Message

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="Your Welcome Channel Name")

    embed = discord.Embed(
        title=f"Welcome {member.name}! 🎉",
        description=f"Hey {member.mention} 👑, welcome to **Your Saver Name** ❤️🔥",
        color=0x0D6EFD #Enter You Color Code 
    )

   

    file = discord.File("Your.gif", filename="Your.gif")
    embed.set_image(url="attachment://Your.gif")


    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)

    await channel.send(embed=embed, file=file)



    
    

bot.run("Your_Bot_Token") 