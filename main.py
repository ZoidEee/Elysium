import sys
from PyQt6.QtWidgets import QApplication
from ui.webbrowser import WebBrowser

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = WebBrowser()
    browser.show()
    sys.exit(app.exec())