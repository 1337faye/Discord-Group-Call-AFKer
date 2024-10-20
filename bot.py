import discord
import asyncio

# Replace with your actual user token and group DM ID
TOKEN = 'insert your very cool token'
GROUP_DM_ID = 000000000000000000000  # Replace with your Group DM's ID

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        # Set a game status when the bot is ready
        game = discord.Game("Managing group calls | !help")
        await self.change_presence(status=discord.Status.idle, activity=game)

    async def confirm_action(self, message, action):
        def check(m):
            return m.author == message.author and m.channel == message.channel and m.content.lower() == 'yes'

        try:
            confirmation_msg = f'{message.author.mention}, React with ✅ to confirm or ❌ to cancel {action}.'
            confirm_message = await message.channel.send(confirmation_msg)
            
            # Add reactions for confirmation
            await confirm_message.add_reaction('✅')
            await confirm_message.add_reaction('❌')

            # Wait for reaction from the user
            def reaction_check(reaction, user):
                return user == message.author and str(reaction.emoji) in ['✅', '❌']

            reaction, user = await self.wait_for('reaction_add', timeout=15.0, check=reaction_check)

            if str(reaction.emoji) == '✅':
                return True  # Action confirmed
            else:
                await message.channel.send(f'**Action canceled.**')
                return False  # Action canceled
        except asyncio.TimeoutError:
            await message.channel.send(f'**Action timed out, {action} canceled.**')
            return False  # Action canceled due to timeout

    async def on_message(self, message):
        if message.author == self.user:
            return

        # Help command to list available commands
        if message.content.lower() == '!help':
            help_msg = """
**Available commands:**
- `!join` : Join the group call.
- `!leave` : Leave the group call.
- `!help` : Show this help message.
- `!github` : Get a link to my GitHub.
"""
            await message.channel.send(help_msg)

        # Check if the message is from the specified group DM
        if message.channel.id == GROUP_DM_ID:
            if message.content.lower() == '!join':
                group_channel = self.get_channel(GROUP_DM_ID)

                if not self.voice_clients:
                    if await self.confirm_action(message, 'joining the call'):
                        try:
                            # Join the group call
                            await group_channel.connect()
                            await message.channel.send(f'**{self.user.name} has successfully joined the call.**')
                            print(f'Joined call in group chat {group_channel}')
                        except Exception as e:
                            await message.channel.send(f'**Error joining call:** {str(e)}')
                            print(f'Error: {str(e)}')
                    else:
                        print('Join action was not confirmed.')
                else:
                    await message.channel.send(f'**{self.user.name} is already in the call.**')
                    print('Already in the call.')

            elif message.content.lower() == '!leave':
                voice_client = discord.utils.get(self.voice_clients, guild=message.guild)

                if voice_client and voice_client.is_connected():
                    if await self.confirm_action(message, 'leaving the call'):
                        try:
                            # Leave the call
                            await voice_client.disconnect()
                            await message.channel.send(f'**{self.user.name} has left the call.**')
                            print('Left the group call.')
                        except Exception as e:
                            await message.channel.send(f'**Error leaving call:** {str(e)}')
                            print(f'Error: {str(e)}')
                    else:
                        print('Leave action was not confirmed.')
                else:
                    await message.channel.send(f'**{self.user.name} is not currently in the call.**')
                    print('Not in the call.')

            elif message.content.lower() == '!github':
              await message.channel.send(f'**GitHub Repository:**  \n - https://github.com/1337faye/Discord-Group-Call-AFKer/')

client = MyClient()

client.run(TOKEN)
