import converter

url = str(input('Enter a youtube URL: '))
converter.check_url(url)

format = str(input('Enter a format type: '))
converter.check_format(format)

if __name__ == '__main__':
  converter.YoutubeVideoConverter(url, format).convert()