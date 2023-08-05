from settings import *
from PyQt5 import QtCore, QtGui
from toxcore_enums_and_consts import TOX_PUBLIC_KEY_SIZE


class BaseContact:
    """
    Class encapsulating TOX contact
    Properties: name (alias of contact or name), status_message, status (connection status)
    widget - widget for update, tox id (or public key)
    Base class for all contacts.
    """

    def __init__(self, name, status_message, widget, tox_id):
        """
        :param name: name, example: 'Toxygen user'
        :param status_message: status message, example: 'Toxing on Toxygen'
        :param widget: ContactItem instance
        :param tox_id: tox id of contact
        """
        self._name, self._status_message = name, status_message
        self._status, self._widget = None, widget
        self._tox_id = tox_id
        self.init_widget()

    # -----------------------------------------------------------------------------------------------------------------
    # Name - current name or alias of user
    # -----------------------------------------------------------------------------------------------------------------

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = str(value, 'utf-8')
        self._widget.name.setText(self._name)
        self._widget.name.repaint()

    name = property(get_name, set_name)

    # -----------------------------------------------------------------------------------------------------------------
    # Status message
    # -----------------------------------------------------------------------------------------------------------------

    def get_status_message(self):
        return self._status_message

    def set_status_message(self, value):
        self._status_message = str(value, 'utf-8')
        self._widget.status_message.setText(self._status_message)
        self._widget.status_message.repaint()

    status_message = property(get_status_message, set_status_message)

    # -----------------------------------------------------------------------------------------------------------------
    # Status
    # -----------------------------------------------------------------------------------------------------------------

    def get_status(self):
        return self._status

    def set_status(self, value):
        self._status = value
        self._widget.connection_status.update(value)

    status = property(get_status, set_status)

    # -----------------------------------------------------------------------------------------------------------------
    # TOX ID. WARNING: for friend it will return public key, for profile - full address
    # -----------------------------------------------------------------------------------------------------------------

    def get_tox_id(self):
        return self._tox_id

    tox_id = property(get_tox_id)

    # -----------------------------------------------------------------------------------------------------------------
    # Avatars
    # -----------------------------------------------------------------------------------------------------------------

    def load_avatar(self):
        """
        Tries to load avatar of contact or uses default avatar
        """
        prefix = ProfileHelper.get_path() + 'avatars/'
        avatar_path = prefix + '{}.png'.format(self._tox_id[:TOX_PUBLIC_KEY_SIZE * 2])
        if not os.path.isfile(avatar_path) or not os.path.getsize(avatar_path):  # load default image
            avatar_path = curr_directory() + '/images/avatar.png'
        width = self._widget.avatar_label.width()
        pixmap = QtGui.QPixmap(avatar_path)
        self._widget.avatar_label.setPixmap(pixmap.scaled(width, width, QtCore.Qt.KeepAspectRatio,
                                                          QtCore.Qt.SmoothTransformation))
        self._widget.avatar_label.repaint()

    def reset_avatar(self):
        avatar_path = (ProfileHelper.get_path() + 'avatars/{}.png').format(self._tox_id[:TOX_PUBLIC_KEY_SIZE * 2])
        if os.path.isfile(avatar_path):
            os.remove(avatar_path)
            self.load_avatar()

    def set_avatar(self, avatar):
        avatar_path = (ProfileHelper.get_path() + 'avatars/{}.png').format(self._tox_id[:TOX_PUBLIC_KEY_SIZE * 2])
        with open(avatar_path, 'wb') as f:
            f.write(avatar)
        self.load_avatar()

    def get_pixmap(self):
        return self._widget.avatar_label.pixmap()

    # -----------------------------------------------------------------------------------------------------------------
    # Widgets
    # -----------------------------------------------------------------------------------------------------------------

    def init_widget(self):
        if self._widget is not None:
            self._widget.name.setText(self._name)
            self._widget.status_message.setText(self._status_message)
            self._widget.connection_status.update(self._status)
            self.load_avatar()
