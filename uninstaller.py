from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget, QMessageBox
import os
import sys
import shutil
import subprocess

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
        self.uninstallButton.clicked.connect(self.confirmUninstallation)
        self.layout.addWidget(self.uninstallButton)

        self.closeButton = QPushButton("Close")
        self.closeButton.clicked.connect(self.closeApplication)
        self.layout.addWidget(self.closeButton)

    def confirmUninstallation(self):
        if self.isAppRunning("wincuts.exe"):
            reply = QMessageBox.question(self, 'Application is running',
                                         "Wincuts is still running. It must be closed before uninstallation can proceed. Do you want to close it now?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.terminateApp("wincuts.exe")  # close the app
            else:
                self.infoText.append("Please close Wincuts manually before proceeding.")
                return

        reply = QMessageBox.question(self, 'Confirmation',
                                     "Are you sure you want to uninstall Wincuts? This action cannot be undone.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.startUninstallation()
        else:
            self.infoText.append("Uninstallation cancelled.")

    def isAppRunning(self, process_name):
        try:
            output = subprocess.check_output(f"tasklist | findstr /I {process_name}", shell=True)
            if process_name in str(output):
                return True
        except subprocess.CalledProcessError:
            return False
        return False

    def terminateApp(self, process_name):
        try:
            subprocess.check_output(f"taskkill /im {process_name} /f", shell=True)
            self.infoText.append(f"{process_name} has been closed.")
        except subprocess.CalledProcessError as e:
            self.infoText.append(f"Failed to close {process_name}. Please close it manually.")

    def startUninstallation(self):
        self.uninstallButton.setEnabled(False)
        self.infoText.append("Starting uninstallation...")

        # Set the folder path
        folder_path = os.path.dirname(os.path.abspath(sys.argv[0]))

        # Remove the folder and its contents
        self.removeFolder(folder_path)

        self.infoText.append("Uninstallation completed. Please close the uninstaller.")

    def removeFolder(self, folder_path):
        try:
            shutil.rmtree(folder_path)
            self.infoText.append(f"Removed folder and all its contents: {folder_path}")
        except Exception as e:
            self.infoText.append(f"Error removing folder {folder_path}: {e}")

    def closeApplication(self):
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UninstallerWindow()
    window.show()
    sys.exit(app.exec_())
