import sys, os, glob

from PyQt5.QtCore import Qt, QUrl, QDir
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QStyle, QAction, QMessageBox, QTableWidgetItem

# change from file
from Ui_main_pages import Ui_MainWindow
# from Cartoon_character import Cartoon

class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        # mimeData = QMimeData()

        # start first page
        self.ui.stackedWidget.setCurrentWidget(self.ui.start_page)
        # self.ui.stackedWidget.setCurrentWidget(self.ui.found_page)

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

        # ======= initiate table ==============
        # change width of column
        # self.ui.table1.setColumnWidth(0, 420)
        # self.ui.table1.setColumnWidth(1, 150)
        #
        # # button openFile =====================================
        # self.ui.table1.itemDoubleClicked.connect(self.openImage)

        # self.loadData()

    def loadData(self):
        people = [{'name': 'images\\title we bare bear.png', 'age': 45, 'address': 'NY', }, {'name': 'Mark', 'age': 41, 'address': 'ENG', },
                  {'name': 'output_video.mp4', 'age': 45, 'address': 'NY', },
                  {'name': 'images\\shin-chan2.jpg', 'age': 41, 'address': 'ENG', },
                  {'name': 'John', 'age': 45, 'address': 'NY', }, {'name': 'Mark', 'age': 41, 'address': 'ENG', },
                  {'name': 'John', 'age': 45, 'address': 'NY', }, {'name': 'Mark', 'age': 41, 'address': 'ENG', },
                  {'name': 'John', 'age': 45, 'address': 'NY', }, {'name': 'Mark', 'age': 41, 'address': 'ENG', }
                  ]

        row = 0
        self.ui.table1.setRowCount(len(people))

        print(type(people))

        for person in people:
            self.ui.table1.setItem(row, 0, QTableWidgetItem(person['name']))
            self.ui.table1.setItem(row, 1, QTableWidgetItem(str(person['age'])))  # number change to str like print
            # self.ui.table1.setItem(row, 2, QTableWidgetItem(person['address']))
            row = row + 1

    def load_frame_output_data(self, name_list, time_list):
        print('hai')
        # self.ui.table1.setRowCount(len(people))

        # row = 0
        #
        # for person in people:
        #     self.ui.table1.setItem(row, 0, QTableWidgetItem(person['name']))
        #     self.ui.table1.setItem(row, 1, QTableWidgetItem(str(person['age'])))  # number change to str like print
        #     # self.ui.table1.setItem(row, 2, QTableWidgetItem(person['address']))
        #     row = row + 1

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
                self.showPopupError('No Image!', "Please choose an Image")

        except:
            # when no file selected
            self.showPopupError('No Image!', "Please choose an Image")

    def showNotFoundPage(self):
        self.ui.label_inputImage1.setPixmap(QPixmap(self.image_name))
        self.ui.stackedWidget.setCurrentWidget(self.ui.not_found_page)

    def showFoundPage(self):

        # ======= initiate table ==============
        # change width of column
        # self.ui.table1.setColumnWidth(0, 420)
        # self.ui.table1.setColumnWidth(1, 150)
        #
        # # button openFile =====================================
        # self.ui.table1.itemDoubleClicked.connect(self.openImage)
        #
        # self.loadData()
        #
        # self.ui.label_characterName.setText(self.characterName)
        # # self.ui.label_16.setText(self.character_name)
        #
        # self.ui.label_inputImage2.setPixmap(QPixmap(self.image_name))
        self.ui.stackedWidget.setCurrentWidget(self.ui.found_page)

    def showPopupError(self, errorText, errorInfo):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning Popup")
        msg.setText(errorText)
        msg.setInformativeText(errorInfo)
        msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()


    # =================== button function ========================

    # to read image
    def chooseImage(self):
        fname = QFileDialog.getOpenFileName(self.ui.insert_page, 'Open file',
                                            'c:\\Users\\Asus\\Pictures\\cartoon character',
                                            "Image files (*.jpg *.png *.jpeg)")
        # 'c:\\', "Image files (*.jpg *.png *.jpeg)")
        # print(fname[0].title())
        # print(type(fname[0]))
        self.image_name = fname[0]
        self.characterName = 'rename me'
        # self.characterName = self.ui.text_2.toPlainText()

        self.ui.cartoon_image.setPixmap(QPixmap(self.image_name))

    def openImage(self):
        row = self.ui.table1.currentRow()
        item = self.ui.table1.item(row, 0).text()
        # self.runFile(item)
        self.setFrameFound(item)

    def runFile(self, fileName):
        try:
            os.startfile(fileName)
        except:
            print('[ERROR] File Not Found')

    def setFrameFound(self, fileName):
        img_ext = ["jpg", "jpeg", "png", "bmp"]
        ext = fileName.split('.')[-1]
        if ext in img_ext:
            self.ui.frameFound.setPixmap(QPixmap(fileName))
        else:
            self.showPopupError('Not an image', 'File open should be in *.png, *jpeg, *jpg')



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
