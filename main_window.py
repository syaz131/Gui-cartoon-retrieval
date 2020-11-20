import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

# change from file
from Ui_main_pages import Ui_MainWindow


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        # start first page
        self.ui.stackedWidget.setCurrentWidget(self.ui.start_page)

        # set switch button pages
        self.ui.btn_startApp.clicked.connect(self.showInsertPage)
        self.ui.btn_insertAnotherImage1.clicked.connect(self.showInsertPage)
        self.ui.btn_insertAnotherImage2.clicked.connect(self.showInsertPage)
        self.ui.btn_changeImage.clicked.connect(self.showInsertPage)

        self.ui.btn_insertImage.clicked.connect(self.showMatchPage)
        self.ui.pushButton_foundPage.clicked.connect(self.showFoundPage)
        self.ui.pushButton_notFoundPage.clicked.connect(self.showNotFoundPage)

        # not yet functioning
        self.ui.btn_matchCharacter.clicked.connect(self.show)
        # self.ui.pushButton_3.clicked.connect(self.showBlue)

    def show(self):
        self.main_win.show()

    def showInsertPage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.insert_page)

    def showMatchPage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.match_page)

    def showNotFoundPage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.not_found_page)

    def showFoundPage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.found_page)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())

# to compile
# pyinstaller.exe --onefile Pages_colour.py

# to convert ui to py
# pyuic5 name_.ui -o Ui_main_pages.py