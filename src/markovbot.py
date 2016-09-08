import discord
import markovify
import asyncio

##########
# CONFIG #
##########

# Set this to the path where your .txts are. This should be a folder that contains .txt files with the name of the chain/command
textdir = "logs/"

# Dictonaries with the files and options
# Filename is the name of the file within the above directory
# Command is the argument used for calling this markov
# Username is the name of the user (for changing nicknames). If it is set to None, it will not change the nickname
# Avatar is the file name of the avatar for this user. If it is set to None, it will not change the avatar. It looks for the avatar in the same directory as the logs
# Newline set to False if you want it to seperate sentences based on periods instead of newlines
# Model shouldn't be touched
# Cache shouldn't be touched
config = [
  {
    'filename': 'text.txt',
    'command': 'test',
    'username': None,
    # Example to set the nickname:
    # 'username': 'Test User',
    'avatar': None,
    # Example to set the avatar:
    # 'avatar': 'test.png'
    'newline': True,
    'model': None,
    'cache': []
  }
 ]

# Default avatar name
defaultavatar = 'avatar.png'

# Bot token goes here
bottoken = "MTg3ODE4MDI4NjQwMTA4NTQ0.CrGbBQ.syQBhtEptt9mNSGcKG0O2a_sres"

# Set the commands to trigger a markov. The second one is optional
command = ".markov"
altcommand = ".mk"

################

def markov(model):
    m = None
    while m == None:
        m = model.make_sentence()
    return "\u200b"+m.encode("ascii","backslashreplace").decode("unicode-escape")

def markovcache():
    for c in config:
        while len(c['cache']) <= 10:
            print("Generating cache for {0}.".format(c['username']))
            m = markov(c['model'])
            c['cache'].append(m)

for c in config:
    with open(textdir+c['filename']) as t:
        text = t.read()

    if c['newline']:
        c['model'] = markovify.text.NewlineText(text)
    else:
        c['model'] = markovify.Text(text)

print("Generating markov phrases. If this takes too long, your source text may be too short.\n")
markovcache()


client = discord.Client()

async def sendmarkov(markov, message):
    if len(markov['cache']) == 0:
        markovcache()

    msg = c['cache'].pop()

    if message.channel.is_private:
        await client.send_message(message.channel, msg)
        print("PM with {0.author}\n{1}:{2}\n".format(message, markov['username'], msg[1:]))

    else:
        oldname = message.server.me.display_name

        if markov['username']:
            try:
               await client.change_nickname(message.server.me, markov['username'])
            except:
                print("Tried to change nickname on {0.server.name}, failed.".format(message))

        if markov['avatar']:
            try:
                with open(textdir+markov['avatar']) as a:
                    avvy = a.read()
                await client.change_profile(avatar=avvy)
            except:
                print("Tried to change avatar, failed.")

        await client.send_message(message.channel, msg)

        if markov['username']:
            try:
               await client.change_nickname(message.server.me, oldname)
            except:
                pass

        if markov['avatar']:
            try:
                with open(defaultavatar) as a:
                    avvy = a.read()
                await client.change_profile(avatar=avvy)
            except:
                pass

        print("{0.server.name}#{0.channel.name}\n{1}:{2}\n".format(message, markov['username'], msg[1:]))

    markovcache()

@client.event
async def on_ready():
    print('Logged in as:\n{0.name}, {0.id}\n'.format(client.user))
    with open(defaultavatar) as a:
        avvy = a.read()
    await client.change_profile(avatar=avvy)

@client.event
async def on_message(message):
    if message.author.bot or message.author == client.user:
        return

    if message.content.lower().split()[0] == command or message.content.lower().split()[0] == altcommand:

        if len(config) == 1:
            await sendmarkov(config[0], message)
            return

        arg = message.content.lower().split()[1]

        for c in config:
            if c['command'] == arg:
                await sendmarkov(c, message)


client.run(bottoken)
