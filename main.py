import discord
import dotenv
import os
import typing
import json

dotenv.load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
EMBED_COLOR = int(os.getenv('EMBED_COLOR'), base=16)  # 0xffc0cb

intents = discord.Intents.default() + discord.Intents.message_content + discord.Intents.messages
no_mentions = discord.AllowedMentions.none()
admin_permissions = discord.Permissions.none() + discord.Permissions.administrator

bot = discord.Bot(intents=intents)

info = {'log': 0, 'source': []}


def save_data():
    with open('data.json', 'w') as f:
        json.dump(info, f, indent=4)


def get_data():
    global info
    try:
        with open('data.json', 'r') as f:
            value = json.load(f)
            if value:
                info = value
    except json.decoder.JSONDecodeError:
        print('[ERROR] JSONDecodeError: file data is too short or file is empty')
    except FileNotFoundError:
        print('[ERROR] FileNotFoundError: no data.json')


@bot.event
async def on_ready():
    print(f"[INFO ]We have logged in as {bot.user}")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if isinstance(message.channel, discord.Thread):
        channel_id = message.channel.parent.id
    else:
        channel_id = message.channel.id
    if channel_id not in info['source']:
        return
    visit_url = message.jump_url
    for attachment in message.attachments:
        if attachment.content_type.startswith('image'):
            image_url = attachment.url
            break
    else:
        return
    channel_id = info['log']
    if channel_id == 0:
        print(['[WARNING] No alert channel set, skipping an artwork that should have an alert'])
    channel = await bot.fetch_channel(channel_id)
    embed = discord.Embed(title='New art has been posted ', color=EMBED_COLOR,
                          description=f"{message.author.mention} in {visit_url}")
    embed.set_thumbnail(url=image_url)
    await channel.send(embed=embed, view=LinkView(visit_url), allowed_mentions=no_mentions)


class LinkView(discord.ui.View):
    def __init__(self, url: str):
        super().__init__(timeout=None)
        button = discord.ui.Button(label="Visit", style=discord.ButtonStyle.link, url=url)
        self.add_item(button)


@bot.slash_command()
async def hello(ctx):
    await ctx.respond("Hello!")
    await bot.sync_commands(bot.commands)


@bot.slash_command(description="Set the alerts channel (only one, previous will be replaced)",
                   default_member_permissions=admin_permissions)
@discord.option(name='channel', description='Channel to send alerts')
async def setlogchannel(ctx: discord.ApplicationContext,
                        channel: discord.TextChannel):
    channel_id = channel.id
    info['log'] = channel_id
    save_data()
    await ctx.respond(f'{channel.mention} was set as alert channel')


@bot.slash_command(description="Set a source channel (one of multiple, enable/disable)",
                   default_member_permissions=admin_permissions)
@discord.option(name='channel', description='Channel to get posts', input_type=discord.TextChannel)
async def setsourcechannel(ctx: discord.ApplicationContext,
                           channel: typing.Union[discord.TextChannel, discord.ForumChannel],
                           mode: discord.Option(description='New mode of the channel', choices=['enabled', 'disabled'])
                           ):
    channel_id = channel.id
    b = (mode == 'enabled')
    if b:
        if channel_id in info['source']:
            await ctx.respond(f'Notifying about new artworks in {channel.mention} is already enabled')
        else:
            await ctx.respond(f'Notifying about new artworks in {channel.mention} was enabled')
            info['source'].append(channel_id)
            save_data()
    else:
        if channel_id not in info['source']:
            await ctx.respond(f'Notifying about new artworks in {channel.mention} is already disabled')
        else:
            await ctx.respond(f'Notifying about new artworks in {channel.mention} was disabled')
            info['source'].remove(channel_id)
            save_data()


@bot.slash_command(description="List chosen channels", default_member_permissions=admin_permissions)
async def listchannels(ctx: discord.ApplicationContext):
    alert_channel_id = info['log']
    if alert_channel_id != 0:
        alert_channel = await bot.fetch_channel(alert_channel_id)
        alert = alert_channel.mention
    else:
        alert = '*No alert channel set yet. Use `/setlogchannel` to fix that*'
    source_channels = [(await bot.fetch_channel(i)).mention for i in info['source']]
    if len(source_channels) == 0:
        source = '*No source channels set yet. Use `/setsourcechannel` to fix that*'
    else:
        source = ', '.join(source_channels)
    text = f"## Alert channel: \n{alert}\n\n## Source channels: \n{source}"
    await ctx.respond(text)

get_data()
bot.run(DISCORD_TOKEN)

