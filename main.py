import sys
import csv
from PySide2.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QMessageBox, QVBoxLayout, QWidget
from PySide2.QtGui import QIcon
from keyboard import add_hotkey, wait
from threading import Thread
import datetime

class ShortcutManager:
    def __init__(self):
        self.shortcuts = []

    def load_shortcuts(self, file_name):
        try:
            with open(file_name, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.shortcuts.append(row)
        except FileNotFoundError:
            pass

    def save_shortcuts(self, file_name):
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.shortcuts)

    def add_shortcut(self, keys, command):
        self.shortcuts.append([keys, command])

    def delete_shortcut(self, index):
        del self.shortcuts[index]

class ShortcutEditor(QWidget):
    def __init__(self, shortcut_manager):
        super().__init__()
        self.shortcut_manager = shortcut_manager
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Shortcut Editor")
        self.setGeometry(100, 100, 400, 300)

        self.label_keys = QLabel("Keys:")
        self.lineedit_keys = QLineEdit()
        self.label_command = QLabel("Command:")
        self.lineedit_command = QLineEdit()
        self.button_set_shortcut = QPushButton("Set Shortcut")
        self.button_set_shortcut.clicked.connect(self.set_shortcut)

        self.listwidget_shortcuts = QListWidget()
        self.listwidget_shortcuts.setSelectionMode(QListWidget.SingleSelection)
        self.button_delete_shortcut = QPushButton("Delete Shortcut")
        self.button_delete_shortcut.clicked.connect(self.delete_shortcut)

        layout = QVBoxLayout()
        layout.addWidget(self.label_keys)
        layout.addWidget(self.lineedit_keys)
        layout.addWidget(self.label_command)
        layout.addWidget(self.lineedit_command)
        layout.addWidget(self.button_set_shortcut)
        layout.addWidget(self.listwidget_shortcuts)
        layout.addWidget(self.button_delete_shortcut)

        self.setLayout(layout)

    def set_shortcut(self):
        keys = self.lineedit_keys.text()
        command = self.lineedit_command.text()
        if keys.strip() == "" or command.strip() == "":
            QMessageBox.critical(self, "Error", "Please enter keys and command.")
            return

        # Add the shortcut
        self.shortcut_manager.add_shortcut(keys, command)
        self.list_shortcuts()

    def delete_shortcut(self):
        selected_item = self.listwidget_shortcuts.currentItem()
        if selected_item:
            index = self.listwidget_shortcuts.row(selected_item)
            self.shortcut_manager.delete_shortcut(index)
            self.list_shortcuts()

    def list_shortcuts(self):
        self.listwidget_shortcuts.clear()
        for keys, command in self.shortcut_manager.shortcuts:
            item = QListWidgetItem(f"{keys} -> {command}")
            self.listwidget_shortcuts.addItem(item)

class MainWindow(QMainWindow):
    def __init__(self, shortcut_manager):
        super().__init__()
        self.shortcut_manager = shortcut_manager
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Shortcut Manager")
        self.setGeometry(100, 100, 400, 300)

        # Create a system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("logo.png"))  # Set your own icon

        # Create a menu for the system tray icon
        tray_menu = QMenu()

        open_action = QAction("Open", self)
        quit_action = QAction("Quit", self)

        open_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.quit)

        tray_menu.addAction(open_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Set up shortcut editor
        self.shortcut_editor = ShortcutEditor(self.shortcut_manager)
        self.setCentralWidget(self.shortcut_editor)

        # Load shortcuts
        self.shortcut_manager.load_shortcuts("validated.dat")

        # Start listening for shortcuts
        self.listen_shortcuts()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def quit(self):
        self.shortcut_manager.save_shortcuts("validated.dat")
        QApplication.quit()

    def execute_command(self, command):
        green_ansi = "\u001b[32m"
        reset_ansi = "\u001b[0m"
        # [ DATETIME ] Executing command: [ COMMAND ]
        print(f"{green_ansi}[{datetime.datetime.now()}]{reset_ansi} Executing command: {command}")

    def listen_shortcuts(self):
        for keys, command in self.shortcut_manager.shortcuts:
            add_hotkey(keys, lambda: self.execute_command(command))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    shortcut_manager = ShortcutManager()
    window = MainWindow(shortcut_manager)
    window.show()
    sys.exit(app.exec_())
