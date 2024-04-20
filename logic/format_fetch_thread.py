from PyQt6.QtCore import QThread, pyqtSignal
from pytube import YouTube


class FormatFetchThread(QThread):
    """
    A thread that fetches the audio and video formats for a given YouTube URL.

    Attributes:
        format_fetched (pyqtSignal): A signal emitted when the formats have been fetched.
        url (str): The YouTube URL.
        yt (YouTube): The YouTube object.
        audio_formats (dict): A dictionary of available audio formats and their qualities.
        video_formats (dict): A dictionary of available video formats and their qualities.
    """
    format_fetched = pyqtSignal()

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.yt = YouTube(url)
        self.audio_formats = {}
        self.video_formats = {}

    def run(self):
        """
        Runs the thread and populates the audio and video formats.
        """
        self.populate_audio_formats(self.yt.streams.filter(only_audio=True))
        self.populate_video_formats(self.yt.streams.filter(only_video=True))
        self.format_fetched.emit()

    def populate_audio_formats(self, audio_streams):
        """
        Populates the audio formats dictionary.

        Args:
            audio_streams (iterable): An iterable of audio streams.
        """
        for stream in audio_streams:
            audio_format = stream.mime_type.split('-')[0].split("/")[1]
            audio_quality = stream.abr

            if audio_format not in self.audio_formats:
                self.audio_formats[audio_format] = set()
            self.audio_formats[audio_format].add(audio_quality)

    def populate_video_formats(self, video_streams):
        """
        Populates the video format's dictionary.

        Args:
            video_streams (iterable): An iterable of video streams.
        """
        self.video_formats = {
            "MP4": set(),
            "WebM": set()
        }

        for stream in video_streams:
            video_format = stream.mime_type.split('-')[0].split("/")[1]
            video_quality = stream.resolution

            if video_format == "mp4":
                self.video_formats["MP4"].add(video_quality)
            elif video_format == "webm":
                self.video_formats["WebM"].add(video_quality)
