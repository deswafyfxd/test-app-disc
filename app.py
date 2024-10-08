import yaml
import discord
import requests
import psutil
import os

# Function to get accounts from GitHub
def fetch_accounts():
    url = 'https://raw.githubusercontent.com/deswafyfxd/disc-data-strore/main/accounts.yml'
    response = requests.get(url)
    return yaml.safe_load(response.text)['accounts']

# Function to get recovery email from fetched data
def get_recovery_email(outlook_account, accounts):
    return accounts.get(outlook_account)

# Function to get system stats
def get_system_stats():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    stats = {
        "cpu": f"{cpu}%",
        "memory": f"Total: {memory.total // (1024 ** 2)} MB, Available: {memory.available // (1024 ** 2)} MB, Used: {memory.percent}%",
        "disk": f"Total: {disk.total // (1024 ** 3)} GB, Used: {disk.used // (1024 ** 3)} GB, Free: {disk.free // (1024 ** 3)} GB, Used: {disk.percent}%"
    }
    
    return stats

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

    if message.content.startswith('!system_stats'):
        stats = get_system_stats()
        response_message = (
            f"**CPU Usage**: {stats['cpu']}\n"
            f"**Memory**: {stats['memory']}\n"
            f"**Disk**: {stats['disk']}\n"
        )
        await message.channel.send(response_message)
        print(f"Sent system stats: {response_message}")

def run_discord_bot():
    try:
        client.run(os.getenv('DISCORD_TOKEN'))
    except Exception as e:
        print(f"Failed to connect: {e}")

# Main entry point
if __name__ == "__main__":
    # Start Flask app in a thread
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Bot is running!"

    Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    run_discord_bot()
