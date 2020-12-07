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

        self.videoList = []
        self.imageList = []

        we_bear_title = 'UI Images\\title we bare bear.png'
        we_bear_icon = 'UI Images\\we bare bear sticker medium.png'
        self.ui.label_ico_bear.setPixmap(QPixmap(we_bear_title))
        self.ui.label_2.setPixmap(QPixmap(we_bear_icon))
        self.ui.label_14.setPixmap(QPixmap(we_bear_icon))
        self.ui.label_34.setPixmap(QPixmap(we_bear_icon))
        self.ui.label_61.setPixmap(QPixmap(we_bear_icon))

        loadingGif = 'Loading_2.gif'
        self.movie = QMovie(loadingGif)
        self.ui.label_buffer.setMovie(self.movie)
        self.ui.label_videoPlay.setMovie(self.movie)
        # self.ui.label_buffer_insertPage.setMovie(self.movie)
        # self.ui.label_buffer_insertPage.setHidden(True)
        self.movie.start()

        self.videoOutput_name = 'output\\output_video.mp4'
        # self.videoPlay_output = QMovie(self.videoOutput_name)
        # self.ui.label_videoPlay.setMovie(self.videoPlay_output)
        # self.videoPlay_output.setPaused(True)

        # start first page
        self.ui.stackedWidget.setCurrentWidget(self.ui.start_page)
        # self.ui.stackedWidget.setCurrentWidget(self.ui.found_page)
        # self.ui.stackedWidget.setCurrentWidget(self.ui.insert_page)

        # set switch button pages
        # self.ui.btn_startApp.clicked.connect(self.showLoadingPage)
        self.ui.btn_startApp.clicked.connect(self.showInsertPage)
        self.ui.btn_insertAnotherImage1.clicked.connect(self.showInsertPage)
        self.ui.btn_insertAnotherImage2.clicked.connect(self.showInsertPage)
        self.ui.btn_insertAnotherImage_folderFound.clicked.connect(self.showInsertPage)
        self.ui.btn_insertAnotherImage_pageFileAdvSch.clicked.connect(self.showInsertPage)
        self.ui.btn_toInsertPage_image.clicked.connect(self.showInsertPage)
        self.ui.btn_toInsertPage_video.clicked.connect(self.showInsertPage)

        # # ======= initiate button connection ==================================
        # self.ui.btn_confirmImageVideo.clicked.connect(self.showLoadingPage)
        self.ui.btn_confirmImageVideo.clicked.connect(self.showMatchPage)
        self.ui.btn_chooseImage.clicked.connect(self.chooseImage)
        self.ui.btn_chooseVideo.clicked.connect(self.chooseVideo)
        # self.ui.pushButton_foundPage.clicked.connect(self.showFoundPage)
        # self.ui.pushButton_notFoundPage.clicked.connect(self.showNotFoundPage)
        self.ui.pushButton_runVideoDirectly.clicked.connect(self.playVideoDirectly)

        self.ui.btn_toSelectImagePage.clicked.connect(self.showSelectImagePage)
        self.ui.btn_toSelectVideoPage.clicked.connect(self.showSelectVideoPage)
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
        self.ui.btn_findImageSearch.clicked.connect(self.findMatch_imagePageSearch)
        self.ui.btn_findVideoSearch.clicked.connect(self.findMatch_videoPageSearch)

        self.ui.btn_chooseFile_advancePage_image.clicked.connect(self.chooseFileImage)
        self.ui.btn_chooseFile_advancePage_video.clicked.connect(self.chooseFileVideo)
        # self.ui.btn_chooseFile_advancePage_video.clicked.connect(self.chooseFileAdvance)
        # self.ui.btn_chooseImage_advancePage.clicked.connect(self.chooseImageAdvance)
        self.ui.btn_chooseFolder_video.clicked.connect(self.chooseVideoFolder)
        self.ui.btn_chooseFolder_image.clicked.connect(self.chooseImageFolder)

        # =================== Advance Page - radio button / reset =====================
        self.ui.btn_reset_detectionSettings_image.clicked.connect(self.reset_detectionSettings)
        self.ui.btn_reset_detectionSettings_video.clicked.connect(self.reset_detectionSettings)
        self.ui.btn_reset_videoDetails.clicked.connect(self.reset_videoDetails)

        self.ui.radioButton_imageFile.clicked.connect(self.radioBtn_chooseFileImage)
        self.ui.radioButton_videoFile.clicked.connect(self.radioBtn_chooseFileVideo)
        self.ui.radioButton_imageFolder.clicked.connect(self.radioBtn_chooseImageFolder)
        self.ui.radioButton_videoFolder.clicked.connect(self.radioBtn_chooseVideoFolder)

        # ======= initiate table ==================================
        # change width of column
        self.ui.tableFrameFound.setColumnWidth(0, 300)
        self.ui.tableFrameFound.setColumnWidth(1, 160)
        self.ui.tableFrameFound.setColumnWidth(2, 150)

        self.ui.tableFileName_folderFound.setColumnWidth(0, 490)
        self.ui.tableFileName_folderFound.setColumnWidth(1, 120)
        #
        # # button openFile =====================================
        self.ui.tableFrameFound.itemDoubleClicked.connect(self.changeFrameFound)
        self.ui.tableFileName_folderFound.itemDoubleClicked.connect(self.openImageAndVideoOutput)

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
            self.ui.tableFrameFound.setItem(row, 2, QTableWidgetItem(str(accuracy) + '%'))
            row = row + 1

    def load_outputData_folderSearch(self, name_list, accuracy_list):

        self.ui.tableFileName_folderFound.setRowCount(len(name_list))

        row = 0
        for file in name_list:
            self.ui.tableFileName_folderFound.setItem(row, 0, QTableWidgetItem(file))
            row = row + 1

        row = 0
        for accuracy in accuracy_list:
            self.ui.tableFileName_folderFound.setItem(row, 1, QTableWidgetItem(str(accuracy) + '%'))
            row = row + 1

    # =================== show pages ========================
    def show(self):
        self.main_win.show()

    def showInsertPage(self):
        self.settings_details_backToDefault()
        self.ui.insertPage_cartoonImage.setText('                           Choose an image to search')
        # self.ui.insertPage_cartoonVideo.setText('                Choose a video to search')
        self.image_name = ''
        self.video_name = ''
        self.ui.stackedWidget.setCurrentWidget(self.ui.insert_page)

    def showMatchPage(self):
        # self.ui.label_statusStartLoad.setText('  Click the button to start Matching Character >>')

        try:
            if self.image_name != '':
                self.ui.matchPage_inputImage.setPixmap(QPixmap(self.image_name))
                self.cartoon_image.setFileName(self.image_name)
                self.cartoon_image.detectCharacter()
                self.ui.stackedWidget.setCurrentWidget(self.ui.videoSearchPage)
                # self.ui.stackedWidget.setCurrentWidget(self.ui.match_page)

                # if self.video_name != '':
                #     self.ui.matchPage_inputVideo.setPixmap(QPixmap(self.firstFrameName))
                #
                #     self.ui.text_2.setPlainText(str(self.cartoon_image.isCharacterFound))
                #     self.ui.stackedWidget.setCurrentWidget(self.ui.match_page)
                #
                # else:
                #     # when no file selected
                #     self.showPopupError('No Video!', "Please choose a Video")
            else:
                # when no file selected
                self.showPopupError('No Image!', "Please choose an Image")

        except:
            self.showPopupError('No Image or Video!', "Please choose Image and Video")

    def showResultPage(self):
        if self.cartoon_image.isCharacterFound:

            self.cartoon_video.setFileName(self.video_name)
            self.cartoon_video.setCharacterToFindId(self.cartoon_image.characterId)
            # self.loadingScreen.startAnimation()
            self.ui.label_statusStartLoad.setEnabled(True)
            self.cartoon_video.detectCharacter()
            # self.loadingScreen.stopAnimation()
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

    def showFileAdvSearchResult(self):
        self.ui.label_conf_fileSearch.setText(str(self.cartoon_image.CONFIDENCE))
        self.ui.label_scale_fileSearch.setText(str(self.cartoon_image.SCALE))
        self.ui.label_thresh_fileSearch.setText(str(self.cartoon_image.NMS_THRESHOLD))
        self.ui.stackedWidget.setCurrentWidget(self.ui.resultPage_fileSearch)

    def showNotFoundPage(self):
        self.ui.label_inputImage1.setPixmap(QPixmap(self.image_name))
        self.ui.stackedWidget.setCurrentWidget(self.ui.not_found_page)

    def showFolderFoundPage(self):

        output_imageInput = 'output\\output_imageInput.png'
        self.ui.frameFound_folderFoundInput.setPixmap(QPixmap(output_imageInput))
        self.ui.label_characterName_folderFound.setText('Input Image - ' + self.cartoon_image.getCharacterName())
        self.ui.label_frameTitle_folderFound.setText('                                Accuracy : ' +
                                                     self.cartoon_image.accuracy_image)

        self.ui.label_conf_folderFound.setText(str(self.cartoon_video.CONFIDENCE))
        self.ui.label_scale_folderFound.setText(str(self.cartoon_video.SCALE))
        self.ui.label_thresh_folderFound.setText(str(round(self.cartoon_video.NMS_THRESHOLD, 3)))

        self.ui.label_widthFolderFound.setText(str(self.cartoon_video.videoWidth))
        self.ui.label_heightFolderFound.setText(str(self.cartoon_video.videoHeight))
        self.ui.label_fpsFolderFound.setText(str(self.cartoon_video.videoFps))

        self.ui.stackedWidget.setCurrentWidget(self.ui.resultFoundPage_advFolder)

    def showFoundPage(self):
        output_image_name = 'output\\output_image.png'

        self.ui.inputImage_found.setPixmap(QPixmap(output_image_name))
        self.ui.frameFound.setText('             Double click on Data to change Frame')
        self.ui.label_frameTitle.setText('      Time : -           ' + '          Accuracy : -')
        self.ui.label_characterName.setText(self.cartoon_image.getCharacterName())
        self.ui.label_accuracy.setText('Accuracy : ' + self.cartoon_image.accuracy_image)

        self.ui.label_conf_tabFound.setText(str(self.cartoon_video.CONFIDENCE))
        self.ui.label_scale_tabFound.setText(str(self.cartoon_video.SCALE))
        self.ui.label_thresh_tabFound.setText(str(self.cartoon_video.NMS_THRESHOLD))
        self.ui.label_width_tabFound.setText(str(self.cartoon_video.videoWidth))
        self.ui.label_height_tabFound.setText(str(self.cartoon_video.videoHeight))
        self.ui.label_fps_tabFound.setText(str(self.cartoon_video.videoFps))

        # statistics video
        maxAcc = max(self.cartoon_video.frame_accuracies)
        # print(maxAcc)
        minAcc = min(self.cartoon_video.frame_accuracies)
        # print(minAcc+maxAcc)
        sumAcc = sum(self.cartoon_video.frame_accuracies)
        numOfAppearance = len(self.cartoon_video.frame_accuracies)
        avgAcc = round(sumAcc/numOfAppearance, 2)
        numOfFrame = self.cartoon_video.numOfFramestats
        appearancePercentage = round(numOfAppearance/numOfFrame*100, 2)
        # print(appearancePercentage)
        fps = self.cartoon_video.fpsStats
        totalTimeAppearance = round((1/fps)*numOfAppearance, 2)
        # print(totalTimeAppearance)


        self.ui.label_characterName_input.setText('Input Image - ' + self.cartoon_image.getCharacterName())
        self.ui.label_lowestAccNum.setText(str(minAcc)+'%')
        self.ui.label_highestAccNum.setText(str(maxAcc)+'%')

        self.ui.label_averageAccNum.setText(str(avgAcc) + '%')
        self.ui.label_numAppearance.setText(str(numOfAppearance) + ' frames')
        self.ui.label_numFps.setText(str(numOfFrame) + ' frames')
        self.ui.label_percentageAppearance.setText(str(appearancePercentage) + '%')
        self.ui.label_totalAppearanceTime.setText(str(totalTimeAppearance) + ' seconds')




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

        self.ui.stackedWidget.setCurrentWidget(self.ui.imageSearchPage)

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
            # self.ui.insertPage_cartoonVideo.setPixmap(QPixmap(self.firstFrameName))
        except:
            # self.ui.insertPage_cartoonVideo.setText(' ')
            print('[ERROR] - Cant read video file')

    def chooseImageAdvance(self):
        fname = QFileDialog.getOpenFileName(self.ui.insert_page, 'Open file',
                                            'c:\\Users\\Asus\\Pictures\\cartoon character',
                                            "Image files (*.jpg *.png *.jpeg)")
        self.image_name = fname[0]
        self.ui.advancePage_insertImage.setPixmap(QPixmap(self.image_name))

    def chooseFileImage(self):
        fname = QFileDialog.getOpenFileName(self.ui.insert_page, 'Open file',
                                            'c:\\Users\\Asus\\Pictures\\cartoon character',
                                            "Image files (*.jpg *.png *.jpeg)")

        self.fileAdvance_name = fname[0]
        try:
            ext = self.fileAdvance_name.split('.')[-1]
            if ext in self.cartoon_image.IMG_EXT:
                self.ui.advancePage_insertFile_image.setPixmap(QPixmap(self.fileAdvance_name))
            else:
                self.fileExt = ''
                error_msg = "[ERROR] Invalid file format"
                sys.exit(error_msg)

        except:
            self.ui.advancePage_insertFile_image.setText(' ')
            print('[ERROR] - Cant read image file')

    def chooseFileVideo(self):
        fname = QFileDialog.getOpenFileName(self.ui.insert_page, 'Open file',
                                            'c:\\Users\\Asus\\Pictures\\cartoon character',
                                            "Image files (*.mp4 *.avi)")

        self.fileAdvance_name = fname[0]
        try:
            ext = self.fileAdvance_name.split('.')[-1]
            if ext in self.cartoon_image.VID_EXT:
                self.firstFrameName = self.cartoon_video.getFirstFrame(self.fileAdvance_name)
                self.ui.advancePage_insertFile_video.setPixmap(QPixmap(self.firstFrameName))
            else:
                self.fileExt = ''
                error_msg = "[ERROR] Invalid file format"
                sys.exit(error_msg)

        except:
            self.ui.advancePage_insertFile_video.setText(' ')
            print('[ERROR] - Cant read video file')

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

    def openImageAndVideoOutput(self):
        row = self.ui.tableFileName_folderFound.currentRow()
        item = self.ui.tableFileName_folderFound.item(row, 0).text()
        self.runFile(item)

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
        # self.ui.insertPage_cartoonVideo.setText('                Choose a video to search')
        self.video_name = ''
        self.ui.stackedWidget.setCurrentWidget(self.ui.insert_page)


    def radioBtn_chooseFileImage(self):
        self.ui.frame_2.setEnabled(True)
        self.ui.btn_chooseFile_advancePage_image.setEnabled(True)

        self.ui.frame_5.setEnabled(False)
        self.ui.btn_chooseFile_advancePage_video.setEnabled(False)

        self.ui.label_dirAdvance_image.setEnabled(False)
        self.ui.btn_chooseFolder_image.setEnabled(False)

        self.ui.label_dirAdvance_video.setEnabled(False)
        self.ui.btn_chooseFolder_video.setEnabled(False)

    def radioBtn_chooseFileVideo(self):
        self.ui.frame_2.setEnabled(False)
        self.ui.btn_chooseFile_advancePage_image.setEnabled(False)

        self.ui.frame_5.setEnabled(True)
        self.ui.btn_chooseFile_advancePage_video.setEnabled(True)

        self.ui.label_dirAdvance_image.setEnabled(False)
        self.ui.btn_chooseFolder_image.setEnabled(False)

        self.ui.label_dirAdvance_video.setEnabled(False)
        self.ui.btn_chooseFolder_video.setEnabled(False)

    def radioBtn_chooseImageFolder(self):
        self.ui.frame_2.setEnabled(False)
        self.ui.btn_chooseFile_advancePage_image.setEnabled(False)

        self.ui.frame_5.setEnabled(False)
        self.ui.btn_chooseFile_advancePage_video.setEnabled(False)

        self.ui.label_dirAdvance_image.setEnabled(True)
        self.ui.btn_chooseFolder_image.setEnabled(True)

        self.ui.label_dirAdvance_video.setEnabled(False)
        self.ui.btn_chooseFolder_video.setEnabled(False)

    def radioBtn_chooseVideoFolder(self):
        self.ui.frame_2.setEnabled(False)
        self.ui.btn_chooseFile_advancePage_image.setEnabled(False)

        self.ui.frame_5.setEnabled(False)
        self.ui.btn_chooseFile_advancePage_video.setEnabled(False)

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

        self.ui.doubleSpinBox_confidence_video.setValue(confidence)
        self.ui.doubleSpinBox_scale_video.setValue(scale)
        self.ui.doubleSpinBox_threshold_video.setValue(threshold)

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
        self.cartoon_image.isVideoDetails = True
        self.cartoon_video.isVideoDetails = True
        # self.cartoon_image.setConfidence(self.ui.doubleSpinBox_confidence.value())
        # self.cartoon_image.setScale(self.ui.doubleSpinBox_scale.value())
        # self.cartoon_image.setThreshold(self.ui.doubleSpinBox_threshold.value())
        self.cartoon_video.setConfidence(self.ui.doubleSpinBox_confidence.value())
        self.cartoon_video.setScale(self.ui.doubleSpinBox_scale.value())
        self.cartoon_video.setThreshold(self.ui.doubleSpinBox_threshold.value())

        # print(self.ui.doubleSpinBox_threshold.value()) - use this
        # video advance details
        self.cartoon_video.setWidth(self.ui.spinBox_width.value())
        self.cartoon_video.setHeight(self.ui.spinBox_height.value())
        self.cartoon_video.setFps(self.ui.spinBox_fps.value())



        # if self.image_name != '':
        #     self.cartoon_image.setFileName(self.image_name)
        #     self.cartoon_image.detectCharacter()
        if self.cartoon_image.isCharacterFound:
            print('call find_match_character')

            self.find_match_character()
            self.cartoon_image.isVideoDetails = False
            self.cartoon_video.isVideoDetails = False
        else:
            self.showNotFoundPage()
            self.cartoon_image.isVideoDetails = False
            self.cartoon_video.isVideoDetails = False
        # else:
        #     self.showPopupError('No Image Chosen!', 'Please choose an input image')

    def findMatch_imagePageSearch(self):
        print('image search btn')

        self.cartoon_video.isVideoDetails = True
        self.cartoon_video.setConfidence(self.ui.doubleSpinBox_confidence.value())
        self.cartoon_video.setScale(self.ui.doubleSpinBox_scale.value())
        self.cartoon_video.setThreshold(self.ui.doubleSpinBox_threshold.value())

        if self.cartoon_image.isCharacterFound:
            print('find match adv')
            # ===== edit here ==============
            self.find_match_character()

            self.cartoon_image.isVideoDetails = False
            self.cartoon_video.isVideoDetails = False
        else:
            self.showNotFoundPage()
            self.cartoon_image.isVideoDetails = False
            self.cartoon_video.isVideoDetails = False

    def findMatch_videoPageSearch(self):
        print('video search button')

        self.cartoon_video.isVideoDetails = True
        self.cartoon_video.setConfidence(self.ui.doubleSpinBox_confidence_video.value())
        self.cartoon_video.setScale(self.ui.doubleSpinBox_scale_video.value())
        self.cartoon_video.setThreshold(self.ui.doubleSpinBox_threshold_video.value())
        self.cartoon_video.setWidth(self.ui.spinBox_width.value())
        self.cartoon_video.setHeight(self.ui.spinBox_height.value())
        self.cartoon_video.setFps(self.ui.spinBox_fps.value())

        if self.cartoon_image.isCharacterFound:
            print('find match adv')
            # ===== edit here ==============
            self.find_match_character()

            self.cartoon_image.isVideoDetails = False
            self.cartoon_video.isVideoDetails = False
        else:
            self.showNotFoundPage()
            self.cartoon_image.isVideoDetails = False
            self.cartoon_video.isVideoDetails = False

    def find_match_character(self):

        # search image file
        if self.ui.btn_chooseFile_advancePage_image.isEnabled() and self.ui.radioButton_imageFile.isChecked():
            try:
                directory = self.fileAdvance_name
                print(directory)

                if directory == '':
                    self.showPopupError('Error', 'Choose a file to search')

                else:
                    print('run file search')
                    self.cartoon_video.setFileName(directory)
                    self.cartoon_video.detectCharacter()

                    if self.cartoon_image.characterId == self.cartoon_video.characterId:
                        outputName_imageInput = "output\\output_imageInput.png"
                        outputName_imageItem = "output\\output_imageItem.png"

                        self.ui.frameImage_advInput.setPixmap(QPixmap(outputName_imageInput))
                        self.ui.label_found_advInput.setText(self.cartoon_image.getCharacterName())
                        self.ui.label_frameTitle_advInput.setText('                                Accuracy : '
                                                                  + str(self.cartoon_image.accuracy_image)+'%')

                        self.ui.frameImage_advSearch.setPixmap(QPixmap(outputName_imageItem))
                        self.ui.label_found_advSearch.setText(self.cartoon_video.getCharacterName())
                        self.ui.label_frameTitle_advSearch.setText('                                Accuracy : '
                                                                   + str(self.cartoon_video.accuracy_image)+'%')

                        self.ui.label_titleNotFound_fileSearch.setHidden(True)
                        self.ui.label_notFound_advInput.setHidden(True)
                        self.ui.label_notFound_advSearch.setHidden(True)
                        self.ui.label_titleFound_fileSearch.setHidden(False)
                        self.ui.label_found_advInput.setHidden(False)
                        self.ui.label_found_advSearch.setHidden(False)

                        self.showFileAdvSearchResult()

                    else:
                        self.ui.frameImage_advInput.setPixmap(QPixmap(self.cartoon_image.FILE))
                        self.ui.label_frameTitle_advInput.setText('                                Accuracy : -')
                        self.ui.frameImage_advSearch.setPixmap(QPixmap(self.cartoon_video.FILE))
                        self.ui.label_frameTitle_advSearch.setText('                                Accuracy : -')

                        self.ui.label_titleNotFound_fileSearch.setHidden(False)
                        self.ui.label_notFound_advInput.setHidden(False)
                        self.ui.label_notFound_advSearch.setHidden(False)
                        self.ui.label_titleFound_fileSearch.setHidden(True)
                        self.ui.label_found_advInput.setHidden(True)
                        self.ui.label_found_advSearch.setHidden(True)

                        self.showFileAdvSearchResult()

                    # elif self.cartoon_video.MODE == 'video':
                    #     print('detect video')
                    #     self.video_name = directory
                    #     self.showResultPage()

            except:
                self.showPopupError('Error', 'Choose a file to search')

        # search video file
        elif self.ui.btn_chooseFile_advancePage_video and self.ui.radioButton_videoFile.isChecked():
            try:
                directory = self.fileAdvance_name
                print(directory)

                if directory == '':
                    self.showPopupError('Error', 'Choose a file to search')

                else:
                    print('search video file')
                    self.cartoon_video.setFileName(directory)
                    self.cartoon_video.detectCharacter()
                    self.video_name = directory
                    self.showResultPage()
            except:
                self.showPopupError('Error', 'Choose a file to search')



        # Folder Search - IMAGE
        elif self.ui.btn_chooseFolder_image.isEnabled() and self.ui.radioButton_imageFolder.isChecked():
            try:
                print(222)
                directory = self.ui.label_dirAdvance_image.text()
                print(directory)

                if directory == '' or directory == 'Folder Directory':
                    self.showPopupError('Error', 'Choose a folder to search')

                else:
                    print('run image folder search')

                    directoryJpg = directory + '\\*.jpg'
                    directoryJpeg = directory + '\\*.jpeg'
                    directoryPng = directory + '\\*.png'
                    directoryBmp = directory + '\\*.bmp'
                    self.imageList.clear()

                    image_glob = glob.glob(directoryJpg)
                    for image in image_glob:
                        self.imageList.append(image)

                    image_glob = glob.glob(directoryJpeg)
                    for image in image_glob:
                        self.imageList.append(image)

                    image_glob = glob.glob(directoryPng)
                    for image in image_glob:
                        self.imageList.append(image)

                    image_glob = glob.glob(directoryBmp)
                    for image in image_glob:
                        self.imageList.append(image)

                    if len(self.imageList) == 0:
                        self.showPopupError('Error', 'No image file in folder')

                    else:
                        self.detectCartoonList(self.imageList)
                        print(self.imageList)

                        if len(self.cartoon_video.outputImageFolderList) == 0:
                            self.showNotFoundPage()
                        else:
                            self.load_outputData_folderSearch(self.cartoon_video.outputImageFolderList,
                                                              self.cartoon_video.frame_accuracies)

                            self.ui.groupBox_videoDetail_folderSearch.setHidden(True)
                            self.showFolderFoundPage()

            except:
                self.showPopupError('Error', 'Choose a folder to search')

        # Folder Search - VIDEO
        elif self.ui.btn_chooseFolder_video.isEnabled() and self.ui.radioButton_videoFolder.isChecked():
            try:
                directory = self.ui.label_dirAdvance_video.text()
                print(directory)

                if directory == '' or directory == 'Folder Directory':
                    self.showPopupError('Error', 'Choose a folder to search')

                else:
                    print('run video folder search')

                    directoryMp4 = directory + '\\*.mp4'
                    directoryAvi = directory + '\\*.avi'
                    self.videoList.clear()

                    video_glob = glob.glob(directoryMp4)
                    for video in video_glob:
                        self.videoList.append(video)

                    video_glob = glob.glob(directoryAvi)
                    for video in video_glob:
                        self.videoList.append(video)

                    if len(self.videoList) == 0:
                        self.showPopupError('Error', 'No video file in folder')

                    else:
                        self.detectCartoonList(self.videoList)

                        if len(self.cartoon_video.outputVideoFolderList) == 0:
                            self.showNotFoundPage()

                        else:
                            print(self.cartoon_video.frame_accuracies)
                            self.load_outputData_folderSearch(self.cartoon_video.outputVideoFolderList,
                                                              self.cartoon_video.frame_accuracies)

                            self.ui.groupBox_videoDetail_folderSearch.setHidden(False)
                            self.showFolderFoundPage()

            except:
                self.showPopupError('Error', 'Choose a folder to search')

        else:
            self.showPopupError('Search Item Not Chosen', 'Choose a search item')

    def detectCartoonList(self, cartoonList):
        self.cartoon_video.outputImageFolderList.clear()
        self.cartoon_video.outputVideoFolderList.clear()
        self.cartoon_video.frame_accuracies.clear()

        count = 0
        for cartoonFileName in cartoonList:
            self.cartoon_video.setFileName(cartoonFileName)
            self.cartoon_video.setCharacterToFindId(self.cartoon_image.characterId)
            self.cartoon_video.detectCharacter_inFolder(count)
            count = count + 1

    def settings_details_backToDefault(self):
        confidence = 0.5
        scale = 0.004
        threshold = 0.3

        self.cartoon_image.CONFIDENCE = confidence
        self.cartoon_image.SCALE = scale
        self.cartoon_image.NMS_THRESHOLD = threshold

        self.cartoon_video.CONFIDENCE = confidence
        self.cartoon_video.SCALE = scale
        self.cartoon_video.NMS_THRESHOLD = threshold

    def showSelectImagePage(self):
        self.ui.radioButton_imageFile.setChecked(True)
        self.radioBtn_chooseFileImage()
        self.reset_videoDetails()
        self.reset_detectionSettings()

        self.ui.advancePage_insertFile_image.setText('         Choose a file to search')
        self.ui.label_dirAdvance_image.setText('Folder Directory')
        self.fileAdvance_name = ''

        print('image search')
        try:
            if self.image_name != '':
                self.ui.matchPage_inputImage.setPixmap(QPixmap(self.image_name))
                self.cartoon_image.setFileName(self.image_name)
                self.cartoon_image.detectCharacter()
                self.ui.stackedWidget.setCurrentWidget(self.ui.imageSearchPage)
            else:
                self.showPopupError('No Image!', "Please choose an Image before proceed.")
        except:
            self.showPopupError('No Image!', "Please choose an Image before proceed.")


    def showSelectVideoPage(self):
        self.ui.radioButton_videoFile.setChecked(True)
        self.radioBtn_chooseFileVideo()
        self.reset_videoDetails()
        self.reset_detectionSettings()

        self.ui.advancePage_insertFile_video.setText('         Choose a file to search')
        self.ui.label_dirAdvance_video.setText('Folder Directory')
        self.fileAdvance_name = ''

        print('video search')
        try:
            if self.image_name != '':
                self.ui.matchPage_inputImage.setPixmap(QPixmap(self.image_name))
                self.cartoon_image.setFileName(self.image_name)
                self.cartoon_image.detectCharacter()
                self.ui.stackedWidget.setCurrentWidget(self.ui.videoSearchPage)
            else:
                self.showPopupError('No Image!', "Please choose an Image before proceed.")
        except:
            self.showPopupError('No Image!', "Please choose an Image before proceed.")

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
