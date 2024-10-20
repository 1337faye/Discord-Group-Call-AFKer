```markdown
# Discord Group Call Manager Bot

This bot helps manage group voice calls on Discord. It allows users to join and leave calls, and provides helpful commands for easy interaction.

## Requirements

- Python version 3.8 or higher
- [discord.py-self](https://pypi.org/project/discord.py-self/) - A library to interact with Discord's API.
- [PyNaCl](https://pypi.org/project/PyNaCl/) - A required dependency for voice functionality.

You can install the required packages using pip:

pip install discord.py-self pynacl
```

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/1337faye/Discord-Group-Call-AFKer.git
   cd Discord-Group-Call-AFKer
   ```

2. **Modify the Bot Token and Group Chat ID:**
   Open the main bot file (usually `bot.py` or similar) and locate the following lines:

   ```python
   TOKEN = 'insert your very cool token here'  # Replace with your actual Discord bot token
   GROUP_DM_ID = 000000000000000000  # Replace with your Group DM's ID
   ```

   Replace `'YOUR_TOKEN_HERE'` with your actual Discord bot token and `123456789012345678` with your Group DM's ID.

3. **Run the Bot:**
   After making the necessary modifications, run the bot with the following command:

   ```bash
   python bot.py
   ```

## Commands

- `!join` : Join the group call.
- `!leave` : Leave the group call.
- `!help` : Show this help message.
- `!github` : Get a link to the bot's GitHub repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Thanks to the developers of [discord.py-self](https://pypi.org/project/discord.py-self/) and [PyNaCl](https://pypi.org/project/PyNaCl/) for providing the necessary libraries to make this bot functional.
```
