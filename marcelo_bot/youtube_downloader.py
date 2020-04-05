import youtube_dl
import asyncio
from discord import PCMVolumeTransformer, FFmpegPCMAudio

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

YTDL_OPTS = {
    "default_search": "ytsearch",
    "format": "bestaudio/best",
    "quiet": True,
    "extract_flat": "in_playlist"
}

FFMPEG_OPTS = {
    'options': '-vn'
}

class YoutubeDownloader():
    def __init__(self, url):
        with youtube_dl.YoutubeDL(YTDL_OPTS) as ytdl:
            data = self._get_video_info(url)
            self.data = data
            self.title = data.get('title')
            self.url = data.get('url')
            self.duration = data.get('duration') or 0

    def _get_video_info(self, url_or_search):
        with youtube_dl.YoutubeDL(YTDL_OPTS) as ytdl:
            info = ytdl.extract_info(url_or_search, download = False)
            video = None
            if "_type" in info and info["_type"] == "playlist":
                print(info["entries"][0])
                return self._get_video_info(
                    info["entries"][0]["url"])  # get info for first video
            else:
                video = info
            return video

    def get_player(self):
        """Get Audio from discord lib"""
        url = self.data['url']
        return PCMVolumeTransformer(FFmpegPCMAudio(url, **FFMPEG_OPTS))