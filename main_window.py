import sys, os, glob

from PyQt5.QtCore import Qt, QUrl, QDir
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QTableWidgetItem

# change from file
from Ui_main_pages import Ui_MainWindow
from Cartoon_character import Cartoon


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        # mimeData = QMimeData()

        self.image_name = ''
        self.video_name = ''
        self.isImageMatchedVideo = False

        # start first page
        # self.ui.stackedWidget.setCurrentWidget(self.ui.start_page)
        self.ui.stackedWidget.setCurrentWidget(self.ui.insert_page)

        # set switch button pages
        self.ui.btn_startApp.clicked.connect(self.showInsertPage)
        self.ui.btn_insertAnotherImage1.clicked.connect(self.showInsertPage)
        self.ui.btn_insertAnotherImage2.clicked.connect(self.showInsertPage)

        # # ======= initiate button connection ==================================
        self.ui.btn_confirmImageVideo.clicked.connect(self.showMatchPage)
        self.ui.btn_chooseImage.clicked.connect(self.chooseImage)
        self.ui.btn_chooseVideo.clicked.connect(self.chooseVideo)
        self.ui.pushButton_foundPage.clicked.connect(self.showFoundPage)
        self.ui.pushButton_notFoundPage.clicked.connect(self.showNotFoundPage)

        self.ui.btn_changeImage.clicked.connect(self.changeImage_clicked)
        self.ui.btn_changeVIdeo.clicked.connect(self.changeVideo_clicked)

        # not yet functioning
        self.ui.btn_findMatchCharacter.clicked.connect(self.showResultPage)
        # self.ui.pushButton_3.clicked.connect(self.showBlue)

        # drag and drop image
        # self.ui.insertPage_cartoonImage.setPixmap(image)

        # ======= initiate table ==================================
        # change width of column
        self.ui.tableFrameFound.setColumnWidth(0, 280)
        self.ui.tableFrameFound.setColumnWidth(1, 160)
        self.ui.tableFrameFound.setColumnWidth(2, 120)
        #
        # # button openFile =====================================
        self.ui.tableFrameFound.itemDoubleClicked.connect(self.changeFrameFound)

        # ========= initiate cartoon detector ==================
        self.cartoon_image = Cartoon()
        self.cartoon_video = Cartoon()
        # dir = 'images/shin-chan2.jpg'
        # dir = 'images/bean 5 secs.mp4'
        # cartoon.setConfidence(0.6)
        # self.cartoon_image.detectCharacter()

    def load_frame_output_data(self, name_list='h', time_list='h', accuracy_list='b'):
        self.ui.tableFrameFound.setRowCount(len(name_list))

        row = 0
        for file in name_list:
            self.ui.tableFrameFound.setItem(row, 0, QTableWidgetItem(file))
            row = row + 1

        row = 0
        for time in time_list:
            self.ui.tableFrameFound.setItem(row, 1, QTableWidgetItem(time))
            row = row + 1

        row = 0
        for accuracy in accuracy_list:
            self.ui.tableFrameFound.setItem(row, 2, QTableWidgetItem(accuracy))
            row = row + 1

    # =================== show pages ========================
    def show(self):
        self.main_win.show()

    def showInsertPage(self):
        self.ui.insertPage_cartoonImage.setText('         Choose an image to search')
        self.ui.insertPage_cartoonVideo.setText('            Choose a video to search')
        self.image_name = ''
        self.video_name = ''
        self.ui.stackedWidget.setCurrentWidget(self.ui.insert_page)

    def showMatchPage(self):
        try:
            if self.image_name != '':
                self.ui.matchPage_inputImage.setPixmap(QPixmap(self.image_name))
                self.cartoon_image.setFileName(self.image_name)

                if self.video_name != '':
                    self.ui.matchPage_inputVideo.setPixmap(QPixmap(self.firstFrameName))

                    self.cartoon_image.detectCharacter()
                    self.ui.text_2.setPlainText(str(self.cartoon_image.isFound))
                    self.ui.stackedWidget.setCurrentWidget(self.ui.match_page)

                else:
                    # when no file selected
                    self.showPopupError('No Video!', "Please choose a Video")
            else:
                # when no file selected
                self.showPopupError('No Image!', "Please choose an Image")

        except:
            self.showPopupError('No Image or Video!', "Please choose Image and Video")



    def showResultPage(self):
        if self.cartoon_image.isFound:

            # get character name from image
            # run detect video
            # assign true to self.isImageMatchedVideo = True
            # pass list = load data
            self.cartoon_video.setFileName(self.video_name)
            self.cartoon_video.detectCharacter()
            # get name and compare video and image

            self.load_frame_output_data(self.cartoon_video.fileNames, self.cartoon_video.timestamps,
                                        self.cartoon_video.frame_accuracies)
            self.showFoundPage()
        else:
            self.showNotFoundPage()

    def showNotFoundPage(self):
        self.ui.label_inputImage1.setPixmap(QPixmap(self.image_name))
        self.ui.stackedWidget.setCurrentWidget(self.ui.not_found_page)

    def showFoundPage(self):
        output_image_name = 'output_image.png'

        self.ui.inputImage_found.setPixmap(QPixmap(output_image_name))
        self.ui.frameFound.setText('Double click on Data to change Frame')
        self.ui.label_frameTitle.setText('Frame Time : -' + '\nAccuracy : -')
        self.ui.label_characterName.setText(self.cartoon_image.getCharacterName())
        self.ui.label_accuracy.setText('Accuracy : ' + self.cartoon_image.accuracy_image)
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
        self.image_name = fname[0]
        self.ui.insertPage_cartoonImage.setPixmap(QPixmap(self.image_name))

    def chooseVideo(self):
        fname = QFileDialog.getOpenFileName(self.ui.insert_page, 'Open file',
                                            'c:\\Users\\Asus\\Pictures\\cartoon character',
                                            "Video files (*.mp4 *.avi)")
        self.video_name = fname[0]

        try:
            self.firstFrameName = self.cartoon_video.getFirstFrame(self.video_name)
            self.ui.insertPage_cartoonVideo.setPixmap(QPixmap(self.firstFrameName))
        except:
            self.ui.insertPage_cartoonVideo.setText(' ')
            print('[ERROR] - Cant read video file')

    def changeFrameFound(self):
        row = self.ui.tableFrameFound.currentRow()
        item = self.ui.tableFrameFound.item(row, 0).text()
        time = self.ui.tableFrameFound.item(row, 1).text()
        acc = self.ui.tableFrameFound.item(row, 2).text()
        self.ui.label_frameTitle.setText('Frame Time : ' + time + '\nAccuracy : ' + acc)
        self.setFrameFound(item)

    def runFile(self, fileName):
        try:
            os.startfile(fileName)
        except:
            print('[ERROR] File Not Found')

    def setFrameFound(self, fileName):
        img_ext = ["jpg", "jpeg", "png", "bmp"]
        ext = fileName.split('.')[-1]
        if ext in img_ext and os.path.exists(fileName):
            self.ui.frameFound.setPixmap(QPixmap(fileName))
        else:
            self.showPopupError('Not an image', 'File not found or \nFile open should be in *.png, *jpeg, *jpg')

    def changeImage_clicked(self):
        self.ui.insertPage_cartoonImage.setText('         Choose an image to search')
        self.image_name = ''
        self.ui.stackedWidget.setCurrentWidget(self.ui.insert_page)

    def changeVideo_clicked(self):
        self.ui.insertPage_cartoonVideo.setText('            Choose a video to search')
        self.video_name = ''
        self.ui.stackedWidget.setCurrentWidget(self.ui.insert_page)

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

# activate activate ccir_environment
# python.exe main_window.py

# to import env from yml file
# conda env create -f ccir_env.yml
# to export env to yml file
# conda env export > ccir_env.yml

# to compile
# pyinstaller.exe --onefile Pages_colour.py
# pyinstaller.exe --onefile -w --icon=vip-icon.ico main_window.py
# pyinstaller.exe --onefile -w main_window.py

# to convert ui to py
# pyuic5 UI_ccir.ui -o Ui_main_pages.py

