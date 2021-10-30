class MyLogger(object):
  """Base logger class for ytdl"""
  def debug(self, message: str) -> None:
    pass

  def warning(self, message: str) -> None:
    pass

  def error(self, message: str) -> None:
    pass