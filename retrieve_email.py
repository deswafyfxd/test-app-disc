import yaml
import discord
import requests
import os

# Function to get accounts from GitHub
def fetch_accounts():
    url = 'https://raw.githubusercontent.com/deswafyfxd/disc-data-strore/main/accounts.yml'
    response = requests.get(url)
    accounts = yaml.safe_load(response.text)['accounts']
    print(f"Fetched accounts: {accounts}")  # Debug print
    return accounts

# Function to get recovery email from fetched data
def get_recovery_email(outlook_account, accounts):
    return accounts.get(outlook_account)

# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True

# Discord bot client
client = discord.Client(intents=intents)

# Event when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# Event to handle messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!get_recovery'):
        parts = message.content.split(' ')
        if len(parts) != 2:
            await message.channel.send("Please use the correct format: `!get_recovery <outlook_account>`")
            return

        outlook_account = parts[1]
        accounts = fetch_accounts()
        recovery_email = get_recovery_email(outlook_account, accounts)
        if recovery_email:
            response_message = f'The recovery email for {outlook_account} is {recovery_email}'
        else:
            response_message = f'No recovery email found for {outlook_account}'
        await message.channel.send(response_message)
        print(f"Sent response: {response_message}")

client.run(os.getenv('DISCORD_TOKEN'))
