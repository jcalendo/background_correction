import sys
import os

from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QFrame,
                             QGridLayout, QInputDialog, QLabel, QPushButton)
from PyQt5.QtCore import pyqtSlot

import CorrectBackground


class Dialog(QDialog):

    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)

        frameStyle = QFrame.Sunken | QFrame.Panel

        self.brightLabel = QLabel()
        self.brightLabel.setFrameStyle(frameStyle)
        self.brightButton = QPushButton("select BRIGHTFIELD image")

        self.darkLabel = QLabel()
        self.darkLabel.setFrameStyle(frameStyle)
        self.darkButton = QPushButton("select DARKFIELD image")

        self.directoryLabel = QLabel()
        self.directoryLabel.setFrameStyle(frameStyle)
        self.directoryButton = QPushButton("Select images to be corrected")

        self.runButtonLabel = QLabel()
        self.runButtonLabel.setFrameStyle(frameStyle)
        self.runButton = QPushButton("Run Illumination Correction")

        self.brightButton.clicked.connect(self.setBrightFile)
        self.darkButton.clicked.connect(self.setDarkFile)
        self.directoryButton.clicked.connect(self.setExistingDirectory)
        self.runButton.clicked.connect(self.process_directory)

        layout = QGridLayout()
        layout.setColumnStretch(1, 1)
        layout.setColumnMinimumWidth(1, 250)

        layout.addWidget(self.brightButton, 1, 0)
        layout.addWidget(self.brightLabel, 1, 1)

        layout.addWidget(self.darkButton, 2, 0)
        layout.addWidget(self.darkLabel, 2, 1)

        layout.addWidget(self.directoryButton, 3, 0)
        layout.addWidget(self.directoryLabel, 3, 1)

        layout.addWidget(self.runButton, 4, 0)
        layout.addWidget(self.runButtonLabel, 4, 1)

        self.setLayout(layout)

        self.setWindowTitle("Background Correction")

        self.bright_file = []
        self.dark_file = []
        self.img_dir = []

    def setBrightFile(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Select Brightfield Image",
                                                  r"D:\My Pictures", 
                                                  ("Image Files (*.png *.jpg *.tif *.bmp)"),
                                                  options=options)

        if fileName:
            self.brightLabel.setText(fileName)
            self.bright_file.append(fileName)

    def setDarkFile(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Select Darkfield image", 
                                                  r"D:\My Pictures", 
                                                  ("Image Files (*.png *.jpg *.tif *.bmp)"), 
                                                  options=options)

        if fileName:
            self.darkLabel.setText(fileName)
            self.dark_file.append(fileName)

    def setExistingDirectory(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,
                                                     "Select Specimen Image Directory",
                                                      self.directoryLabel.text(), 
                                                      options=options)
        if directory:
            self.directoryLabel.setText(directory)
            self.img_dir.append(directory)

    def process_directory(self):
        self.runButtonLabel.setText("Correction Complete")

        input_dir = self.img_dir[-1]

        if not os.path.exists(os.path.join(input_dir, "corrected_images")):
            os.makedirs(os.path.join(input_dir, "corrected_images"))

        output_dir = os.path.join(input_dir, "corrected_images")

        bright_img = self.bright_file[-1]
        dark_img = self.dark_file[-1]

        CorrectBackground.process_folder(input_dir, bright_img, dark_img, output_dir)

        print("\nIllumination Correction Complete")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    print("This program was written by Gennaro Calendo\n")
    print("Please select a brightfield image file and a darkfield image file. Then select the directory of the images to be corrected.")
    print("After making your selection, click 'Run Illimunation Correction'.\n")
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec_())
