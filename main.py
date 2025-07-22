# OpenWolf Bot
# =============
# Made by b1twalker
# OpenWolf Bot is a open-source multifunctional Discord bot designed to provide various features and functionalities for Discord servers.


# Global and other variables
global timesrestarted
version = '0.1'
whenlocked = {} # refer to /unlockdown command

# Formatting things
# - Colors
class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
# - Logger message types
infomsg = '[OpenWolf/Info] '
warnmsg = '\033[93m[OpenWolf/Warning] '
errmsg = '\033[91m[OpenWolf/Error] '
fatalmsg = '\033[91m[OpenWolf/Fatal] '
debugmsg = '[OpenWolf/Debug] '
# Formatting things

# Loading all default Python libs
try:
    import sys
    import datetime
    from datetime import timedelta
    import time
    import subprocess
    import asyncio
    import json
    from time import sleep
    import configparser
    import os
except ModuleNotFoundError:
    print(f"{errmsg} Something went wrong with Python standard library imports.")
    print(f"{errmsg} Is your Python installation corrupted?")
    exit(1)



# Some important functions
def KInterruptExit(): # Grace exit on KeyboardInterrupt (currently doesn't work)
    print(f"{infomsg}OpenWolf is shutting down..." + bcolors.ENDC)
    try:
        asyncio.run(bot.close())
    except Exception:
        pass
    exit(0)

def debug_print(msg): # Displays debug messages when loglevel is set to debug
    if logdebug == True:
        print(f"{debugmsg}{msg}")

def load_locale(lang_code): # Loading locale file
    try:
        locales_dir = os.path.join(os.path.dirname(__file__), 'locales')
        locale_path = os.path.join(locales_dir, f'{lang_code}.json')
        english_fallback = os.path.join(locales_dir, 'en_US.json')
        with open(locale_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f'{errmsg}Locale file for {lang_code} not found. Falling back to English.' + bcolors.ENDC)
        with open(english_fallback, 'r', encoding='utf-8') as f:
            return json.load(f)
        
def tlang(key, **kwargs): # Getting localized string from locale file
    if key not in LOCALE:
        debug_print(f"Locale key '{key}' not found, falling back to key name.")
    text = LOCALE.get(key, key)
    return text.format(**kwargs)

# Config file location
config_dir = os.path.join(os.path.dirname(__file__), 'config')
os.makedirs(config_dir, exist_ok=True)
config_path = os.path.join(config_dir, 'openwolf.ini')
class config(): # Config and things
    def create():
        config = configparser.ConfigParser()
    
        # Add sections and key-value pairs
        config['General'] = {'cfgversion': '1', 'log_level': 'info', 'token': '', 'custom_statuses': False, 'asciilogo': True}
        config['Commands'] = {'language': '', 'require_reason': True}
        config['Other'] = {'debug': False, 'skipdisclaimer': False}
    
        # Write the configuration to a file
        with open(config_path, 'w') as configfile:
            config.write(configfile)


    def read():
        # Create a ConfigParser object
        config = configparser.ConfigParser()
    
        # Read the configuration file
        config.read(config_path)
    
        # Access values from the configuration file 
        cfgversion = config.get('General', 'cfgversion')
        log_level = config.get('General', 'log_level')
        token = config.get('General', 'token')
        custom_statuses = config.getboolean('General', 'custom_statuses')
        asciilogo = config.getboolean('General', 'asciilogo')
        language = config.get('Commands', 'language')
        require_reason = config.getboolean('Commands', 'require_reason')
        debug_mode = config.getboolean('Other', 'debug')
        skipdisclaimer = config.getboolean('Other', 'skipdisclaimer')
    
        # Return a dictionary with the retrieved values
        config_values = {
            'cfgversion': cfgversion,
            'log_level': log_level,
            'token': token,
            'custom_statuses': custom_statuses,
            'asciilogo': asciilogo,
            'language': language,
            'require_reason': require_reason,
            'debug_mode': debug_mode,
            'skipdisclaimer': skipdisclaimer
        }
    
        return config_values

try: # Loading config
    print('[OpenWolf/Bootstrap] Reading config...')
    config_data = config.read()
