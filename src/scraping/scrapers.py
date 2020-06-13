
#use youtube_dl for getting the automatic captions
"""
example:
ydl_opts = {'writesubtitles': True, 'allsubtitles': True, 'writeautomaticsub': True}
... with youtube_dl.YoutubeDL(ydl_opts) as ydl:
...     info = ydl.extract_info("https://www.youtube.com/watch?v=fpXngRB-VTw", download=False)
"""
#if you give it a channel url, you can get a list of videos... hopefully?

class Scraper:
    pass

class ChannelScraper(Scraper):
    pass



class VideoScraper(Scraper):
    pass

