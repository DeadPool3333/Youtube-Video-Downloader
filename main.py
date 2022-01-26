from os import getcwd
from os.path import isdir

from pytube import YouTube


class YVDException(Exception):
    ...


url = input('Enter the youtube video\'s URL: ')

try:
    youtube = YouTube(url)
except Exception as e:
    raise YVDException(*e.args)

info = f'''Title: {youtube.title}
Length of video (in seconds): {youtube.length}
Published on: {youtube.publish_date}
Views: {youtube.views}
Thumbnail: {youtube.thumbnail_url}
Author: {youtube.author}
Channel URL: {youtube.channel_url}

Description: {youtube.description}'''
print(info)

path = input(
    'Enter the path where you want to store\nor press Enter to store in current path: '
)
path = path or getcwd()

if not isdir(path):
    raise YVDException(f'{path} is not a valid directory')

filename = input(
    'Enter the filename name to keep it as downloaded file\'s name\nor press Enter to keep it as default name: '
)
filename = filename or 'yt-download'
filename += '.mp4'

video = youtube.streams.get_highest_resolution()

try:
    video.download(path, filename)
except Exception as e:
    raise YVDException(*e.args)

print('Download completed!')
