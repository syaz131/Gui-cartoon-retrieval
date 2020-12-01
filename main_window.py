import sys, os, glob

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QUrl, QDir
from PyQt5.QtGui import QPixmap, QIcon, QMovie
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QTableWidgetItem, QSlider, QLabel, \
    QSizePolicy, QStyle, QWidget

# change from file
from Ui_main_pages import Ui_MainWindow
from Cartoon_character import Cartoon


# from Loading_window import LoadingScreen

class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 300)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.label_animation = QLabel(self)

        self.movie = QMovie('Loading_2.gif')
        self.label_animation.setMovie(self.movie)
        self.movie.start()

    def startAnimation(self):
        self.movie.start()
        self.show()

    def stopAnimation(self):
        self.close()
        self.movie.stop()


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        # mimeData = QMimeData()

        self.image_name = ''
        self.video_name = ''
        self.isImageMatchedVideo = False
        self.fileExt = ''

        we_bear_ico = 'title we bare bear'
        self.ui.label_ico_bear.setPixmap((QPixmap(we_bear_ico)))

        loadingGif = 'Loading_2.gif'
        self.movie = QMovie(loadingGif)
        self.ui.label_buffer.setMovie(self.movie)
        self.ui.label_videoPlay.setMovie(self.movie)
        # self.ui.label_buffer_insertPage.setMovie(self.movie)
        # self.ui.label_buffer_insertPage.setHidden(True)
        self.movie.start()

        self.videoOutput_name = 'output_video_bean_eg.mp4'
        self.videoPlay_output = QMovie(self.videoOutput_name)
        self.ui.label_videoPlay.setMovie(self.videoPlay_output)
        self.videoPlay_output.setPaused(True)

        # start first page
        self.ui.stackedWidget.setCurrentWidget(self.ui.advanceSearch_page)
        # self.ui.stackedWidget.setCurrentWidget(self.ui.start_page)
        # self.ui.stackedWidget.setCurrentWidget(self.ui.found_page)
        # self.ui.stackedWidget.setCurrentWidget(self.ui.pushButton_foundPage)
        # self.ui.stackedWidget.setCurrentWidget(self.ui.insert_page)

        # set switch button pages
        # self.ui.btn_startApp.clicked.connect(self.showLoadingPage)
        self.ui.btn_startApp.clicked.connect(self.showInsertPage)
        self.ui.btn_insertAnotherImage1.clicked.connect(self.showInsertPage)
        self.ui.btn_insertAnotherImage2.clicked.connect(self.showInsertPage)

        # ====================== Loading Window =========================================
        self.loadingScreen = LoadingScreen()

        # # ======= initiate button connection ==================================
        # self.ui.btn_confirmImageVideo.clicked.connect(self.showLoadingPage)
        self.ui.btn_confirmImageVideo.clicked.connect(self.showMatchPage)
        self.ui.btn_chooseImage.clicked.connect(self.chooseImage)
        self.ui.btn_chooseVideo.clicked.connect(self.chooseVideo)
        self.ui.pushButton_foundPage.clicked.connect(self.showFoundPage)
        self.ui.pushButton_notFoundPage.clicked.connect(self.showNotFoundPage)
        self.ui.pushButton_runVideoDirectly.clicked.connect(self.playVideoDirectly)

        self.ui.btn_changeImage.clicked.connect(self.changeImage_clicked)
        self.ui.btn_changeVIdeo.clicked.connect(self.changeVideo_clicked)

        # not yet functioning
        self.ui.btn_findMatchCharacter.clicked.connect(self.showResultPage)
        # self.ui.pushButton_3.clicked.connect(self.showBlue)

        # drag and drop image
        # self.ui.insertPage_cartoonImage.setPixmap(image)

        # ================ Extra Pages - Advance Search / How To Use ===================
        self.ui.btn_advanceSearch.clicked.connect(self.showAdvanceSearchPage)  # reset all value var
        self.ui.btn_howToUse.clicked.connect(self.showHowToUsePage)
        self.ui.btn_readyToStart.clicked.connect(self.showInsertPage)
        self.ui.btn_findMatchCharacter_advanceSearch.clicked.connect(self.showAdvanceSearchResult)
        # self.ui.btn_findMatchCharacter_advanceSearch.clicked.connect(self.showResultPage)

        self.ui.btn_chooseFile_advancePage.clicked.connect(self.chooseFileAdvance)
        self.ui.btn_chooseImage_advancePage.clicked.connect(self.chooseImageAdvance)
        self.ui.btn_chooseFolder_video.clicked.connect(self.chooseVideoFolder)
        self.ui.btn_chooseFolder_image.clicked.connect(self.chooseImageFolder)

        # =================== Advance Page - radio button / reset =====================
        self.ui.btn_reset_detectionSettings.clicked.connect(self.reset_detectionSettings)
        self.ui.btn_reset_videoDetails.clicked.connect(self.reset_videoDetails)

        self.ui.radioButton_oneFile.clicked.connect(self.radioBtn_chooseFile)
        self.ui.radioButton_imageFolder.clicked.connect(self.radioBtn_chooseImageFolder)
        self.ui.radioButton_videoFolder.clicked.connect(self.radioBtn_chooseVideoFolder)

        # ======= initiate table ==================================
        # change width of column
        self.ui.tableFrameFound.setColumnWidth(0, 300)
        self.ui.tableFrameFound.setColumnWidth(1, 180)
        self.ui.tableFrameFound.setColumnWidth(2, 160)
        #
        # # button openFile =====================================
        self.ui.tableFrameFound.itemDoubleClicked.connect(self.changeFrameFound)

        # ========= initiate cartoon detector ==================
        self.cartoon_image = Cartoon()
        self.cartoon_video = Cartoon()
        # dir = 'images/shin-chan2.jpg'
        # dir = 'images/bean 5 secs.mp4'
        # cartoon.setConfidence(0.6)

        # ============================= videoPlayer ==============================
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # videoWidget = QVideoWidget()
        self.label_moviePlay = QVideoWidget()
        # self.label_moviePlay = QVideoWidget(self.ui.frame_11)
        # self.label_moviePlay.setGeometry(QtCore.QRect(12, 15, 440, 210))
        # self.label_moviePlay.setStyleSheet("background-color:lightyellow; border-radius: 0;")

        # self.playButton = QPushButton()
        # self.ui.pushButton_playVideo.setEnabled(False)
        # self.ui.pushButton_playVideo.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.ui.pushButton_playVideo.clicked.connect(self.play)
        self.ui.pushButton_pauseVideo.clicked.connect(self.openVideoFile)

        self.ui.horizontalSlider_video = QSlider(Qt.Horizontal)
        self.ui.horizontalSlider_video.setRange(0, 0)
        self.ui.horizontalSlider_video.sliderMoved.connect(self.setPosition)

        # self.errorLabel = QLabel()
        # self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self.mediaPlayer.setVideoOutput(self.label_moviePlay)
        # self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def load_frame_output_data(self, name_list='h', time_list='h', accuracy_list='b'):

        # accuracy_list = ['82.61%', '82.79%', '73.9%', '74.23%', '80.14%', '80.31%', '80.25%', '74.33%', '74.25%',
        # '69.91%', '70.37%', '63.82%', '63.83%', '65.21%', '65.17%', '65.2%', '65.24%', '65.27%', '65.25%',
        # '65.32%', '65.32%', '65.33%', '65.33%', '65.4%', '65.38%', '63.53%', '63.49%', '85.45%', '68.85%', '69.0%',
        # '75.48%', '75.56%', '88.24%', '88.26%', '88.19%', '91.88%', '91.84%', '91.83%', '79.39%', '79.07%',
        # '87.3%', '87.75%', '92.47%', '92.52%', '92.56%', '90.77%', '90.87%', '90.92%', '91.12%', '91.13%',
        # '91.21%', '91.24%', '90.14%', '90.32%', '89.54%', '89.54%', '89.59%', '88.61%', '88.39%', '87.01%',
        # '86.96%', '86.97%', '88.17%', '88.08%', '90.41%', '90.41%', '90.41%', '90.41%', '88.91%', '90.87%',
        # '90.86%', '88.27%', '88.18%', '88.17%', '90.19%']
        #
        # time_list = ['0.033 sec', '0.066 sec', '0.100 sec', '0.133 sec', '0.166 sec', '0.200 sec', '0.233 sec',
        # '0.266 sec', '0.300 sec', '0.333 sec', '0.366 sec', '0.400 sec', '0.433 sec', '0.466 sec', '0.500 sec',
        # '0.533 sec', '0.566 sec', '0.600 sec', '0.633 sec', '0.666 sec', '0.700 sec', '0.733 sec', '0.766 sec',
        # '0.800 sec', '0.833 sec', '0.866 sec', '0.900 sec', '1.566 sec', '1.600 sec', '1.633 sec', '3.533 sec',
        # '3.566 sec', '3.600 sec', '3.633 sec', '3.666 sec', '3.766 sec', '3.800 sec', '3.833 sec', '3.866 sec',
        # '3.900 sec', '3.933 sec', '3.966 sec', '4.000 sec', '4.033 sec', '4.066 sec', '4.100 sec', '4.133 sec',
        # '4.166 sec', '4.200 sec', '4.233 sec', '4.266 sec', '4.300 sec', '4.333 sec', '4.366 sec', '4.400 sec',
        # '4.433 sec', '4.466 sec', '4.500 sec', '4.533 sec', '4.566 sec', '4.600 sec', '4.633 sec', '4.666 sec',
        # '4.700 sec', '4.733 sec', '4.766 sec', '4.800 sec', '4.833 sec', '4.866 sec', '4.900 sec', '4.933 sec',
        # '4.966 sec', '5.000 sec', '5.033 sec', '5.066 sec']
        #
        # name_list = ['output\\output_bean00001.png', 'output\\output_bean00002.png', 'output\\output_bean00003.png',
        #  'output\\output_bean00004.png', 'output\\output_bean00005.png', 'output\\output_bean00006.png',
        #  'output\\output_bean00007.png', 'output\\output_bean00008.png', 'output\\output_bean00009.png',
        #  'output\\output_bean00010.png', 'output\\output_bean00011.png', 'output\\output_bean00012.png',
        #  'output\\output_bean00013.png', 'output\\output_bean00014.png', 'output\\output_bean00015.png',
        #  'output\\output_bean00016.png', 'output\\output_bean00017.png', 'output\\output_bean00018.png',
        #  'output\\output_bean00019.png', 'output\\output_bean00020.png', 'output\\output_bean00021.png',
        #  'output\\output_bean00022.png', 'output\\output_bean00023.png', 'output\\output_bean00024.png',
        #  'output\\output_bean00025.png', 'output\\output_bean00026.png', 'output\\output_bean00027.png',
        #  'output\\output_bean00047.png', 'output\\output_bean00048.png', 'output\\output_bean00049.png',
        #  'output\\output_bean00106.png', 'output\\output_bean00107.png', 'output\\output_bean00108.png',
        #  'output\\output_bean00109.png', 'output\\output_bean00110.png', 'output\\output_bean00113.png',
        #  'output\\output_bean00114.png', 'output\\output_bean00115.png', 'output\\output_bean00116.png',
        #  'output\\output_bean00117.png', 'output\\output_bean00118.png', 'output\\output_bean00119.png',
        #  'output\\output_bean00120.png', 'output\\output_bean00121.png', 'output\\output_bean00122.png',
        #  'output\\output_bean00123.png', 'output\\output_bean00124.png', 'output\\output_bean00125.png',
        #  'output\\output_bean00126.png', 'output\\output_bean00127.png', 'output\\output_bean00128.png',
        #  'output\\output_bean00129.png', 'output\\output_bean00130.png', 'output\\output_bean00131.png',
        #  'output\\output_bean00132.png', 'output\\output_bean00133.png', 'output\\output_bean00134.png',
        #  'output\\output_bean00135.png', 'output\\output_bean00136.png', 'output\\output_bean00137.png',
        #  'output\\output_bean00138.png', 'output\\output_bean00139.png', 'output\\output_bean00140.png',
        #  'output\\output_bean00141.png', 'output\\output_bean00142.png', 'output\\output_bean00143.png',
        #  'output\\output_bean00144.png', 'output\\output_bean00145.png', 'output\\output_bean00146.png',
        #  'output\\output_bean00147.png', 'output\\output_bean00148.png', 'output\\output_bean00149.png',
        #  'output\\output_bean00150.png', 'output\\output_bean00151.png', 'output\\output_bean00152.png']

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
        self.ui.insertPage_cartoonImage.setText('              Choose an image to search')
        self.ui.insertPage_cartoonVideo.setText('                Choose a video to search')
        self.image_name = ''
        self.video_name = ''
        self.ui.stackedWidget.setCurrentWidget(self.ui.insert_page)

    def showMatchPage(self):
        # self.ui.stackedWidget.setCurrentWidget(self.ui.loading_page)
        # self.movie.start()
        try:
            if self.image_name != '':
                self.ui.matchPage_inputImage.setPixmap(QPixmap(self.image_name))
                self.cartoon_image.setFileName(self.image_name)

                if self.video_name != '':
                    self.ui.matchPage_inputVideo.setPixmap(QPixmap(self.firstFrameName))

                    # self.showLoadingPage()
                    # self.showLoadingPage()
                    # self.ui.stackedWidget.setCurrentWidget(self.ui.loading_page)
                    # self.ui.label_buffer_insertPage.setHidden(False)
                    # self.ui.stackedWidget.setCurrentWidget(self.ui.insert_page)
                    self.loadingScreen.startAnimation()
                    self.cartoon_image.detectCharacter()
                    self.loadingScreen.stopAnimation()
                    # self.ui.label_buffer_insertPage.setHidden(True)
                    # self.movie.stop()

                    self.ui.text_2.setPlainText(str(self.cartoon_image.isCharacterFound))
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
        if self.cartoon_image.isCharacterFound:

            self.cartoon_video.setFileName(self.video_name)
            self.cartoon_video.setCharacterToFindId(self.cartoon_image.characterId)
            self.loadingScreen.startAnimation()
            self.cartoon_video.detectCharacter()
            self.loadingScreen.stopAnimation()
            # self.ui.label_buffer_insertPage.setHidden(True)

            self.isImageMatchedVideo = self.cartoon_video.isImageMatchedVideo  # assign img match vid is T/F
            # true go to found page
            # false go to not found
            if self.isImageMatchedVideo:
                self.load_frame_output_data(self.cartoon_video.fileNames, self.cartoon_video.timestamps,
                                            self.cartoon_video.frame_accuracies)
                self.showFoundPage()
            else:
                self.showNotFoundPage()
        else:
            self.showNotFoundPage()

    def showNotFoundPage(self):
        self.ui.label_inputImage1.setPixmap(QPixmap(self.image_name))
        self.ui.stackedWidget.setCurrentWidget(self.ui.not_found_page)

    def showFoundPage(self):
        output_image_name = 'output_image.png'

        self.ui.inputImage_found.setPixmap(QPixmap(output_image_name))
        self.ui.frameFound.setText('             Double click on Data to change Frame')
        self.ui.label_frameTitle.setText('      Time : -           ' + '          Accuracy : -')
        self.ui.label_characterName.setText(self.cartoon_image.getCharacterName())
        self.ui.label_accuracy.setText('Accuracy : ' + self.cartoon_image.accuracy_image)
        self.ui.stackedWidget.setCurrentWidget(self.ui.found_page)

    def showAdvanceSearchPage(self):
        self.radioBtn_chooseFile()
        # reset all value to default
        self.reset_videoDetails()
        self.reset_detectionSettings()
        self.ui.advancePage_insertImage.setText('     Choose an image to search')
        self.ui.advancePage_insertFile.setText('         Choose a file to search')
        self.ui.label_dirAdvance_image.setText('Folder Directory')
        self.ui.label_dirAdvance_video.setText('Folder Directory')

        self.ui.stackedWidget.setCurrentWidget(self.ui.advanceSearch_page)

    def showHowToUsePage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.howToUse_page)

    def showLoadingPage(self):
        self.movie.start()
        self.ui.stackedWidget.setCurrentWidget(self.ui.loading_page)

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

    def chooseImageAdvance(self):
        fname = QFileDialog.getOpenFileName(self.ui.insert_page, 'Open file',
                                            'c:\\Users\\Asus\\Pictures\\cartoon character',
                                            "Image files (*.jpg *.png *.jpeg)")
        self.image_name = fname[0]
        self.ui.advancePage_insertImage.setPixmap(QPixmap(self.image_name))

    def chooseFileAdvance(self):
        fname = QFileDialog.getOpenFileName(self.ui.insert_page, 'Open file',
                                            'c:\\Users\\Asus\\Pictures\\cartoon character',
                                            "Image files (*.jpg *.png *.jpeg *.mp4 *.avi)")

        # danger to use self.image_name
        self.fileAdvance_name = fname[0]

        try:
            ext = self.fileAdvance_name.split('.')[-1]
            if ext in self.cartoon_image.IMG_EXT:
                # self.fileExt = 'image'
                self.ui.advancePage_insertFile.setPixmap(QPixmap(self.fileAdvance_name))
            elif ext in self.cartoon_image.VID_EXT:
                # self.fileExt = 'video'
                self.firstFrameName = self.cartoon_video.getFirstFrame(self.fileAdvance_name)
                self.ui.advancePage_insertFile.setPixmap(QPixmap(self.firstFrameName))
            else:
                self.fileExt = ''
                error_msg = "[ERROR] Invalid file format"
                sys.exit(error_msg)

        except:
            self.ui.advancePage_insertFile.setText(' ')
            print('[ERROR] - Cant read image/video file')

    def chooseImageFolder(self):
        directory = QFileDialog.getExistingDirectory(self.ui.insert_page, 'Open file',
                                               'c:\\Users\\Asus\\Pictures\\cartoon character',
                                               QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        try:
            print(directory)
            self.ui.label_dirAdvance_image.setText(directory)
        except:
            print("No folder selected")

    def chooseVideoFolder(self):
        directory = QFileDialog.getExistingDirectory(self.ui.insert_page, 'Open file',
                                               'c:\\Users\\Asus\\Pictures\\cartoon character',
                                               QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        try:
            print(directory)
            self.ui.label_dirAdvance_video.setText(directory)
        except:
            print("No folder selected")

    def changeFrameFound(self):
        row = self.ui.tableFrameFound.currentRow()
        item = self.ui.tableFrameFound.item(row, 0).text()
        time = self.ui.tableFrameFound.item(row, 1).text()
        acc = self.ui.tableFrameFound.item(row, 2).text()
        self.ui.label_frameTitle.setText('      Time : ' + time + '          Accuracy : ' + acc)
        self.setFrameFound(item)

    def playVideoDirectly(self):
        self.runFile(self.videoOutput_name)

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
        self.ui.insertPage_cartoonImage.setText('              Choose an image to search')
        self.image_name = ''
        self.ui.stackedWidget.setCurrentWidget(self.ui.insert_page)

    def changeVideo_clicked(self):
        self.ui.insertPage_cartoonVideo.setText('                Choose a video to search')
        self.video_name = ''
        self.ui.stackedWidget.setCurrentWidget(self.ui.insert_page)

    def radioBtn_chooseFile(self):
        self.ui.radioButton_oneFile.setChecked(True)
        self.ui.frame_dragDrop_3.setEnabled(True)
        self.ui.btn_chooseFile_advancePage.setEnabled(True)

        self.ui.label_dirAdvance_image.setEnabled(False)
        self.ui.btn_chooseFolder_image.setEnabled(False)

        self.ui.label_dirAdvance_video.setEnabled(False)
        self.ui.btn_chooseFolder_video.setEnabled(False)

    def radioBtn_chooseImageFolder(self):
        self.ui.frame_dragDrop_3.setEnabled(False)
        self.ui.btn_chooseFile_advancePage.setEnabled(False)

        self.ui.label_dirAdvance_image.setEnabled(True)
        self.ui.btn_chooseFolder_image.setEnabled(True)

        self.ui.label_dirAdvance_video.setEnabled(False)
        self.ui.btn_chooseFolder_video.setEnabled(False)

    def radioBtn_chooseVideoFolder(self):
        self.ui.frame_dragDrop_3.setEnabled(False)
        self.ui.btn_chooseFile_advancePage.setEnabled(False)

        self.ui.label_dirAdvance_image.setEnabled(False)
        self.ui.btn_chooseFolder_image.setEnabled(False)

        self.ui.label_dirAdvance_video.setEnabled(True)
        self.ui.btn_chooseFolder_video.setEnabled(True)

    def reset_detectionSettings(self):
        confidence = 0.5
        scale = 0.004
        threshold = 0.3

        self.ui.doubleSpinBox_confidence.setValue(confidence)
        self.ui.doubleSpinBox_scale.setValue(scale)
        self.ui.doubleSpinBox_threshold.setValue(threshold)

    def reset_videoDetails(self):
        width = 600
        height = 336
        fps = 30

        self.ui.spinBox_width.setValue(width)
        self.ui.spinBox_height.setValue(height)
        self.ui.spinBox_fps.setValue(fps)

    def showAdvanceSearchResult(self):
        print(22)

        # set vid details and detect settings
        self.cartoon_image.setConfidence(self.ui.doubleSpinBox_confidence.value())
        self.cartoon_image.setScale(self.ui.doubleSpinBox_scale.value())
        self.cartoon_image.setThreshold(self.ui.doubleSpinBox_threshold.value())
        self.cartoon_video.setConfidence(self.ui.doubleSpinBox_confidence.value())
        self.cartoon_video.setScale(self.ui.doubleSpinBox_scale.value())
        self.cartoon_video.setThreshold(self.ui.doubleSpinBox_threshold.value())

        # print(self.ui.doubleSpinBox_threshold.value()) - use this
        # video advance details
        self.cartoon_video.setHeight(self.ui.spinBox_width.value())
        self.cartoon_video.setWidth(self.ui.spinBox_height.value())
        self.cartoon_video.setFps(self.ui.spinBox_fps.value())

        if self.image_name != '':
            self.cartoon_image.setFileName(self.image_name)
            self.cartoon_image.detectCharacter()
            if self.cartoon_image.isCharacterFound:
                print('call findMatch_advanceSearh')
                self.findMatch_advanceSearh()
            else:
                self.showNotFoundPage()
        else:
            self.showPopupError('No Image Chosen!', 'Please choose an input image')

    def findMatch_advanceSearh(self):
        # assign folder directory
        directory = ''



        if self.ui.btn_chooseFile_advancePage.isEnabled() and self.ui.radioButton_oneFile.isChecked():
            try:
                directory = self.fileAdvance_name
                print(directory)

                if directory == '':
                    self.showPopupError('Error', 'Choose a file to search')

                else:
                    print('run file search')
                    self.cartoon_video.setFileName(directory)

                    # self.cartoon_video.setCharacterToFindId(self.cartoon_image.characterId)
                    if self.cartoon_video.MODE == 'image':
                        self.cartoon_video.detectCharacter()

                        if self.cartoon_image.characterId == self.cartoon_video.characterId:
                            self.showFoundPage()
                            # special found page - advance
                        else:
                            self.showNotFoundPage()
                            # special not found page - advance

                    elif self.cartoon_video.MODE == 'video':
                        print('detect video')
                        self.video_name = directory
                        self.showResultPage()

            except:
                self.showPopupError('Error', 'Choose a file to search')

        elif self.ui.btn_chooseFolder_image.isEnabled() and self.ui.radioButton_imageFolder.isChecked():
            try:
                directory = self.ui.label_dirAdvance_image.text()
                print(directory)

                if directory == '' or directory == 'Folder Directory':
                    self.showPopupError('Error', 'Choose a folder to search')

                else:
                    print('run image folder search')

            except:
                self.showPopupError('Error', 'Choose a folder to search')

        elif self.ui.btn_chooseFolder_video.isEnabled() and self.ui.radioButton_videoFolder.isChecked():
            try:
                directory = self.ui.label_dirAdvance_video.text()
                print(directory)

                if directory == '' or directory == 'Folder Directory':
                    self.showPopupError('Error', 'Choose a folder to search')

                else:
                    print('run video folder search')

            except:
                self.showPopupError('Error', 'Choose a folder to search')

        else:
            self.showPopupError('Search Item Not Chosen', 'Choose a search item')

    # # =================== play video event ========================

    def openVideoFile(self):
        fileName = self.videoOutput_name
        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.ui.pushButton_playVideo.setEnabled(True)

    # def openFile(self):
    #     fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
    #                                               QDir.homePath())
    #
    #     if fileName != '':
    #         self.mediaPlayer.setMedia(
    #             QMediaContent(QUrl.fromLocalFile(fileName)))
    #         self.playButton.setEnabled(True)

    def play(self):
        self.movie.start()
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            # self.movie.setPaused(True)
        else:
            self.mediaPlayer.play()
            # self.movie.setPaused(False)

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.ui.pushButton_playVideo.setText('Play')
            # self.ui.pushButton_playVideo.setIcon(
            #     self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.ui.pushButton_playVideo.setText('Pause')
            # self.ui.pushButton_playVideo.setIcon(
            # self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.ui.horizontalSlider_video.setValue(position)

    def durationChanged(self, duration):
        self.ui.horizontalSlider_video.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.ui.pushButton_playVideo.setEnabled(False)
        # self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())


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
