import sys
import csv
import datetime
import subprocess
import argparse
from PySide2.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QMessageBox, QVBoxLayout, QWidget, QCheckBox, QHBoxLayout
from PySide2.QtGui import QIcon
from keyboard import add_hotkey, remove_hotkey
import ctypes

appid = 'lyubomirt.wincuts.base.v1.0.0'  # Arbitrary
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

class ShortcutManager:
    def __init__(self):
        self.shortcuts = []

    def load_shortcuts(self, file_name):
        try:
            with open(file_name, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    keys, command, open_in_window_str = row
                    open_in_window = open_in_window_str.lower() == 'true'
                    self.shortcuts.append([keys, command, open_in_window])
        except FileNotFoundError:
            pass

    def save_shortcuts(self, file_name):
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.shortcuts)

    def add_shortcut(self, keys, command, open_in_window):
        self.shortcuts.append([keys, command, open_in_window])
        self.save_shortcuts("validated.dat")  # Save shortcuts after adding

    def delete_shortcut(self, index):
        del self.shortcuts[index]
        self.save_shortcuts("validated.dat")  # Save shortcuts after deleting

class ShortcutEditor(QWidget):
    def __init__(self, shortcut_manager, main_window):
        super().__init__()
        self.shortcut_manager = shortcut_manager
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Shortcut Editor")
        self.setMinimumSize(400, 300)  # Minimum size restriction
        self.resize(600, 400)  # Default size

        self.label_keys = QLabel("Keys:")
        self.lineedit_keys = QLineEdit()
        self.label_command = QLabel("Command:")
        self.lineedit_command = QLineEdit()
        self.label_open_in_window = QLabel("Window Patch (experimental):")
        self.checkbox_open_in_window = QCheckBox()

        # Horizontal layout for the checkbox and label
        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(self.label_open_in_window)
        checkbox_layout.addWidget(self.checkbox_open_in_window)
        checkbox_layout.addStretch()

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
        layout.addLayout(checkbox_layout)  # Adding the horizontal layout
        layout.addWidget(self.button_set_shortcut)
        layout.addWidget(self.listwidget_shortcuts)
        layout.addWidget(self.button_delete_shortcut)

        self.setLayout(layout)

    def set_shortcut(self):
        keys = self.lineedit_keys.text()
        command = self.lineedit_command.text()
        open_in_window = self.checkbox_open_in_window.isChecked()
        if keys.strip() == "" or command.strip() == "":
            QMessageBox.critical(self, "Error", "Please enter keys and command.")
            return
        # Make sure the shortcut is not already in use
        for k, c, _ in self.shortcut_manager.shortcuts:
            if k == keys:
                QMessageBox.critical(self, "Error", "Shortcut already in use.")
                return
        
        # Make sure the shortcut format is valid
        try:
            add_hotkey(keys, lambda: None)  # Try to add the hotkey
            remove_hotkey(keys)  # Remove the hotkey
        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid shortcut format. You need to write correct key names separated by '+' without spaces.\nExample: Ctrl+Shift+T")
            return
        except KeyError:
            pass  # No need to remove the hotkey if it wasn't added

        # Add the shortcut
        self.shortcut_manager.add_shortcut(keys, command, open_in_window)
        self.main_window.listen_shortcut(keys, command, open_in_window)  # Listen to the new shortcut
        self.list_shortcuts()

    def delete_shortcut(self):
        selected_item = self.listwidget_shortcuts.currentItem()
        if selected_item:
            index = self.listwidget_shortcuts.row(selected_item)
            keys, command, open_in_window = self.shortcut_manager.shortcuts[index]
            remove_hotkey(keys)  # Stop tracking the deleted shortcut
            self.shortcut_manager.delete_shortcut(index)
            self.list_shortcuts()


    def list_shortcuts(self):
        self.listwidget_shortcuts.clear()
        for keys, command, open_in_window in self.shortcut_manager.shortcuts:
            item = QListWidgetItem(f"{keys} -> {command} {'[WindowPatch]' if open_in_window else ''}")
            self.listwidget_shortcuts.addItem(item)


class MainWindow(QMainWindow):
    def __init__(self, shortcut_manager):
        super().__init__()
        self.shortcut_manager = shortcut_manager
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Shortcut Manager")
        self.setMinimumSize(400, 300)  # Minimum size restriction
        self.resize(400, 300)  # Default size
        self.setWindowIcon(QIcon("logo.png"))

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
        self.shortcut_editor = ShortcutEditor(self.shortcut_manager, self)
        self.setCentralWidget(self.shortcut_editor)

        # Load shortcuts
        self.shortcut_manager.load_shortcuts("validated.dat")
        self.shortcut_editor.list_shortcuts()  # Ensure shortcuts are listed

        # Start listening for shortcuts
        self.listen_shortcuts()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def quit(self):
        QApplication.quit()

    def execute_command(self, command, open_in_window):
        green_ansi = "\u001b[32m"
        reset_ansi = "\u001b[0m"
        # [ DATETIME ] Executing command: [ COMMAND ]
        print(f"{green_ansi}[{datetime.datetime.now()}]{reset_ansi} Executing command: {command}")
        # Execute the command here
        if open_in_window:
            subprocess.call('start ' + command, shell=True)
        else:
            subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def listen_shortcuts(self):
        for keys, command, open_in_window in self.shortcut_manager.shortcuts:
            add_hotkey(keys, self.get_execute_command_function(command, open_in_window))

    def listen_shortcut(self, keys, command, open_in_window):
        try:
            remove_hotkey(keys)  # Remove old hotkey binding if exists
        except KeyError:
            pass
        add_hotkey(keys, self.get_execute_command_function(command, open_in_window))

    def get_execute_command_function(self, command, open_in_window):
        def execute():
            self.execute_command(command, open_in_window)
        return execute

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Shortcut Manager')
    parser.add_argument('-litr', action='store_true', help='Start the app in tray mode')
    args = parser.parse_args()

    app = QApplication(sys.argv)
    shortcut_manager = ShortcutManager()
    window = MainWindow(shortcut_manager)
    window.show()

    if args.litr:
        window.hide()  # Hide the window if started in tray mode

    sys.exit(app.exec_())