except configparser.NoSectionError: # Config doesn't exist, running first-time setup
    print(f'[OpenWolf/Bootstrap] Failed to read config. Using a default one')
    config.create()
    # First-time setup: Step 1
    print(f"Hello there, welcome to OpenWolf, open-source Discord Bot!")
    print(f"It seems that you are running OpenWolf for the first time.")
    print(f"Don't worry! I'll guide you through the setup process.")
    while True:
        setup_step1 = input(f"First of all, did you already set up bot in Discord Developer Portal? (yes/no): ").strip().lower()
        if setup_step1.startswith('y'):
            break
        elif setup_step1.startswith('n'):
            print(f"Please set up your bot in Discord Developer Portal first. You can find the instructions here: https://discordpy.readthedocs.io/en/stable/discord.html")
            exit(1)
        else:
            print(f"Invalid input. Please enter 'yes' or 'no'.")
    # Step 2: Bot token input
    import getpass
    print("")
    print(f"Great! Please enter your bot token in the field below.")
    print(f"Your bot token is a password to your bot. Do not share it with anyone.")
    print(f"The field will not show your token.")
    token = getpass.getpass(f"Bot token: ").strip()
    while True:
        if token == '':
            print(f"Bot token cannot be empty. Please try again.")
            token = getpass.getpass(f"Bot token: ").strip()
        else:
            break
    config = configparser.ConfigParser()
    config.read(config_path)
    config['General']['token'] = token
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    # Step 3: Language selection
    print("")
    print(f"Please select your preferred language for the bot.")
    print(f"You can list available languages by typing 'list'.")
    print(f"Leave the box empty for default (English (United States))")
    print(f"Also, you can change it later in the config file.")
    while True:
        locales_dir = os.path.join(os.path.dirname(__file__), 'locales')
        locale_files = [f for f in os.listdir(locales_dir) if f.endswith('.json')]
        locale_codes = [os.path.splitext(f)[0] for f in locale_files]
        input_lang = input(f"Language: ").strip()
        if input_lang.lower() == 'list': # List locale files in locales/ directory
            print("Available languages:")
            print(", ".join(locale_codes))
            input_lang = input("Language: ").strip()
        if input_lang in locale_codes: # Set language and write to config
            config = configparser.ConfigParser()
            config.read(config_path)
            config['General']['language'] = input_lang
            with open(config_path, 'w') as configfile:
                config.write(configfile)
            LANG = input_lang
            LOCALE = load_locale(LANG)
            print(tlang('language_set'))
            break
        if input_lang.lower() == '': # Box empty, defaulting to English (United States)
            print(f"Defaulting to English (United States).")
            config = configparser.ConfigParser()
            config.read(config_path)
            config['General']['language'] = 'en_US'
            with open(config_path, 'w') as configgile:
                config.write(config_path)
            LANG = 'en_US'
            LOCALE = load_locale(LANG)
            print(tlang('language_set'))
        else: # Invalid input or locale file doesn't exist
            print(f"Language '{input_lang}' not found. Please enter a valid language code.")
    # Done!
    try:
        print(f"")
        print(f"Congratulations! You have successfully set up OpenWolf.")
        print(f"Now you can run the bot by executing the main.py file.")
        print(f"Thank you for trying out OpenWolf!")
        print(f"– The OpenWolf Team")
        print(f"")
        sleep(2)
        exit(0)
    except KeyboardInterrupt: # Exit immediately
        exit(0)
except configparser.NoOptionError:
    print(bcolors.FAIL + 'It seems you updated OpenWolf, and config is outdated.')
    print('Please copy your token from openwolf.ini, then remove it and reconfigure OpenWolf.')
    print('Automatic config update will be implemented in future versions. Sorry for inconvenience' + bcolors.ENDC)
    exit(0)

loglevel = config_data['log_level'] # get loglevel
if loglevel == 'debug': # loglevel is set to debug, enable debug messages
    logdebug = True
elif config_data['debug_mode'] == True: # Debug mode is enabled, enable debug messages
    logdebug = True
else: # loglevel is not debug nor debug mode is enabled, debug messages disabled
    logdebug = False

debug_print('Importing discord') # Try to import discord
try:
    import audioop
except ModuleNotFoundError:
    print(f"{errmsg}Module audioop-lts is not installed.")
    print(f"{errmsg}Since audioop got deprecated in Python 3.13, and discord.py depends on it, you need")
    print(f"{errmsg}to install 'audioop-lts' package.")
try:
    import discord
    from discord.ext import commands
except ModuleNotFoundError:
    print(f"{errmsg}Discord.py is not installed. Please install it and try again.")
    print(f"{errmsg}You can install it using pip: pip install -U discord.py")
    print(f"{errmsg}Pro tip: if you get 'externally-managed-environment' error while installing discord.py,")
    print(f"{errmsg}try to install it in virtual environment.")
    print(f"{errmsg}More info: https://docs.python.org/3/library/venv.html")
    exit(1)
start_time = time.time()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=">",intents=intents)

