from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget, QMessageBox
import os
import sys
import shutil
import subprocess
import ctypes
import tempfile
class UninstallerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wincuts Uninstaller")
        self.setGeometry(300, 300, 400, 200)
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        self.infoText = QTextEdit()
        self.infoText.setReadOnly(True)
        self.layout.addWidget(self.infoText)

        self.uninstallButton = QPushButton("Uninstall")
        self.uninstallButton.clicked.connect(self.confirm_uninstallation)
        self.layout.addWidget(self.uninstallButton)

        self.closeButton = QPushButton("Close")
        self.closeButton.clicked.connect(self.close_application)
        self.layout.addWidget(self.closeButton)

    def confirm_uninstallation(self):
        # First, show what will be deleted
        folder_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.preview_deletion(folder_path)

        if self.is_app_running("wincuts.exe"):
            reply = QMessageBox.question(self, 'Application is running',
                                         "Wincuts is still running. It must be closed before uninstallation can proceed. Do you want to close it now?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.terminate_app("wincuts.exe")  # close the app
            else:
                self.infoText.append("Please close Wincuts manually before proceeding.")
                return

        reply = QMessageBox.question(self, 'Confirmation',
                                     "Are you sure you want to uninstall Wincuts? This action cannot be undone.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.start_uninstallation()
        else:
            self.infoText.append("Uninstallation cancelled.")

    def is_app_running(self, process_name):
        try:
            output = subprocess.check_output(f"tasklist | findstr /I {process_name}", shell=True)
            if process_name in str(output):
                return True
        except subprocess.CalledProcessError:
            return False
        return False

    def terminate_app(self, process_name):
        try:
            subprocess.check_output(f"taskkill /im {process_name} /f", shell=True)
            self.infoText.append(f"{process_name} has been closed.")
        except subprocess.CalledProcessError as e:
            self.infoText.append(f"Failed to close {process_name}. Please close it manually.")

    def start_uninstallation(self):
        self.uninstallButton.setEnabled(False)
        self.infoText.append("Starting uninstallation...")

        # Set the folder path
        folder_path = os.path.dirname(os.path.abspath(sys.argv[0]))

        # Remove the folder and its contents
        self.removeFolder(folder_path)
        self.schedule_self_deletion()
        # Final message to the user
        self.infoText.append(
            "Uninstallation completed. The uninstaller will be removed upon reboot. Please close the uninstaller.")

    def schedule_self_deletion(self):
        self.infoText.append("yes")
        _MoveFileEx = ctypes.windll.kernel32.MoveFileExW
        _MoveFileEx.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint]
        MOVEFILE_DELAY_UNTIL_REBOOT = 0x4

        # Create the batch script in a temporary directory
        temp_dir = tempfile.gettempdir()
        batch_script_path = os.path.join(temp_dir, "delete_uninstaller.bat")

        with open(batch_script_path, 'w') as bat_file:
            bat_file.write("timeout /t 5\n")
            bat_file.write(f"del /f /q \"{os.path.abspath(__file__)}\"\n")
            bat_file.write(f"del /f /q \"{batch_script_path}\"\n")  # Command to delete the batch script itself
            bat_file.write("exit\n")

        # Schedule the batch script for execution on reboot
        if not _MoveFileEx(batch_script_path, None, MOVEFILE_DELAY_UNTIL_REBOOT):
            error_code = ctypes.GetLastError()
            self.infoText.append(f"Failed to schedule batch script for execution on reboot. Error code: {error_code}")
        else:
            self.infoText.append("Batch script scheduled for execution on reboot to delete the uninstaller.")

    def schedule_file_deletion(self, filepath):
        self.infoText.append("file")
        _MoveFileEx = ctypes.windll.kernel32.MoveFileExW
        _MoveFileEx.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint]
        MOVEFILE_DELAY_UNTIL_REBOOT = 0x4
        if not _MoveFileEx(filepath, None, MOVEFILE_DELAY_UNTIL_REBOOT):
            error_code = ctypes.GetLastError()
            self.infoText.append(f"Failed to schedule {filepath} for deletion on reboot. Error code: {error_code}")
        else:
            self.infoText.append(f"Scheduled {filepath} for deletion on reboot.")

    def removeFolder(self, folder_path):
        uninstaller_path = os.path.abspath(__file__)
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if item_path != uninstaller_path:
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                except Exception as e:
                    self.infoText.append(f"Cannot remove {item_path} immediately, scheduling for deletion on reboot.")
                    self.schedule_file_deletion(item_path)

    def preview_deletion(self, folder_path):
        self.infoText.append("The following files and directories will be deleted:\n")
        uninstaller_path = os.path.abspath(__file__)  # Absolute path of the uninstaller
        for root, dirs, files in os.walk(folder_path, topdown=True):
            for name in files:
                file_path = os.path.join(root, name)
                if file_path != uninstaller_path:  # Skip the uninstaller
                    self.infoText.append(file_path)
            for name in dirs:
                dir_path = os.path.join(root, name) + "\\"  # Adding a backslash to indicate a directory
                self.infoText.append(dir_path)
        self.infoText.append(
            "\nAdditionally, the uninstaller and a temporary batch file used for cleanup will be deleted upon reboot.")
        self.infoText.append("\nReview the list above before proceeding with the uninstallation.")

    def close_application(self):
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UninstallerWindow()
    window.show()
    sys.exit(app.exec_())