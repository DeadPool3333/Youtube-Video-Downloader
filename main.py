from src import converter

url = str(input('Enter a youtube URL: '))
converter.check_url(url)
converter.check_video_status(url)

format = str(input('Enter a file format type: '))
converter.check_format(format)

if __name__ == '__main__':
  converter.YoutubeVideoConverter(url, format).download()