debug = config_data['debug_mode']
loglevel = config_data['log_level']
LANG = config_data['language']
if LANG == '':
    print(f"Welcome to OpenWolf! It seems that you haven't set a language in the config file.")
    print(f"Please enter your preferred language code. It will be saved in the config file.")
    print(f"To list available languages, type 'list'")
    while True:
        locales_dir = os.path.join(os.path.dirname(__file__), 'locales')
        locale_files = [f for f in os.listdir(locales_dir) if f.endswith('.json')]
        locale_codes = [os.path.splitext(f)[0] for f in locale_files]
        input_lang = input(f"Language: ").strip()
        if input_lang.lower() == 'list':
            print("Available languages:")
            print(", ".join(locale_codes))
            input_lang = input("Language: ").strip()
        if input_lang in locale_codes:
            config = configparser.ConfigParser()
            config.read(config_path)
            config['Commands']['language'] = input_lang
            with open(config_path, 'w') as configfile:
                config.write(configfile)
            LANG = input_lang
            LOCALE = load_locale(LANG)
            print(f"{tlang('language_set')}")
            break
        else:
            print(f"Language '{input_lang}' not found. Please enter a valid language code.")
LOCALE = load_locale(LANG)

# Get list of users that can use debug messages
debug_access_path = os.path.join(os.path.dirname(__name__), "config", "debug_access.json")
while True:
    try:
        with open(debug_access_path, 'r') as f:
            debug_access = json.load(f)
            break
    except FileNotFoundError:
        with open(debug_access_path, 'w') as f:
            f.write("[]")
            f.close()
    except Exception as e:
        debug_print(f"Something happened when tried to get list of users with debug access: {f}")
        pass
        break

# Custom animated status (requires custom_statuses to be enabled in config)
async def animated_status():
    with open(os.path.join(os.path.dirname(__file__), "config", "statuses.json"), "r", encoding="utf-8") as f:
        status_strings = json.load(f)
    statuses = [discord.Game(s.format(version=version)) for s in status_strings]
    while True:
        for status in statuses:
            await bot.change_presence(activity=status)
            await asyncio.sleep(10)

print('[OpenWolf/Bootstrap] Token set succesfully. Logging in')

if debug == False:
    debug_print(tlang('debugmessages_debug_disabled'))

timesrestarted = 0
@bot.event
async def on_ready():
    global timesrestarted
    debug_print(tlang('debugmessages_slashcommands_syncing'))
    print('[OpenWolf/Bootstrap] ', tlang('bootstrap_ready'))
    await bot.tree.sync()
    if config_data['custom_statuses'] == True:
        bot.loop.create_task(animated_status())
    else:
        await bot.change_presence(activity=discord.Game(f"🐺 OpenWolf v{version}"))
    end_time = time.time()
    total_time_raw = end_time - start_time
    total_time = f"{total_time_raw:.2f}"
    # Animated ASCII art logo (line-by-line animation)
    ascii_logo = [
        "                          ██                               ",
        "                          ████                             ",
        "                    ███   ██████                           ",
        "                     ███████  ████                         ",
        "                      ██████   ████    ██                  ",
        "                      ██        ████     ███               ",
        "                     ███         ███       ███             ",
        "                   ████           ███  █     ███           ",
        "                  ███             ███  ██     ███          ",
        "                  ███ ███          ██   █     ████         ",
        "                  ███ ██           ██   ██     ███         ",
        "                ███████████        ██   ███     ███        | You are running OpenWolf!",
        "             ████                 ███     █  █  ██         | Your open-source Discord assistant",
        "          ████             █      ██      █  ██ ██         | Version {version}",
        "         █████             ██    ███    █    █████         ",
        "           ███      █████  ██   ███     ██   ████          ",
        "            █████████   ████  ████      ███ ██ ██          ",
        "                          ██ ████       █████  ██          ",
        "                           ████        █████  ██           ",
        "                          ███         █████   █            ",
        "                         ███         ████     █            ",
        "                        ███        ████                    ",
        "                        ██       ████                      ",
        "                       ██      ███                         ",
        "                      ██     ██                            ",
        "                      █      █                             ",
        "                            █                              ",
        "                                                            "
    ]

    if timesrestarted == 0:
        timesrestarted += 1
        if config_data['asciilogo'] == False:
            print(f'{infomsg}You are running OpenWolf!')
            print(f'{infomsg}Your open-source Discord assistant')
            print(f'{infomsg}Version {version}')
        else:
            sys.stdout.write('\033[2J\033[H')  # Clear screen and move cursor to top
            for idx, line in enumerate(ascii_logo):
                print(line.format(version=version))
                sys.stdout.flush()
                time.sleep(0.03)
        print(infomsg + tlang('bot_ready', total_time=total_time))
        if LANG != 'en_US':
            print(f"{infomsg}Selected language: {tlang('language')}")
        print(infomsg + tlang('selected_language') + tlang('language_original'))
        print(infomsg + tlang('logged_in', bot_name=bot.user.name, bot_discriminator=bot.user.discriminator, bot_id=bot.user.id))
    else:
        print(infomsg + tlang('ascii_skipped'))
        print(f'{infomsg}You are running OpenWolf!')
        print(f'{infomsg}Your open-source Discord assistant')
        print(f"Version {version}")
        print(infomsg + tlang('reconnected'))
        print(infomsg + tlang('logged_in', bot_name=bot.user.name, bot_discriminator=bot.user.discriminator, bot_id=bot.user.id))

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(tlang('on_guild_join'))
        break

