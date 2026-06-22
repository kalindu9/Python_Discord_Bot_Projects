import discord
from discord.ext import commands
from discord.ui import View, Button, Select
import discord
import json
from discord.ext import commands
from discord.ext import tasks

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

STAFF_ROLE_ID =11111222222   # 👈 CHANGE THIS ENTER YOUER ROLE ID
LOG_CHANNEL_NAME = "ticket-logs" # ENTER YOUER CHANNLE NAME

# ---------- CATEGORY SELECT ----------
class TicketSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Technical Issues", emoji="🛠️"),
            discord.SelectOption(label="V2ray Issues", emoji="⚠️"),
        ]
        super().__init__(placeholder="Select ticket category...", options=options)

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        staff_role = guild.get_role(STAFF_ROLE_ID)

        channel_name = f"ticket-{user.name}"

        # Already ticket check
        if discord.utils.get(guild.channels, name=channel_name):
            await interaction.response.send_message("❌ You already have a ticket!", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            staff_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True),
        }

        channel = await guild.create_text_channel(
            name=channel_name,
            overwrites=overwrites
        )

        embed = discord.Embed(
            title="🎫 Ticket Opened",
            description=f"**Category:** {self.values[0]}\nStaff will assist you shortly.",
            color=discord.Color.green()
        )

        await channel.send(
            content=f"{user.mention} ||<@&{STAFF_ROLE_ID}>||",
            embed=embed,
            view=CloseView()
        )

        await interaction.response.send_message(f"✅ Ticket created: {channel.mention}", ephemeral=True)


# ---------- CLOSE BUTTON ----------
class CloseButton(Button):
    def __init__(self):
        super().__init__(label="Close Ticket", style=discord.ButtonStyle.danger, emoji="❌")

    async def callback(self, interaction: discord.Interaction):
        # STAFF ONLY CHECK
        if STAFF_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("❌ Only staff can close tickets!", ephemeral=True)
            return

        channel = interaction.channel
        guild = interaction.guild

        log_channel = discord.utils.get(guild.channels, name=LOG_CHANNEL_NAME)

        if log_channel:
            await log_channel.send(f"📁 Ticket closed: {channel.name} by {interaction.user}")

        await interaction.response.send_message("Closing ticket...", ephemeral=True)
        await channel.delete()


class CloseView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CloseButton())


# ---------- MAIN PANEL ----------
class TicketPanel(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.primary, emoji="📩")
    async def create_ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            "📂 Select ticket category:",
            view=CategoryView(),
            ephemeral=True
        )


class CategoryView(View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(TicketSelect())


# ---------- COMMAND ----------
@bot.command()
async def ticket(ctx):
    embed = discord.Embed(
        title="🎫 Ceylon Lk Hosting Support Tickets",
        description=(
            "Create Ticket For Contact Staff Support\n\n"
            "📌 Click the **Create Ticket** button below\n"
            "📂 Select your ticket category\n"
            "🔒 Private channel will be created\n"
            "👮 Only you & staff can see it\n\n"
            "**📂 Ticket Categories**\n"
            "🛠️ Technical Issues - Bugs & problems\n"
            "🌐 V2ray Issues - Not Working V2ry & Ping Issues "
        ),
        color=discord.Color.blue()
    )

    await ctx.send(embed=embed, view=TicketPanel())


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run("YOUR_BOT_TOKEN")