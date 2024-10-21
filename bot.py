"""
Made by Faye, check out my cool stuff @ https://faye.lol !!!! 

MIT License

Copyright (c) 2024 Faye A

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import discord
import asyncio
import random
import requests
import signal
import time


# Replace with your actual user token and group DM ID
TOKEN = "insert your very cool token here"  # I recommend you store this in your environment variables (or else you're probably cooked)
GROUP_DM_ID = 69420  # Replace with your Group DM's ID (this matters less in terms of security but still, don't share it)

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = time.time()  # Store the start time when the bot starts

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        game = discord.Game("Managing group calls | !help")
        await self.change_presence(status=discord.Status.do_not_disturb, activity=game)
        
    
    async def send_exit_message(self):
        channel = self.get_channel(GROUP_DM_ID)
        if channel:
            await channel.send(f"**This bot is shutting down, this could be for a variety of reasons, if this is not intended, check your logs.**")

    async def confirm_action(self, message, action):
        try:
            confirmation_msg = f'{message.author.mention}, React with ✅ to confirm or ❌ to cancel {action}.'
            confirm_message = await message.channel.send(confirmation_msg)
            
            # Add reactions for confirmation
            await confirm_message.add_reaction('✅')
            await confirm_message.add_reaction('❌')

            # Wait for reaction from the user
            def reaction_check(reaction, user):
                return user == message.author and str(reaction.emoji) in ['✅', '❌']

            reaction, user = await self.wait_for('reaction_add', timeout=15.0, check=reaction_check) #15 secs

            if str(reaction.emoji) == '✅':
                return True  # Action confirmed
            else:
                await message.channel.send(f'**Action canceled.**')
                return False  # Action canceled
        except asyncio.TimeoutError:
            await message.channel.send(f'**Action timed out, {action} canceled.**')
            return False  # Action canceled due to timeout

    async def start_whiteboard(self, channel_id, session_id, nonce):
        url = "https://discord.com/api/v9/interactions"
        
        headers = {
            "accept": "*/*",
            "authorization": f"{TOKEN}",  # Authorization token as a variable
            "content-type": "application/json",  # Use JSON instead of multipart/form-data
            "origin": "https://discord.com",
            "referer": f"https://discord.com/channels/@me/{channel_id}",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        }

        payload = {
            "type": 2,
            "application_id": "1070087967294631976",  # Whiteboard application ID
            "channel_id": channel_id,  
            "session_id": session_id,  # Variable representing the session ID
            "data": {
                "version": "1275950090028056640",
                "id": "1275950090028056639",  # Command ID
                "name": "launch",  # Command name
                "type": 4,
                "options": [],
                "application_command": {
                    "id": "1275950090028056639",
                    "type": 4,
                    "version": "1275950090028056640",
                    "name": "launch",
                    "dm_permission": True,
                    "contexts": [0, 1, 2],
                    "integration_types": [0, 1],
                    "handler": 2,
                    "description": "",
                    "options": [],
                    "name_localized": "launch"
                },
                "attachments": []
            },
            "nonce": nonce,  # Variable for nonce
            "analytics_location": "activities_mini_shelf"
        }

        # Make the request with JSON payload
        response = requests.post(url, headers=headers, json=payload)  # Use json=payload
        if response.status_code in {200, 201, 204}:
            return None
        else:
            raise Exception(f"{response.status_code} - {response.text}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.lower() == '!help':
            help_msg = """
**Available commands:**
- `!join` : Join the group call.
- `!leave` : Leave the group call.
- `!github` : Get a link to my GitHub.
- `!help` : Show this help message.
- `!uptime` : Tells you how long this bot has been running.
"""
            await message.channel.send(help_msg)

        if message.channel.id == GROUP_DM_ID:
            if message.content.lower() == '!join':
                group_channel = self.get_channel(GROUP_DM_ID)

                if not self.voice_clients:
                    if await self.confirm_action(message, 'joining the call'):
                        try:
                            # Join the group call
                            await group_channel.connect()
                            await message.channel.send(f'** User "{self.user.name}" has successfully joined the call.**')
                            
                            try:
                                await message.channel.send(f"**Starting Whiteboard activity so Discord won't terminate this session.**")
                                await self.start_whiteboard(GROUP_DM_ID, session_id=self.sessions[0].session_id, nonce=str(random.randint(10**18, 10**18 + 2*(10**17))))
                                await message.channel.send(f"**Whiteboard activity started.**")
                            except Exception as e:
                                await message.channel.send(f'**Error starting Whiteboard activity:** {str(e)}')
                                await message.channel.send(f"**The call will continue but Discord will likely terminate it in 2-5 hours.**")
                            
                        except Exception as e:
                            await message.channel.send(f'**Error joining call:** {str(e)}')
                    else:
                        print('Join action was not confirmed.')
                else:
                    await message.channel.send(f'**{self.user.name} is already in the call.**')

            elif message.content.lower() == '!leave':
                voice_client = discord.utils.get(self.voice_clients, guild=message.guild)

                if voice_client and voice_client.is_connected():
                    if await self.confirm_action(message, 'leaving the call'):
                        try:
                            # Leave the call
                            await voice_client.disconnect()
                            await message.channel.send(f'**{self.user.name} has left the call.**')
                        except Exception as e:
                            await message.channel.send(f'**Error leaving call:** {str(e)}')
                    else:
                        print('Leave action was not confirmed.')
                else:
                    await message.channel.send(f'**{self.user.name} is not currently in the call.**')

            elif message.content.lower() == '!github':
                await message.channel.send(f'**GitHub Repository:**  \n - https://github.com/1337faye/Discord-Group-Call-AFKer/')
            elif message.content.lower() == '!uptime':
                uptime_seconds = int(time.time() - self.start_time)
                hours, remainder = divmod(uptime_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                uptime_msg = f"**Uptime:** {hours}h {minutes}m {seconds}s"
                await message.channel.send(uptime_msg)
def signal_handler(sig, frame):
    asyncio.create_task(client.send_exit_message())
    asyncio.create_task(client.close())  # Gracefully close the client

client = MyClient()

# Register signal handlers for multiple signals
signals = [signal.SIGINT, signal.SIGTERM, signal.SIGQUIT, signal.SIGHUP]
for sig in signals:
    signal.signal(sig, signal_handler)

client.run(TOKEN)