# Debug commands (work only with debug enabled in config)
if debug == True:
    @bot.tree.command(name="hello", description=tlang('command_description_hello')) # Instance info
    async def hello(interaction: discord.Interaction):
        if interaction.user.name in debug_access: # If user has debug access, they can request instance info
            await interaction.response.send_message(tlang('hello_debug'))
            uname_smo = subprocess.Popen(["uname -smo"], stdout=subprocess.PIPE, shell=True, text=True)
            (out, err) = uname_smo.communicate()
            out1 = out
            err1 = err
            uname_n = subprocess.Popen(["uname -n"], stdout=subprocess.PIPE, shell=True, text=True)
            (out, err) = uname_n.communicate()
            hostname = out
            hosterror = err
            fastfetch = subprocess.Popen(["fastfetch -l none -s \"Host:OS:Kernel:Uptime:Memory:Swap\" --pipe"], stdout=subprocess.PIPE, shell=True, text=True)
            (out, err) = fastfetch.communicate()
            fastfetch_out = out
            fastfetch_err = err
            embed = discord.Embed(
                title=f":wolf:  OpenWolf v{version} — {tlang('hello_instance_info')}",
                description=f"{fastfetch_out}"
                f"Ping: {round(bot.latency * 1000)} мс\n",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.now()
            )
            await interaction.followup.send(embed=embed)
            debug_print(tlang('debugmessages_hello', user_name=interaction.user.name, user_id=interaction.user.id))
        else: # If not, bot will just greet them
            await interaction.response.send_message(tlang('hello'))
        return
    @bot.tree.command(name="restartbot", description=tlang('command_description_restartbot')) # Restart bot within Discord
    async def restartbot(interaction:discord.Interaction):
        view = ConfirmView(interaction.user)
        if interaction.user.name in debug_access: # If user has debug access, bot will restart
            await interaction.response.send_message(embed=discord.Embed(
                title=tlang('generic_danger'),
                description=tlang('restartbot_holdon_message'),
                color=discord.Color.orange()
            ), ephemeral=True, view=view)
            restartmessage = await interaction.original_response()
            await view.wait()
            if view.value:
                await restartmessage.edit(embed=discord.Embed(
                    title=":white_check_mark: " + tlang('restartbot_success'),
                    color=discord.Color.green()), view=None)
                debug_print(tlang('debugmessages_restartbot', user_name=interaction.user.name, user_id=interaction.user.id))
                os.execv(sys.executable, ['python'] + sys.argv)
                await bot.close()
            else:
                await restartmessage.edit(embed=discord.Embed(
                    title=":white_check_mark: " + tlang('restartbot_cancelled'),
                    color=discord.Color.green()), view=None)
        else:
            await interaction.response.send_message(embed=discord.Embed(
                title=f":white_check_mark: {tlang('restartbot_nopermission_title')}",
                description=tlang('restartbot_nopermission_description'),
            ), ephemeral=True)
            debug_print(tlang('debugmessages_restartbot_nopermission', user_name=interaction.user.name, user_id=interaction.user.id))
    @bot.tree.command(name="ping",description=tlang('command_description_ping'))
    async def ping(interaction:discord.Interaction):
        await interaction.response.send_message(tlang('ping_pong') + f" ({bot.latency*1000:.2f}ms)")

