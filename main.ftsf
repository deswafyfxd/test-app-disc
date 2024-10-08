from flask_app import app
from discord_bot import client
from threading import Thread
import os

if __name__ == "__main__":
    # Run Flask app in a separate thread
    Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    client.run(os.getenv('DISCORD_TOKEN'))
