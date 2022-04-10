import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PyQt6.QtCore import QUrl
from dbus_notify import ZapNotifications

URL = 'https://www.bennish.net/web-notifications.html'


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setMinimumSize(800, 800)
        self.browser = Browser()
        self.setCentralWidget(self.browser)


class Browser(QWebEngineView):
    def __init__(self):
        super().__init__()
        profile = QWebEngineProfile(self)
        profile.setNotificationPresenter(self.show_notification)

        self.page = WebPage(profile, self)
        self.setPage(self.page)

        self.load(QUrl(URL))

    def show_notification(self, notification):
        zap = ZapNotifications(notification, self.parent)
        zap.show()


class WebPage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        QWebEnginePage.__init__(self, *args, **kwargs)
        self.featurePermissionRequested.connect(self.permission)

    def permission(self, frame, feature):
        self.setFeaturePermission(
            frame, feature,  QWebEnginePage.PermissionPolicy.PermissionGrantedByUser)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Notification test")
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