@bot.tree.command(name="changelog", description=tlang('command_description_changelog'))
async def changelog(interaction: discord.Interaction):
    embed = discord.Embed(
        title="OpenWolf Bot — Changelog",
        description=(
            f"Finally open-source!!"
        ),
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="fixmsg", description=tlang('command_description_fixmsg')) # Fix user's message if they wrote it in wrong keyboard layout
async def blya(interaction: discord.Interaction):
    messages = [message async for message in interaction.channel.history(limit=2)]
    x = str(messages[1].content)
    a = {'Q':'Й','W':'Ц','E':'У','R':'К','T':'Е','Y':'Н','U':'Г','I':'Ш','O':'Щ','P':'З','{':'Х','}':'Ї','A':'Ф','S':'І','D':'В','F':'А','G':'П','H':'Р','J':'О','K':'Л','L':'Д',':':'Ж','"':'Є','Z':'Я','X':'Ч','C':'С','V':'М','B':'И','N':'Т','M':'Ь','<':'Б','>':'Ю','~':"'",'q':'й','w':'ц','e':'у','r':'к','t':'е','y':'н','u':'г','i':'ш','o':'щ','p':'з','[':'х',']':'ї','a':'ф','s':'і','d':'в','f':'а','g':'п','h':'р','j':'о','k':'л','l':'д',';':'ж',"'":'є','z':'я','x':'ч','c':'с','v':'м','b':'и','n':'т','m':'ь',',':'б','.':'ю','`':"'",' ':' ','&':'?',"-":"-","'":'`','Й':'Q','Ц':'W','У':'E','К':'R','Е':'T','Н':'Y','Г':'U','Ш':'I','Щ':'O','З':'P','Х':'{','Ї':'}','Ф':'A','І':'S','В':'D','А':'F','П':'G','Р':'H','О':'J','Л':'K','Д':'L','Ж':':','Э':'"','Я':'Z','Ч':'X','С':'C','М':'V','И':'B','Т':'N','Ь':'M','Б':'<','Ю':'>','Ё':'~','й':'q','ц':'w','у':'e','к':'r','е':'t','н':'y','г':'u','ш':'i','щ':'o','з':'p','х':'[','ї':']','ф':'a','і':'s','в':'d','а':'f','п':'g','р':'h','о':'j','л':'k','д':'l','ж':';','э':"'",'я':'z','ч':'x','с':'c','м':'v','и':'b','т':'n','ь':'m','б':',','ю':'.','Ы':'S','Ъ':'}','ы':'s','ъ':']','Є':'"','є':'"','Ё':'~','ё':'`'}
    res = ''
    j = 0
    while j < len(x):
       if x[j] in a:
           i = a[x[j]]
           res += i
           j+=1
    debug_print(tlang('debugmessages_fixmsg', user_name=interaction.user.name, user_id=interaction.user.id))
    await interaction.response.send_message(str(messages[1].author.mention) + tlang('user_wanted_to_say') + res)

# Moderation commands
@bot.tree.command(name="ban",description=tlang('command_description_ban'))
async def ban(interaction:discord.Interaction, member:discord.Member, reason:str = None):
    if interaction.user.guild_permissions.ban_members: # Check if user have permissions
        notnotified = False # This variable is used to notify users about ban in DMs (False if notified, True if not)
        userembed = discord.Embed(
            title=f":octagonal_sign:  " + tlang('ban_userembed_title') + interaction.guild.name,
            description=tlang('ban_userembed_description'),
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        ) # Embed that user gets when banned
        if reason == None:
            userembed.add_field(name=tlang('punish_reason'), value=tlang('punish_reason_default'))
        else:
            userembed.add_field(name=tlang('punish_reason'), value=reason)
        userembed.add_field(name=tlang('ban_serverembed_bannedby'), value=interaction.user.name)
        userembed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)
        userembed.set_footer(text=tlang('generic_requestedby') + interaction.user.name + " | OpenWolf", icon_url=interaction.user.avatar.url)
        serverembed = discord.Embed(
            title=f":white_check_mark:  " + tlang('ban_serverembed_title') + f" {member.name}",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        serverembed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        serverembed.add_field(name=tlang('punish_reason'), value=reason if reason else tlang('punish_reason_default'))
        serverembed.add_field(name=tlang('ban_serverembed_bannedby'), value=interaction.user.name)
        if notnotified:
            serverembed.add_field(name=tlang('punish_usernotnotified_title'), value=tlang('punish_usernotnotified_description'))
        if config_data['require_reason'] == True and reason == None:
            await interaction.response.send_message(embed=discord.Embed(
                title=":x: " + tlang('punish_reason_required'),
                color=discord.Color.red()
            ), ephemeral=True)
        else:
            try:
                await member.send(embed=userembed)
            except discord.Forbidden:
                notnotified = True # User has DMs disabled, user not notified
                pass
            await member.ban()
            await interaction.response.send_message(embed=serverembed)
            debug_print(tlang('debugmessages_ban', user_name=interaction.user.name, user_id=interaction.user.id, target_name=member.name, target_id=member.id, guild_name=interaction.guild.name, guild_id=interaction.guild.id))
    else:
        await interaction.response.send_message(embed=discord.Embed(title=tlang('generic_insufficient_permissions'), color=discord.Color.red()), ephemeral=True)

@bot.tree.command(name="kick",description=tlang('command_description_kick'))
async def kick(interaction:discord.Interaction, member:discord.Member, reason:str = None):
    if interaction.user.guild_permissions.kick_members:
        notnotified = False
        userembed = discord.Embed(
            title=f":warning:  " + tlang('kick_userembed_title') + " " + f"{interaction.guild.name}",
            description=tlang('kick_userembed_description'),
            color=discord.Color.yellow(),
            timestamp=datetime.datetime.now()
        )
        userembed.add_field(name=tlang('punish_reason'), value=reason if reason else tlang('punish_reason_default'))
        userembed.add_field(name=tlang('kick_serverembed_kickedby'), value=interaction.user.name)
        userembed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)
        userembed.set_footer(text=f"{tlang('generic_requestedby')}{interaction.user.name} | OpenWolf", icon_url=interaction.user.avatar.url)
        serverembed = discord.Embed(
            title=":white_check_mark:  " + tlang('kick_serverembed_title') + " " + member.name,
            color=discord.Color.green(),
            timestamp=datetime.datetime.now())
        serverembed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        serverembed.add_field(name=tlang('punish_reason'), value=reason if reason else tlang('punish_reason_default'))
        serverembed.add_field(name=tlang('kick_serverembed_kickedby'), value=interaction.user.name)
        if notnotified:
            serverembed.add_field(name=tlang('punish_usernotnotified_title'), value=tlang('punish_usernotnotigied_description'))
        if config_data['require_reason'] == True and reason == None:
            await interaction.response.send_message(embed=discord.Embed(
                title=":x: " + tlang('punish_reason_required'),
                color=discord.Color.red()
            ), ephemeral=True)
            try:
                await member.send(embed=userembed)
            except discord.Forbidden:
                notnotified = True
                pass
            await member.kick()
            await interaction.response.send_message(embed=kickembed)
        debug_print(tlang('debugmessages_kick', user_name=interaction.user.name, user_id=interaction.user.id, target_name=member.name, target_id=member.id, guild_name=interaction.guild.name, guild_id=interaction.guild.id))
    else:
        await interaction.response.send_message(embed=discord.Embed(title=tlang('generic_insufficient_permissions'), color=discord.Color.red()), ephemeral=True)

