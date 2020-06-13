

from youtube_transcript_api import YouTubeTranscriptApi

class Channel:
    def __init__(self, userName, numVideos):
        self.userName = userName
        self.videos = videos


class Video:
    def __init__(self, vidId, title):
        self.vidId = vidId
        self.title = title
        self.lang
    #get the transcript json of the video
    def get_transcript(self):
        return YouTubeTranscriptApi.get_transcript(video_id=self.vidId)



