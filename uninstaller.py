from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget, QMessageBox
import os
import sys
import shutil

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
        reply = QMessageBox.question(self, 'Confirmation',
                                     "Are you sure you want to uninstall the application? This action cannot be undone.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.startUninstallation()
        else:
            self.infoText.append("Uninstallation cancelled.")

    def startUninstallation(self):
        self.uninstallButton.setEnabled(False)
        self.infoText.append("Starting uninstallation...")

        # set the folder path
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