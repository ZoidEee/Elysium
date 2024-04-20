from PyQt6.QtCore import QUrl, Qt, QSize
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QToolBar, QLabel, QSizePolicy,
    QToolButton
)

from logic.download_media_dialog import DownloadMediaDialog


class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Elysium")
        self.setFixedSize(1000, 800)
        self.setup_main_window_ui()
        self.show()

    def setup_main_window_ui(self):
        """
        This function sets up the main window's UI, including the web view, toolbar, and related actions.
        """
        self.web_view = QWebEngineView()
        self.web_view.load(QUrl("https://www.youtube.com/watch?v=kGScxakv49Q"))
        self.web_view.urlChanged.connect(self.handle_url_change)

        self.setup_main_window_toolbar()

        layout = QVBoxLayout()
        layout.addWidget(self.web_view)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        central_widget.setStyleSheet("background-color: #ffffff;")
        self.setCentralWidget(central_widget)

    def setup_main_window_toolbar(self):
        """
        This function sets up the main window's toolbar, including the back, forward, and download actions,
        as well as a URL label that updates when the webpage changes.
        """
        self.toolbar = QToolBar()

        # QToolbar Properties/Settings
        self.toolbar.setFixedHeight(45)
        self.toolbar.setMovable(False)
        self.toolbar.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.toolbar.setStyleSheet(
            """
            background-color: #f1f3f4;
            padding: 0 10px; 
            """
        )

        self.addToolBar(self.toolbar)
        self.addToolBarBreak()

        # Set the icon size to 25x25
        self.toolbar.setIconSize(QSize(25, 25))

        # Create Toolbar Actions
        self.back_action = QAction(QIcon("icons/back.png"), "Back", self)
        self.back_action.triggered.connect(self.web_view.back)

        self.forward_action = QAction(QIcon("icons/forward.png"), "Forward", self)
        self.forward_action.triggered.connect(self.web_view.forward)

        self.download_action = QAction(QIcon("icons/plus.png"), "Download", self)
        self.download_action.triggered.connect(self.download_media_dialog)

        self.view_downloads_action = QAction(QIcon("icons/download.png"), "View Downloads", self)
        self.view_downloads_action.triggered.connect(self.show_downloads_dialog)

        # Create Toolbar Buttons
        self.back_button = QToolButton()
        self.back_button.setDefaultAction(self.back_action)
        self.back_button.setFixedSize(30, 30)

        self.forward_button = QToolButton()
        self.forward_button.setDefaultAction(self.forward_action)
        self.forward_button.setFixedSize(30, 30)

        self.download_button = QToolButton()
        self.download_button.setDefaultAction(self.download_action)
        self.download_button.setFixedSize(30, 30)

        self.view_downloads_button = QToolButton()
        self.view_downloads_button.setDefaultAction(self.view_downloads_action)
        self.view_downloads_button.setFixedSize(30, 30)

        # Add the buttons to the toolbar
        self.toolbar.addWidget(self.back_button)
        self.toolbar.addWidget(self.forward_button)

        # Set up the URL_box
        self.url_box = QLabel()
        self.url_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.url_box.setFixedHeight(20)
        self.url_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.url_box.setStyleSheet(
            """
            background-color: #f1f3f4; 
            color: #000000;
            """
        )

        self.toolbar.addWidget(self.url_box)

        # Add the download and view downloads buttons to the toolbar
        self.toolbar.addWidget(self.download_button)
        self.toolbar.addWidget(self.view_downloads_button)

        # If the webpage changes then to trigger update_url_box
        self.web_view.urlChanged.connect(self.update_url_box)

    def handle_url_change(self, url):
        """
        This function is triggered when the URL of the web view changes. It checks if the new URL is not on the
        YouTube.com domain or not using HTTPS. If the URL does not meet the criteria, it loads the default
        YouTube.com URL. This ensures that the web browser stays within the YouTube.com domain and uses a secure
        HTTPS connection.
        """
        # Check if the URL is not on the YouTube.com domain or not using HTTPS
        if not (url.host().endswith("youtube.com") and url.scheme() == "https"):
            # Load the default YouTube.com URL
            self.web_view.load(QUrl("https://www.youtube.com"))

    def update_url_box(self, url):
        """
        This function is triggered when the web view's URL changes.
        It updates the text of the url_box widget to display the current URL.
        This allows the user to see the current URL being displayed in the web browser.
        """
        self.url_box.setText(url.toString())

    def download_media_dialog(self):
        current_url = self.web_view.url().toString()
        dialog = DownloadMediaDialog(self, current_url)
        dialog.exec()

    def show_downloads_dialog(self):
        # Implement the download history dialog functionality here
        pass
