import discord
from .markov import Markov
from .config import Config

class MyBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.markov = Markov()


    def run(self):
        super().run(self.config.token, bot=True)


    async def safe_send_message(self, dest, msg):
        try:
            return await self.send_message(dest, msg)
        except discord.HTTPException:
            print("Problem sending a message to {}".format(dest))
        except discord.Forbidden:
            print("No permission to send a message to {}".format(dest))
        except discord.NotFound:
            print("Message destination was not found")


    async def safe_change_nickname(self, server, nick):
    	try:
    		return await self.change_nickname(server.me, nick)
    	except discord.HTTPException:
            print("Problem changing nick in {}".format(dest))
        except discord.Forbidden:
            print("No permission to change nick in {}".format(dest))


    async def safe_change_avatar(self, path):
    	try:
    		with open(path) as a:
    			avatar = a.read()
    		return await self.change_profile(avatar=avatar)
    	except:
    		print("Could not change avatar.")


    async def on_message(self, message):
    	if self.user == message.author:
    		return

    	if message.content.startswith(self.config.prefix):
    		content = message.content.lower()[len(self.config.prefix):].strip()

    		if content == 'help':
    			avail = []
    			for m in self.markov:
    				avail.append('`'+self.config.prefix+m['name']+'`')
    			msg = "Available commands:\n"
    			avail = ', '.join(avail)
    			msg += avail
    			self.safe_send_message(message.channel, msg)

    		if content in self.markov:
    			msg = self.markov.getmarkov(content)

    			for m in self.markov:
    				if m['name'] == content:
    					current = m

    			if message.channel.is_private:
    				self.safe_send_message(message.channel, msg)

    			else:
    				oldname = message.server.me.display_name
    				self.safe_change_nickname(message.server, current['nickname'])
    				self.safe_change_avatar('avatars/'+current['avatar'])
    				self.safe_send_message(message.channel, msg)
    				self.safe_change_nickname(message.server, oldname)
    				self.safe_change_avatar('avatars/default.png')


if __name__ == '__main__':
    bot = MyBot()
    bot.run()