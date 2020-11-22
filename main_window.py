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
        self.ui.btn_matchCharacter.clicked.connect(self.showResultPage)
        # self.ui.pushButton_3.clicked.connect(self.showBlue)

        # drag and drop image
        # self.ui.cartoon_image.setPixmap(image)

        # ======= initiate table ==============
        # change width of column
        self.ui.tableFrameFound.setColumnWidth(0, 280)
        self.ui.tableFrameFound.setColumnWidth(1, 160)
        self.ui.tableFrameFound.setColumnWidth(2, 120)
        #
        # # button openFile =====================================
        self.ui.tableFrameFound.itemDoubleClicked.connect(self.changeFrameFound)

        # ========= initiate cartoon detector ==================
        self.cartoon_image = Cartoon()
        # dir = 'images/shin-chan2.jpg'
        # dir = 'images/bean 5 secs.mp4'
        # cartoon.setConfidence(0.6)
        # self.cartoon_image.detectCharacter()

    def loadData(self):
        people = [{'name': 'images\\title we bare bear.png', 'age': 45, 'address': 'NY', },
                  {'name': 'Mark', 'age': 41, 'address': 'ENG', },
                  {'name': 'output_video.mp4', 'age': 45, 'address': 'NY', },
                  {'name': 'images\\shin-chan2.jpg', 'age': 41, 'address': 'ENG', },
                  {'name': 'John', 'age': 45, 'address': 'NY', }, {'name': 'Mark', 'age': 41, 'address': 'ENG', },
                  {'name': 'John', 'age': 45, 'address': 'NY', }, {'name': 'Mark', 'age': 41, 'address': 'ENG', },
                  {'name': 'John', 'age': 45, 'address': 'NY', }, {'name': 'Mark', 'age': 41, 'address': 'ENG', }
                  ]

        self.ui.tableFrameFound.clear()
        row = 0
        self.ui.tableFrameFound.setRowCount(len(people))

        print(type(people))

        for person in people:
            self.ui.tableFrameFound.setItem(row, 0, QTableWidgetItem(person['name']))
            self.ui.tableFrameFound.setItem(row, 1, QTableWidgetItem(str(person['age'])))  # number change to str like print
            # self.ui.table1.setItem(row, 2, QTableWidgetItem(person['address']))
            row = row + 1

    def load_frame_output_data(self, name_list='h', time_list='h'):
        print('hai')
        print(name_list + time_list)

        times = ['1.000 sec', '1.033 sec', '1.066 sec', '1.100 sec', '1.133 sec', '1.166 sec', '1.200 sec', '1.233 sec',
                 '1.266 sec', '1.300 sec', '1.333 sec', '1.366 sec', '1.400 sec', '1.433 sec', '1.466 sec', '1.500 sec',
                 '1.533 sec', '1.666 sec', '1.700 sec', '1.733 sec', '1.766 sec', '1.800 sec', '1.833 sec', '1.866 sec',
                 '1.900 sec', '1.933 sec', '1.966 sec', '2.000 sec', '2.033 sec', '2.066 sec', '2.100 sec', '2.133 sec',
                 '2.166 sec', '2.200 sec', '2.233 sec', '2.266 sec', '2.300 sec', '2.333 sec', '2.366 sec', '2.400 sec',
                 '2.433 sec', '2.466 sec', '2.500 sec', '2.533 sec', '2.566 sec', '2.600 sec', '2.633 sec', '2.666 sec',
                 '2.700 sec', '2.733 sec', '2.766 sec', '2.800 sec', '2.833 sec', '2.866 sec', '2.900 sec', '2.933 sec',
                 '2.966 sec', '3.000 sec', '3.033 sec', '3.066 sec', '3.100 sec', '3.133 sec', '3.166 sec', '3.200 sec',
                 '3.233 sec', '3.266 sec', '3.300 sec', '3.333 sec', '3.366 sec', '3.400 sec', '3.433 sec', '3.466 sec',
                 '3.500 sec', '3.699 sec', '3.733 sec']
        accuracies = ['10.19%', '1.033 sec', '1 sec', '1 sec', '1.133 sec', '1.166 sec', '1.200 sec', '1.233 sec',
                 '1.266 sec', '1.300 sec', '1.333 sec', '1.366 sec', '1.400 sec', '1.433 sec', '1.466 sec', '1.500 sec',
                 '1.533 sec', '1.666 sec', '1.700 sec', '1.733 sec', '1.766 sec', '1.800 sec', '1.833 sec', '1.866 sec',
                 '1.900 sec', '1.933 sec', '1.966 sec', '2.000 sec', '2.033 sec', '2.066 sec', '2.100 sec', '2.133 sec',
                 '2.166 sec', '2.200 sec', '2.233 sec', '2.266 sec', '2.300 sec', '2.333 sec', '2.366 sec', '2.400 sec',
                 '2.433 sec', '2.466 sec', '2.500 sec', '2.533 sec', '2.566 sec', '2.600 sec', '2.633 sec', '2.666 sec',
                 '2.700 sec', '2.733 sec', '2.766 sec', '2.800 sec', '2.833 sec', '2.866 sec', '2.900 sec', '2.933 sec',
                 '2.966 sec', '3.000 sec', '3.033 sec', '3.066 sec', '3.100 sec', '3.133 sec', '3.166 sec', '3.200 sec',
                 '3.233 sec', '3.266 sec', '3.300 sec', '3.333 sec', '3.366 sec', '3.400 sec', '3.433 sec', '3.466 sec',
                 '3.500 sec', '3.699 sec', '3.733 sec']
        files = ['output\\output_bean00031.png', 'output\\output_bean00032.png', 'output\\output_bean00033.png',
                 'images\\shin-chan2.jpg', 'images\\title we bare bear.png', 'output\\output_bean00036.png',
                 'images\\title we bare bear.png', 'output\\output_bean00038.png', 'output\\output_bean00039.png',
                 'output\\output_bean00040.png', 'output\\output_bean00041.png', 'output\\output_bean00042.png',
                 'output\\output_bean00043.png', 'output\\output_bean00044.png', 'output\\output_bean00045.png',
                 'output\\output_bean00046.png', 'output\\output_bean00047.png', 'output\\output_bean00051.png',
                 'output\\output_bean00052.png', 'output\\output_bean00053.png', 'output\\output_bean00054.png',
                 'output\\output_bean00055.png', 'output\\output_bean00056.png', 'output\\output_bean00057.png',
                 'output\\output_bean00058.png', 'output\\output_bean00059.png', 'output\\output_bean00060.png',
                 'output\\output_bean00061.png', 'output\\output_bean00062.png', 'output\\output_bean00063.png',
                 'output\\output_bean00064.png', 'output\\output_bean00065.png', 'output\\output_bean00066.png',
                 'output\\output_bean00067.png', 'output\\output_bean00068.png', 'output\\output_bean00069.png',
                 'output\\output_bean00070.png', 'output\\output_bean00071.png', 'output\\output_bean00072.png',
                 'output\\output_bean00073.png', 'output\\output_bean00074.png', 'output\\output_bean00075.png',
                 'output\\output_bean00076.png', 'output\\output_bean00077.png', 'output\\output_bean00078.png',
                 'output\\output_bean00079.png', 'output\\output_bean00080.png', 'output\\output_bean00081.png',
                 'output\\output_bean00082.png', 'output\\output_bean00083.png', 'output\\output_bean00084.png',
                 'output\\output_bean00085.png', 'output\\output_bean00086.png', 'output\\output_bean00087.png',
                 'output\\output_bean00088.png', 'output\\output_bean00089.png', 'output\\output_bean00090.png',
                 'output\\output_bean00091.png', 'output\\output_bean00092.png', 'output\\output_bean00093.png',
                 'output\\output_bean00094.png', 'output\\output_bean00095.png', 'output\\output_bean00096.png',
                 'output\\output_bean00097.png', 'output\\output_bean00098.png', 'output\\output_bean00099.png',
                 'output\\output_bean00100.png', 'output\\output_bean00101.png', 'output\\output_bean00102.png',
                 'output\\output_bean00103.png', 'output\\output_bean00104.png', 'output\\output_bean00105.png',
                 'output\\output_bean00106.png', 'output\\output_bean00112.png', 'output\\output_bean00113.png']

        self.ui.tableFrameFound.setRowCount(len(files))

        row = 0
        for file in files:
            self.ui.tableFrameFound.setItem(row, 0, QTableWidgetItem(file))
            row = row + 1

        row = 0
        for time in times:
            self.ui.tableFrameFound.setItem(row, 1, QTableWidgetItem(time))
            row = row + 1

        row = 0
        for accuracy in accuracies:
            self.ui.tableFrameFound.setItem(row, 2, QTableWidgetItem(accuracy))
            row = row + 1

    # =================== show pages ========================
    def show(self):
        self.main_win.show()

    def showInsertPage(self):
        self.ui.cartoon_image.setText('         Choose an image to search')
        self.image_name = ''
        self.ui.stackedWidget.setCurrentWidget(self.ui.insert_page)

    def showMatchPage(self):
        try:
            if self.image_name != '':
                self.ui.match_page_image.setPixmap(QPixmap(self.image_name))
                self.cartoon_image.setFileName(self.image_name)
                self.cartoon_image.detectCharacter()
                self.ui.text_2.setPlainText(str(self.cartoon_image.isFound))
                self.ui.stackedWidget.setCurrentWidget(self.ui.match_page)
            else:
                # when no file selected
                self.showPopupError('No Image!', "Please choose an Image")

        except:
            # when no file selected
            self.showPopupError('No Image!', "Please choose an Image")

    def showResultPage(self):
        if self.cartoon_image.isFound:
            self.showFoundPage()
        else:
            self.showNotFoundPage()

    def showNotFoundPage(self):
        self.ui.label_inputImage1.setPixmap(QPixmap(self.image_name))
        self.ui.stackedWidget.setCurrentWidget(self.ui.not_found_page)

    def showFoundPage(self):
        output_image_name = 'output_image.png'
        self.load_frame_output_data('jk', 'r')  # get timestamps and fileNames
        self.ui.inputImage_found.setPixmap(QPixmap(output_image_name))
        self.ui.label_characterName.setText(self.cartoon_image.getCharacterName())
        self.ui.label_accuracy.setText(self.cartoon_image.accuracy_image)
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
        self.ui.cartoon_image.setPixmap(QPixmap(self.image_name))

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
