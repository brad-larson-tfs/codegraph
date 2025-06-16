import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Python Web Browser')
        self.setGeometry(100, 100, 900, 600)

        self.browser = QWebEngineView()
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText('Enter URL or local file path (e.g., file:///path/to/file.html)')
        self.go_button = QPushButton('Go')
        self.go_button.clicked.connect(self.load_url)

        layout = QVBoxLayout()
        layout.addWidget(self.url_bar)
        layout.addWidget(self.go_button)
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_url(self):
        url = self.url_bar.text()
        if not url.startswith('http') and not url.startswith('file://'):
            url = 'http://' + url
        self.browser.setUrl(url)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleBrowser()
    window.show()
    sys.exit(app.exec_())
