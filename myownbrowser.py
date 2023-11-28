from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QTimer, Qt, QTime

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # Navigation Bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Back Button
        back_btn = QAction('Back', self)
        back_btn.setStatusTip('Back to previous page')
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # Forward Button
        forward_btn = QAction('Forward', self)
        forward_btn.setStatusTip('Forward to next page')
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        # Reload Button
        reload_btn = QAction('Reload', self)
        reload_btn.setStatusTip('Reload page')
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        # Home Button
        home_btn = QAction('Home', self)
        home_btn.setStatusTip('Go home')
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)


        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Updating URL bar
        self.browser.urlChanged.connect(self.update_urlbar)

        
        # Set Modern Retro Style
        
        self.setup_home_page()
        self.navigate_home()

        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000) 

    def search(self):
        search_query = self.url_bar.text()

        # Check if a webview already exists
        if hasattr(self, 'browser') and isinstance(self.browser, QWebEngineView):
            # Disconnect signals to prevent interference
            self.browser.urlChanged.disconnect()
            self.browser.setParent(None)
        try:
            # Create a new webview and set it as the central widget
            new_webview = QWebEngineView()
            self.setCentralWidget(new_webview)

            # Load the search query in the new webview
            new_webview.setUrl(QUrl(f"https://www.google.com/search?q={search_query}"))

            # Connect the urlChanged signal to update the URL bar
            new_webview.urlChanged.connect(self.update_urlbar)

            # Update the browser reference
            self.browser = new_webview
        except Exception as e:
            print(f"Error creating webview: {e}")
    def retro_style(self):
        retro_stylesheet = """
            QMainWindow {
                background-color: #2e3a40;
                color: #ececec;
            }

            QToolBar {
                background-color: #1c2529;
                border: 1px solid #142224;
            }

            QToolButton {
                background-color: #1c2529;
                border: 1px solid #142224;
            }

            QToolButton:hover {
                background-color: #264b5c;
                border: 1px solid #1c2529;
            }

            QLineEdit {
                background-color: #1c2529;
                color: #ececec;
                border: 1px solid #142224;
                padding: 5px;
            }

            QLineEdit:focus {
                background-color: #264b5c;
                border: 1px solid #264b5c;
            }
        """
        self.setStyleSheet(retro_stylesheet)

        # Set a retro font
        font = self.font()
        font.setFamily("Courier New")
        font.setPointSize(12)
        self.setFont(font)

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.example.com"))

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.browser.setUrl(q)

    def update_urlbar(self, q):
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://localhost:8000"))

    
    def setup_home_page(self):
        home_frame = QFrame()
        home_layout = QVBoxLayout()

        # Welcome Message
        welcome_label = QLabel("Welcome to the Retro Browser")
        welcome_label.setStyleSheet("font-size: 24px; color: #ffcc00; margin-bottom: 20px;")

        # Time and Date Display
        self.time_label = QLabel()
        self.time_label.setStyleSheet("font-size: 18px; color: #ffcc00;")
        home_layout.addWidget(self.time_label, alignment=Qt.AlignCenter)

        # Search Box and Button
        search_layout = QHBoxLayout()

        search_box = QLineEdit()
        search_box.setPlaceholderText("Type your search here...")
        search_box.setStyleSheet("padding: 10px; font-size: 16px;")
        search_layout.addWidget(search_box)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)
        search_button.setStyleSheet("padding: 10px; font-size: 16px;")
        search_layout.addWidget(search_button)

        # Add Search Layout to Home Layout
        home_layout.addWidget(welcome_label, alignment=Qt.AlignCenter)
        home_layout.addLayout(search_layout)

        home_frame.setLayout(home_layout)

        # Set Central Widget with a layout to center it
        central_layout = QVBoxLayout()
        central_layout.addWidget(home_frame, alignment=Qt.AlignCenter)

        central_widget = QWidget()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)


    
    def search(self):
        search_query = self.url_bar.text()
        # For simplicity, let's open the search query in DuckDuckGo.
        self.browser.setUrl(QUrl(f"https://duckduckgo.com/?q={search_query}"))
    
        # Load the custom home page
       

        # Disable the context menu on the home page
        self.browser.page().setContextMenuPolicy(Qt.NoContextMenu)

    def update_time(self):
        current_time = QTime.currentTime()
        time_text = current_time.toString("hh:mm AP")
        self.time_label.setText(time_text)

app = QApplication([])
QApplication.setApplicationName("Simple Browser")
window = Browser()
app.exec_()
