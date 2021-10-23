import re
import errors
import logger
import youtube_dl

def check_url(url: str):
  checking = re.findall('^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$', url)
  if not checking:
    raise errors.InvalidURL(f'"{url}" is an invalid url.')

def check_format(format: str):
  formats = ['aac', 'm4a', 'mp3', 'wav']
  if not format in formats:
    raise errors.InvalidFormat(f'"{format}" is an invalid fiel format. Format must be in aac, m4a, mp3, wav.')


class YoutubeVideoConverter:
  """Base class to convert a yotube video to audio."""
  def __init__(self, url: str, format: str):
    self.url = url
    self.format = format
    self.title = None
    self.size = None

  def my_hook(self, d):
    if d['status'] == 'finished':
      print(f'Converting downloaded video to {self.format}...')

  def convert(self):
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
        print(f'Successfully converted youtube video to {self.format}.')