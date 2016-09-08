import discord
import markovify
import asyncio

##########
# CONFIG #
##########

# Set this to the path your text is
textdir = "text.txt"

# Bot token goes here
bottoken = "MTg3ODE4MDI4NjQwMTA4NTQ0.CrGbBQ.syQBhtEptt9mNSGcKG0O2a_sres"

# set to False if you want it to seperate sentences based on periods instead of newlines
newline = True

# Set the commands to trigger a markov. The second one is optional
command = ".markov"
altcommand = ".mk"

################

client = discord.Client()

@client.event
async def on_ready():
    await markovcache()
    print('Logged in as:\n{0.name}, {0.id}\n'.format(client.user))

@client.event
async def on_message(message):
    if message.author.bot or message.author == client.user:
        return

    if message.content.lower().split(' ')[0] == command or message.content.lower().split(' ')[0] == altcommand:
        if len(cache) == 0:
            await markovcache()
        msg = cache.pop()
        await client.send_message(message.channel, msg)
        if message.channel.is_private:
            print("PM with {0.author}\n{1}\n".format(message, msg[1:]))
        else:
            print("{0.server.name}#{0.channel.name}\n{1}\n".format(message, msg[1:]))
        await markovcache()


with open(textdir) as t:
    text = t.read()

if newline:
    model = markovify.text.NewlineText(text)
else:
    model = markovify.Text(text)

cache = []

async def markov():
    m = None
    while m == None:
        m = model.make_sentence()
    return "\u200b"+m.encode("ascii","backslashreplace").decode("unicode-escape")

async def markovcache():
    while len(cache) <= 10:
        m = await markov()
        cache.append(m)


client.run(bottoken)
