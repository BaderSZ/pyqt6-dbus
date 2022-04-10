import dbus
from PyQt6.QtCore import QStandardPaths, Qt
from PyQt6.QtGui import QPainter, QPainter, QImage, QBrush, QPen

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

__appname__ = 'Notification test'

class ZapNotifications:

    def __init__(self, q_notification, manWindow) -> None:
        self.q_notification = q_notification
        self.manWindow = manWindow

    def show(self):
        item = "org.freedesktop.Notifications"
        path = "/org/freedesktop/Notifications"
        interface = "org.freedesktop.Notifications"
        id_num_to_replace = 0
        actions = {}
        app_name = __appname__
        hints = {}
        time = 2000
        bus = dbus.SessionBus()
        notif = bus.get_object(item, path)

        # ações
        #actions['view'] = ('View', self.manWindow.on_show, None)

        # <expressao1> if <condicao> else <expressao2>
        icon = self.getPathImage(self.q_notification.icon(), self.q_notification.title(
        )) 

        title = self.q_notification.title() 

        message = self.q_notification.message()

        notify = dbus.Interface(notif, interface)
        notify.Notify(app_name, id_num_to_replace, icon,
                      title, message, self._makeActionsList(actions), hints, time)

        # We have a mainloop, so connect callbacks
        notify.connect_to_signal(
            'ActionInvoked', self._onActionInvoked)

        notify.connect_to_signal(
            'NotificationClosed', self._onNotificationClosed)

    def _onNotificationClosed(self,nid, reason):
        print("""Called when the notification is closed""")
        #nid, reason = int(nid), int(reason)
        #print(nid, reason)

    def _onActionInvoked(self, nid, action):
        print("""Called when a notification action is clicked""")
        #nid, action = int(nid), int(action)
        #print(nid, action)
        

    def _makeActionsList(self, actions):
        """Make the actions array to send over DBus"""
        arr = []
        for action, (label, callback, user_data) in actions.items():
            arr.append(action)
            arr.append(label)
        return arr

    def getPathImage(self, qin, title):
        try:  # só por garantia de não quebrar a aplicação por causa de um ícone
            path = QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.AppLocalDataLocation)+'/tmp/'+title+'.png'

            # deixa a foto arrendondada
            qout = QImage(qin.width(), qin.height(),
                          QImage.Format.Format_ARGB32)
            qout.fill(Qt.GlobalColor.transparent)

            brush = QBrush(qin)

            pen = QPen()
            pen.setColor(Qt.GlobalColor.darkGray)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)

            painter = QPainter(qout)
            painter.setBrush(brush)
            painter.setPen(pen)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.drawRoundedRect(0, 0, qin.width(), qin.height(),
                                    qin.width()//2, qin.height()//2)
            painter.end()
            c = qout.save(path)
            if(c == False):
                return 'user'
            else:
                return path
        except:
            return 'user'