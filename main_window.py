import sys, os, glob

from PyQt5.QtCore import Qt, QUrl, QDir
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QStyle, QAction, QMessageBox

# change from file
from Ui_main_pages import Ui_MainWindow


class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        # self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        # self.setStyleSheet('''
        #     QLabel{
        #         border: 4px dashed #aaa
        #     }
        # ''')

    def setPixmap(self, image):
        super().setPixmap(image)


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        # mimeData = QMimeData()

        # start first page
        # self.ui.stackedWidget.setCurrentWidget(self.ui.start_page)
        self.ui.stackedWidget.setCurrentWidget(self.ui.insert_page)

        # set switch button pages
        self.ui.btn_startApp.clicked.connect(self.showInsertPage)
        self.ui.btn_insertAnotherImage1.clicked.connect(self.showInsertPage)
        self.ui.btn_insertAnotherImage2.clicked.connect(self.showInsertPage)
        self.ui.btn_changeImage.clicked.connect(self.showInsertPage)

        self.ui.btn_confirmImage.clicked.connect(self.showMatchPage)
        self.ui.btn_chooseImage.clicked.connect(self.chooseImage)
        # self.ui.btn_insertImage.clicked.connect(self.showMatchPage)
        self.ui.pushButton_foundPage.clicked.connect(self.showFoundPage)
        self.ui.pushButton_notFoundPage.clicked.connect(self.showNotFoundPage)

        # not yet functioning
        self.ui.btn_matchCharacter.clicked.connect(self.show)
        # self.ui.pushButton_3.clicked.connect(self.showBlue)

        # drag and drop image
        # self.ui.cartoon_image.setPixmap(image)

    # =================== show pages ========================
    def show(self):
        self.main_win.show()

    def showInsertPage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.insert_page)

    def showMatchPage(self):

        try:
            if self.image_name != '':
                self.ui.match_page_image.setPixmap(QPixmap(self.image_name))
                self.ui.stackedWidget.setCurrentWidget(self.ui.match_page)

            else:
                # when no file selected
                print('null')

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setText("This is a message box")
                msg.setInformativeText("This is additional information")
                msg.setWindowTitle("MessageBox demo")
                msg.setDetailedText("The details are as follows:")

                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                # msg.buttonClicked.connect(msgbtn)
                # retval = msg.exec_()
                # print"value of pressed message box button:", retval

        except:

            # when no file selected
            print('no type str')

    def chooseImage(self):
        fname = QFileDialog.getOpenFileName(self.ui.insert_page, 'Open file',
                                            'c:\\', "Image files (*.jpg *.png *.jpeg)")
        # print(fname[0].title())
        # print(type(fname[0]))
        self.image_name = fname[0]
        # self.characterName = 'Boruto'
        self.characterName = self.ui.text_2.toPlainText()

        self.ui.cartoon_image.setPixmap(QPixmap(self.image_name))

    def showNotFoundPage(self):
        self.ui.label_inputImage1.setPixmap(QPixmap(self.image_name))
        self.ui.stackedWidget.setCurrentWidget(self.ui.not_found_page)

    def showFoundPage(self):
        self.ui.label_characterName.setText(self.characterName)
        # self.ui.label_16.setText(self.character_name)

        self.ui.label_inputImage2.setPixmap(QPixmap(self.image_name))
        self.ui.stackedWidget.setCurrentWidget(self.ui.found_page)

    # # =================== play video event ========================
    #
    # def openFile(self):
    #     fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
    #                                               QDir.homePath())
    #
    #     if fileName != '':
    #         self.mediaPlayer.setMedia(
    #             QMediaContent(QUrl.fromLocalFile(fileName)))
    #         self.playButton.setEnabled(True)
    #
    # def play(self):
    #     if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
    #         self.mediaPlayer.pause()
    #     else:
    #         self.mediaPlayer.play()
    #
    # def mediaStateChanged(self, state):
    #     if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
    #         self.playButton.setIcon(
    #             self.style().standardIcon(QStyle.SP_MediaPause))
    #     else:
    #         self.playButton.setIcon(
    #             self.style().standardIcon(QStyle.SP_MediaPlay))
    #
    # def positionChanged(self, position):
    #     self.positionSlider.setValue(position)
    #
    # def durationChanged(self, duration):
    #     self.positionSlider.setRange(0, duration)
    #
    # def setPosition(self, position):
    #     self.mediaPlayer.setPosition(position)
    #
    # def handleError(self):
    #     self.playButton.setEnabled(False)
    #     self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())

# to compile
# pyinstaller.exe --onefile Pages_colour.py

# to convert ui to py
# pyuic5 UI_ccir.ui -o Ui_main_pages.py
