# Elysium - YouTube Downloader

Elysium is a desktop application built using PyQt6 that allows users to download audio and video content from YouTube. This application provides a user-friendly interface for selecting the desired file format and quality, and automatically saves the downloaded files in a designated directory.

## Features
- YouTube Video Playback: The application embeds a web view that displays the YouTube video, allowing users to navigate and interact with the platform.
- Audio and Video Download: Users can select the desired audio and/or video format and quality, and the application will download the content from the YouTube video.
- Automatic File Organization: The downloaded files are automatically saved in the user's Music folder, with separate "Audio" and "Video" subdirectories for better organization.
- Customizable File Naming: The application allows users to customize the filename by providing a title and artist information, which are then used to generate the final filename.

## Dependencies
The Elysium application requires the following dependencies:
- Python 3.x
- PyQt6
- pytube

## Usage

1. Run the main.py file to start the Elysium application.
2. The main window will display a web view showing the YouTube video.
3. Click the "Download" button in the toolbar to open the download dialog.
4. In the download dialog, select the desired audio and/or video format and quality.
5. Optionally, enter a title and artist information for the downloaded file.
6. Click the "Download" button to initiate the download process.
7. The downloaded files will be saved in the user's Music folder, in the "Elysium/Audio" and "Elysium/Video" subdirectories.

## Customization

The Elysium application can be further customized by modifying the code in the provided files:

- main.py: This file contains the main application logic and the setup of the main window.
- logic/format_fetch_thread.py: This file contains the logic for fetching the available audio and video formats from the YouTube video.
- ui/download_media_dialog.py: This file contains the implementation of the download dialog, including the UI elements and the download functionality.

You can customize the appearance, add new features, or modify the existing functionality by editing the code in these files.

## Version History 
- 0.0.1 -> first upload of the project; redone multiple times prior to try out PEP8 formatting