@bot.tree.command(name="timeout", description=tlang('command_description_timeout'))
async def timeout(interaction:discord.Interaction, member:discord.Member, duration:int, reason:str = None):
    if interaction.user.guild_permissions.manage_permissions:
        if reason == None:
            await member.timeout(timedelta(hours=duration), reason=tlang('punish_reason_default'))
        else:
            await member.timeout(timedelta(hours=duration), reason=reason)
        serverembed = discord.Embed(
            title=":white_check_mark: " + tlang('timeout_serverembed_title', target_name=member.name,
            color=discord.Colour(0x5865F2)))
        serverembed.add_field(name=tlang('timeout_serverembed_duration', value=str(duration) + 'hours'))
        serverembed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        await interaction.response.send_message(embed=serverembed)
        debug_print(tlang('debugmessages_timeout', user_name=interaction.user.name, user_id=interaction.user.id, target_name=member.name, target_id=member.id, guild_name=interaction.guild.name, guild_id=interaction.guild.id, duration=duration))
    else:
        await interaction.response.send_message(embed=discord.Embed(title=tlang('generic_insufficient_permissions'), color=discord.Color.red()), ephemeral=True)

class ConfirmView(discord.ui.View): # Confirmation buttons for dangerous commands
    def __init__(self, author):
        super().__init__(timeout=60)
        self.author = author
        self.value = None

    @discord.ui.button(label=tlang('ConfirmView_button_confirm'), style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.author:
            await interaction.response.send_message(f"{tlang('ConfirmView_notforyou')}", ephemeral=True)
            return
        self.value = True
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label=tlang('ConfirmView_button_cancel'), style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.author:
            await interaction.response.send_message(f"{tlang('ConfirmView_notforyou')}", ephemeral=True)
            return
        self.value = False
        self.stop()
        await interaction.response.defer()

@bot.tree.command(name="getchannelinfo", description=tlang('command_description_getchannelinfo'))
async def getchannelinfo(interaction:discord.Interaction, channel:discord.TextChannel):
    embed = discord.Embed(
        title=tlang('getchannelinfo_title') + channel.name,
        color=discord.Color.blue()
    )
    embed.add_field(name=tlang('getchannelinfo_id'), value=channel.id, inline=False)
    embed.add_field(
        name=tlang('getchannelinfo_created_at'),
        value=channel.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        inline=False
    )
    embed.add_field(name=tlang('getchannelinfo_type'), value=str(channel.type), inline=False)
    embed.add_field(
        name=tlang('getchannelinfo_member_count'),
        value=len(channel.members),
        inline=False
    )
    category_name = channel.category.name if channel.category else tlang('getchannelinfo_no_category')
    embed.add_field(name=tlang('getchannelinfo_category'), value=category_name, inline=False)
    await interaction.response.send_message(embed=embed)
@bot.tree.command(name="purgechannel", description=tlang('command_description_purgechannel')) # Delete and recreate channel to remove all channel history
async def purgechannel(interaction:discord.Interaction, channel:discord.TextChannel):
    if interaction.user.guild_permissions.manage_channels: # Check if user has permission to manage channels
        view = ConfirmView(interaction.user)
        await interaction.response.send_message(embed=discord.Embed(
            title=f":raised_hand:  " + tlang('purgechannel_holdon_title'),
            description=tlang('purgechannel_holdon_description', channel_name=channel.name),
            color=discord.Color.orange()),
            view=view,
            ephemeral=True)
        await view.wait()
        if view.value:
            try:
                new_channel_name = channel.name
                channel_category = channel.category
                await channel.delete()
                debug_print(tlang('debugmessages_purgechannel', user_name=interaction.user.name, user_id=interaction.user.id, channel_name=channel.name, channel_id=channel.id, guild_name=interaction.guild.name, guild_id=interaction.guild.id))
                new_channel = await interaction.guild.create_text_channel(name=new_channel_name, category=channel_category)
                new_channel_embed = discord.Embed(
                    title=":wastebasket:  " + tlang('purgechannel_success_title'),
                    description=tlang('purgechannel_success_description'),
                    color=discord.Color.green()
                )
                await new_channel.send(embed=new_channel_embed)
            except discord.Forbidden:
                await interaction.followup.send(tlang('purgechannel_exception_Forbidden'), ephemeral=True)
                debug_print(tlang('debugmessages_generic_cant_manage_channels', user_name=interaction.user.name, user_id=interaction.user.id, channel_name=channel.name, channel_id=channel.id, guild_name=interaction.guild.name, guild_id=interaction.guild.id))
            except discord.HTTPException as e:
                await interaction.followup.send(tlang('purgechannel_exception_HTTPException'), ephemeral=True)
                debug_print(tlang('debugmessages_purgechannel_HTTPException', user_name=interaction.user.name, user_id=interaction.user.id, channel_name=channel.name, channel_id=channel.id, guild_name=interaction.guild.name, guild_id=interaction.guild.id, error=e))
            except Exception as e:
                await interaction.followup.send(tlang('purgechannel_exception_generic', error=str(e)), ephemeral=True)
                debug_print(tlang('debugmessages_purgechannel_exception', user_name=interaction.user.name, user_id=interaction.user.id, channel_name=channel.name, channel_id=channel.id, guild_name=interaction.guild.name, guild_id=interaction.guild.id))
        else:
            await interaction.edit_original_response(embed=discord.Embed(
                title=tlang('generic_commandcancelled'),
                color=discord.Color.red()
                ), view=None)
    else:
        await interaction.response.send_message(embed=discord.Embed(title=tlang('generic_insufficient_permissions'), color=discord.Color.red()), ephemeral=True)
@bot.tree.command(name="lockdown", description=tlang('command_description_lockdown')) # Disallow users to send messages in specific channel (lock)
async def lockdown(interaction:discord.Interaction, channel:discord.TextChannel):
    if interaction.user.guild_permissions.manage_channels: # Check if user have permission to manage channels
        view = ConfirmView(interaction.user)
        await interaction.response.send_message(tlang('lockdown_holdon_message', channel_name=channel.name), view=view, ephemeral=True) # Warning before locking channel
        await view.wait()
        if view.value:
            try:
                await channel.set_permissions(interaction.guild.default_role, send_messages=False) # Channel locked. Can be unlocked after 30 seconds
                lockedembed = discord.Embed(
                    title=f":lock: {tlang('lockdown_success_title')}",
                    description=tlang('lockdown_success_description', interaction_user_mention=interaction.user.mention),
                    color=discord.Color.red()
                )
                await interaction.followup.send(f":lock: {tlang('lockdown_admin_success', channel_name=channel.name)}", ephemeral=True)
                whenlocked[channel.id] = int(datetime.datetime.now().timestamp())
                await channel.send(embed=lockedembed)
                debug_print(tlang('debugmessages_lockdown', user_name=interaction.user.name, user_id=interaction.user.id, channel_name=channel.name, channel_id=channel.id, guild_name=interaction.guild.name, guild_id=interaction.guild.id))
            except discord.Forbidden:
                await interaction.followup.send(tlang('lockdown_exception_Forbidden'), ephemeral=True)
                debug_print(tlang('debugmessages_generic_cant_manage_channels', user_name=interaction.user.name, user_id=interaction.user.id, channel_name=channel.name, channel_id=channel.id, guild_name=interaction.guild.name, guild_id=interaction.guild.id))
            except discord.HTTPException as e:
                await interaction.followup.send(tlang('lockdown_exception_HTTPException'), ephemeral=True)
                debug_print(tlang('debugmessages_lockdown_HTTPException', user_name=interaction.user.name, user_id=interaction.user.id, channel_name=channel.name, channel_id=channel.id, guild_name=interaction.guild.name, guild_id=interaction.guild.id, error=e))
            except Exception as e:
                await interaction.followup.send(tlang('lockdown_exception_generic', error=str(e)), ephemeral=True)
                debug_print(tlang('debugmessages_lockdown_exception', user_name=interaction.user.name, user_id=interaction.user.id, channel_name=channel.name, channel_id=channel.id, guild_name=interaction.guild.name, guild_id=interaction.guild.id, error=e))
        else:
            await interaction.followup.send(tlang('generic_commandcancelled'), ephemeral=True)
    else:
        await interaction.response.send_message(embed=discord.Embed(title=tlang('generic_insufficient_permissions'), color=discord.Color.red()), ephemeral=True)

@bot.tree.command(name="unlockdown", description=tlang('command_description_unlockdown')) # Allow users to send messages in previously locked channel
async def unlockdown(interaction:discord.Interaction, channel:discord.TextChannel):
    if interaction.user.guild_permissions.manage_messages: # Check if user have permission to manage channels
        islocked = channel.permissions_for(interaction.guild.default_role).send_messages is False # Check if channel not locked
        if not islocked: # Check if channel locked
            await interaction.response.send_message(tlang('unlockdown_notlocked', channel_name=channel.name), ephemeral=True)
            return
        if channel.id in whenlocked: # Secondary check if channel is locked
            if int(datetime.datetime.now().timestamp()) - whenlocked[channel.id] < 30: # Check if channel was locked more than 30 seconds
                await interaction.response.send_message(tlang('unlockdown_unavailable', channel_name=channel.name), ephemeral=True)
                return
        try: # All check passed, unlock channel
            await channel.set_permissions(interaction.guild.default_role, send_messages=True)
            unlockedembed = discord.Embed(
                title=f":unlock: {tlang('unlockdown_success_title', channel_name=channel.name)}",
                description=tlang('unlockdown_success_description'),
                color=discord.Color.green()
            )
            await interaction.response.send_message(f":unlock: {tlang('unlockdown_admin_success', channel_name=channel.name)}", ephemeral=True)
            await channel.send(embed=unlockedembed)
            debug_print(tlang('debugmessages_unlockdown', user_name=interaction.user.name, user_id=interaction.user.id, channel_name=channel.name, channel_id=channel.id, guild_name=interaction.guild.name, guild_id=interaction.guild.id))
        except discord.Forbidden:
            await interaction.response.send_message(tlang('unlockdown_exception_Forbidden'), ephemeral=True)
            debug_print(tlang('debugmessages_generic_cant_manage_channels', user_name=interaction.user.name, user_id=interaction.user.id, channel_name=channel.name, channel_id=channel.id, guild_name=interaction.guild.name, guild_id=interaction.guild.id))
        except discord.HTTPException as e:
            await interaction.response.send_message(tlang('unlockdown_exception_HTTPException'), ephemeral=True)
            debug_print(tlang('debugmessages_lockdown_HTTPException', user_name=interaction.user.name, user_id=interaction.user.id, channel_name=channel.name, channel_id=channel.id, guild_name=interaction.guild.name, guild_id=interaction.guild.id, error=e))
        except Exception as e:
            await interaction.response.send_message(tlang('unlockdown_exception_generic', error=str(e)), ephemeral=True)
            debug_print(tlang('debugmessages_lockdown_exception', user_name=interaction.user.name, user_id=interaction.user.id, channel_name=channel.name, channel_id=channel.id, guild_name=interaction.guild.name, guild_id=interaction.guild.id, error=e))
    else:
        await interaction.response.send_message(embed=discord.Embed(title=tlang('generic_insufficient_permissions'), color=discord.Color.red()), ephemeral=True)
        

@bot.tree.command(name="clear", description=tlang('command_description_clear')) # Clear n-amount of messages
async def clear(interaction:discord.Interaction, count:int):
    if interaction.user.guild_permissions.manage_messages: # Check if user have permission to delete messages
        await interaction.response.defer(ephemeral=True)
        waiting = discord.Embed(
            title=f":broom:  {tlang('clear_title')}",
            description=f"{tlang('clear_wait_description', channel_name=interaction.channel.name)}",
            color=discord.Color.yellow()
        )
        await interaction.followup.send(embed=waiting, ephemeral=True)
        deleted = await interaction.channel.purge(limit=count)
        debug_print(f"Messages to delete: {len(deleted)}")
        done = discord.Embed(
            title=f":white_check_mark:  {tlang('clear_done_title')}",
            description=f"{tlang('clear_success_description')}" + " " + str(len(deleted)),
            color=discord.Color.green()
        )
        await interaction.edit_original_response(embed=done, view=None)
        debug_print(tlang('debugmessages_clear', user_name=interaction.user.name, user_id=interaction.user.id, guild_name=interaction.guild.name, guild_id=interaction.guild.id, channel_name=interaction.channel.name, channel_id=interaction.channel_id, len=str(len(deleted))))
    else:
        await interaction.response.send_message(tlang('clear_nopermission'), ephemeral=True)

try:
    token = config_data['token']
    bot.run(token, reconnect=True)
except discord.errors.LoginFailure:
    print(f"{fatalmsg}{tlang('login_failed')}" + bcolors.ENDC)
    print(f"{infomsg}{tlang('generic_exiting')}" + bcolors.ENDC)
    exit(1)
except KeyboardInterrupt:
    KInterruptExit()
    exit(0)

        