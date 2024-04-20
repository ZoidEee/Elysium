import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QCheckBox, QComboBox, QProgressBar, QPushButton
from logic.format_fetch_thread import FormatFetchThread


class DownloadMediaDialog(QDialog):
    """
    A dialog window for downloading media from a given URL.

    This class fetches the available audio and video formats from the URL,
    allows the user to select the desired format, and then downloads the
    media to the appropriate directory.
    """

    def __init__(self, parent=None, url=None):
        """
        Initialize the DownloadMediaDialog.

        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
            url (str, optional): The URL of the media to be downloaded. Defaults to None.
        """
        super().__init__(parent)
        self.url = url
        self.format_fetch_thread = FormatFetchThread(url)
        self.format_fetch_thread.format_fetched.connect(self.on_formats_fetched)
        self.init_ui()

    def init_ui(self):
        """
        Initialize the user interface of the DownloadMediaDialog.

        This method sets the window title, size, and calls the `setup_UI` method
        to create the layout and widgets.
        """
        self.setWindowTitle("Download Media")
        self.setFixedSize(500, 350)
        self.setup_UI()
        self.format_fetch_thread.start()

    def setup_UI(self):
        """
        Set up the user interface of the DownloadMediaDialog.

        This method creates the layout and widgets, and arranges them in a grid layout.
        """
        layout = QGridLayout()

        self.video_title = QLabel("Title: ")
        self.video_title_input = QLineEdit()
        self.video_title_input.setPlaceholderText("Title:")

        self.video_artist = QLabel("Artist: ")
        self.video_artist_input = QLineEdit()
        self.video_artist_input.setPlaceholderText("Artist:")

        self.audio_format_cb = QCheckBox("Audio Format")
        self.audio_format_cb.toggled.connect(self.toggle_audio_format)

        self.video_format_cb = QCheckBox("Video Format")
        self.video_format_cb.toggled.connect(self.toggle_video_format)

        self.audio_file_l = QLabel("File Type: ")
        self.audio_file_cmb = QComboBox()
        self.audio_file_cmb.currentIndexChanged.connect(self.update_audio_qualities)
        self.audio_file_cmb.setEnabled(False)

        self.audio_quality_l = QLabel("Audio Quality: ")
        self.audio_quality_cmb = QComboBox()
        self.audio_quality_cmb.setEnabled(False)

        self.video_file_l = QLabel("File Type: ")
        self.video_file_cmb = QComboBox()
        self.video_file_cmb.currentIndexChanged.connect(self.update_video_qualities)
        self.video_file_cmb.setEnabled(False)

        self.video_quality_l = QLabel("Video Quality: ")
        self.video_quality_cmb = QComboBox()
        self.video_quality_cmb.setEnabled(False)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.hide()

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_media)

        self.add_widgets_to_layout(layout)
        self.setLayout(layout)

    def add_widgets_to_layout(self, layout):
        """
        Add the widgets to the grid layout.

        Args:
            layout (QGridLayout): The grid layout to add the widgets to.
        """
        layout.addWidget(self.video_title, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.video_title_input, 0, 2, 1, 3, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.video_artist, 1, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.video_artist_input, 1, 2, 1, 3, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.audio_format_cb, 2, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.audio_file_l, 3, 1, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.audio_file_cmb, 3, 2, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.audio_quality_l, 4, 1, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.audio_quality_cmb, 4, 2, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.video_format_cb, 5, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.video_file_l, 6, 1, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.video_file_cmb, 6, 2, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.video_quality_l, 7, 1, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.video_quality_cmb, 7, 2, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.progress_bar, layout.rowCount(), 0, 1, -1)
        layout.addWidget(self.download_button, layout.rowCount(), 0, 1, -1, Qt.AlignmentFlag.AlignCenter)

    def on_formats_fetched(self):
        """
        Handle the event when the available formats have been fetched.

        This method populates the audio and video format comboboxes, hides the progress bar,
        and sets the progress bar range to 100.
        """
        self.populate_audio_formats(self.format_fetch_thread.audio_formats)
        self.populate_video_formats(self.format_fetch_thread.video_formats)
        self.progress_bar.setValue(100)
        self.progress_bar.hide()

    def populate_audio_formats(self, audio_formats):
        """
        Populate the audio format combobox with the available formats.

        Args:
            audio_formats (dict): A dictionary of available audio formats and their qualities.
        """
        self.audio_file_cmb.clear()
        self.audio_quality_cmb.clear()
        self.audio_file_cmb.addItems(sorted(audio_formats.keys()))
        self.update_audio_qualities(0)

    def update_audio_qualities(self, index):
        """
        Update the audio quality combobox with the available qualities for the selected format.

        Args:
            index (int): The index of the selected audio format in the combobox.
        """
        selected_format = self.audio_file_cmb.currentText()
        self.audio_quality_cmb.clear()
        self.audio_quality_cmb.addItems(
            sorted([str(q) for q in self.format_fetch_thread.audio_formats[selected_format]]))

    def populate_video_formats(self, video_formats):
        """
        Populate the video format combobox with the available formats.

        Args:
            video_formats (dict): A dictionary of available video formats and their qualities.
        """
        self.video_file_cmb.clear()
        self.video_quality_cmb.clear()
        self.video_file_cmb.addItems(sorted(video_formats.keys()))
        self.update_video_qualities(0)

    def update_video_qualities(self, index):
        """
        Update the video quality combobox with the available qualities for the selected format.

        Args:
            index (int): The index of the selected video format in the combobox.
        """
        selected_format = self.video_file_cmb.currentText()
        self.video_quality_cmb.clear()
        if selected_format == "MP4":
            self.video_quality_cmb.addItems(sorted([str(q) for q in self.format_fetch_thread.video_formats["MP4"]]))
        elif selected_format == "WebM":
            self.video_quality_cmb.addItems(sorted([str(q) for q in self.format_fetch_thread.video_formats["WebM"]]))

    def toggle_audio_format(self, checked):
        """
        Toggle the visibility and enabled state of the audio format widgets.

        Args:
            checked (bool): Whether the audio format checkbox is checked.
        """
        self.audio_file_l.setEnabled(checked)
        self.audio_file_cmb.setEnabled(checked)
        self.audio_quality_l.setEnabled(checked)
        self.audio_quality_cmb.setEnabled(checked)

    def toggle_video_format(self, checked):
        """
        Toggle the visibility and enabled state of the video format widgets.

        Args:
            checked (bool): Whether the video format checkbox is checked.
        """
        self.video_file_l.setEnabled(checked)
        self.video_file_cmb.setEnabled(checked)
        self.video_quality_l.setEnabled(checked)
        self.video_quality_cmb.setEnabled(checked)

    def download_media(self):
        """
        Download the selected audio and/or video media.

        This method constructs the file name, creates the necessary directories,
        and calls the `download_audio` and `download_video` methods to download
        the selected media.
        """
        title = self.video_title_input.text().strip().replace(" ", "_")
        artist = self.video_artist_input.text().strip().replace(" ", "_")
        filename = f"{title}-{artist}"

        download_dir = os.path.join(os.path.expanduser("~"), "Music", "Elysium")
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        audio_dir = os.path.join(download_dir, "Audio")
        video_dir = os.path.join(download_dir, "Video")

        for dir_path in (audio_dir, video_dir):
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

        if self.audio_format_cb.isChecked():
            audio_format = self.audio_file_cmb.currentText()
            audio_quality = self.audio_quality_cmb.currentText()
            self.download_audio(os.path.join(audio_dir, f"{filename}.{audio_format.lower()}"), audio_format,
                                audio_quality)

        if self.video_format_cb.isChecked():
            video_format = self.video_file_cmb.currentText()
            video_quality = self.video_quality_cmb.currentText()
            self.download_video(os.path.join(video_dir, f"{filename}.{video_format.lower()}"), video_format,
                                video_quality)

        self.accept()

    def download_audio(self, save_path, audio_format, audio_quality):
        """
        Download the selected audio media.

        Args:
            save_path (str): The path to save the downloaded audio file.
            audio_format (str): The selected audio format.
            audio_quality (str): The selected audio quality.
        """
        stream = self.format_fetch_thread.yt.streams.filter(only_audio=True, abr=audio_quality).first()
        stream.download(output_path=os.path.dirname(save_path), filename=os.path.basename(save_path))

    def download_video(self, save_path, video_format, video_quality):
        """
        Download the selected video media.

        Args:
            save_path (str): The path to save the downloaded video file.
            video_format (str): The selected video format.
            video_quality (str): The selected video quality.
        """
        stream = self.format_fetch_thread.yt.streams.filter(resolution=video_quality,
                                                            file_extension=video_format.lower()).first()
        stream.download(output_path=os.path.dirname(save_path), filename=os.path.basename(save_path))
