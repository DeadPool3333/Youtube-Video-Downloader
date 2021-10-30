import re
import json
import requests
import youtube_dl

from src import errors, logger

def check_url(url: str) -> None:
  """Checks if given url is an valid youtube url or not."""
  if not url:
    raise errors.InvalidURL('You must enter an url.')
  checking = re.findall('^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$', url)
  if not checking:
    raise errors.InvalidURL(f'"{url}" is an invalid url.')

def check_format(format: str) -> None:
  """Checks if given format is an valid format ot not."""
  if not format:
    raise errors.InvalidFormat('You must enter a format.')
  formats = ['aac', 'm4a', 'mp3', 'wav']
  if not format in formats:
    raise errors.InvalidFormat(f'"{format}" is an invalid file format. Format must be in aac, m4a, mp3, wav.')

def check_video_status(url: str) -> None:
  """Checks if the given youtube video's url is valid or not."""
  request = requests.get(f'https://www.youtube.com/oembed?format=json&url={url}')
  if request.text == 'Bad Request':
    raise errors.InvalidURL(f'"{url}" is an invliad youtube url.')

def get_video_data(url: str) -> dict:
  """Returns yotuube video's data like title, etc..."""
  request = requests.get(f'https://www.youtube.com/oembed?format=json&url={url}')
  request = request.text
  return json.loads(request)


class YoutubeVideoConverter:
  """Base class to convert a yotube video to audio."""
  def __init__(self, url: str, format: str):
    self.url = url
    self.format = format

  def my_hook(self, d) -> None:
    """Base ytdl hook."""
    if d['status'] == 'finished':
      print(f'Converting downloaded video to {self.format}...')

  def download(self) -> None:
    """Download given youtube video's url to audio."""
    print('Started downloading video from youtube...')
    ytdl_options = {
      'format': 'bestaudio/best',
      'postprocessors': [
        {
        'key': 'FFmpegExtractAudio',
        'preferredcodec': self.format,
        'preferredquality': '192',
        }
      ],
        'logger': logger.MyLogger(),
        'progress_hooks': [self.my_hook],
    }
    with youtube_dl.YoutubeDL(ytdl_options) as ydl:
      try:
        ydl.download([self.url])
      except:
        raise errors.InvalidURL('Invalid youtube video url.')
      else:
        data = get_video_data(self.url)
        title = data['title']
        channel = data['author_name']
        print(f'Successfully converted youtube video to {self.format}.\n----------\nTitle: {title}t\nChannel: {channel}')