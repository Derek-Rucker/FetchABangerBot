import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import discord
import random
from dotenv import load_dotenv

scopes = ['https://www.googleapis.com/auth/youtube.readonly']

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('YT_API_KEY')

intents = discord.Intents.all()
intents.message_content

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!banger':
        await get_playlist(message)


async def get_playlist(message):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    api_service_name = 'youtube'
    api_version = 'v3'

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY
    )

    all_video_ids = []
    next_page = True
    page_token = ''
    playlist_id = 'PLm323Lc7iSW9oSIDihesMJXmMNfh8U59k'

    while next_page:
        request = youtube.playlistItems().list(
            part='snippet,contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=page_token
        )
        response = request.execute()

        for videos in response['items']:
            all_video_ids.append(videos['contentDetails']['videoId'])

        if 'nextPageToken' not in response:
            next_page = False
        else:
            page_token = response['nextPageToken']

    video_id = random.choice(all_video_ids)
    await message.channel.send('B A N G E R S')
    await message.channel.send(f'https://www.youtube.com/watch?v={video_id}')

client.run(TOKEN)
