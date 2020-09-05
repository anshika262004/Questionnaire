import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
import cv2
import pytesseract
from pytesseract import image_to_string
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract"
import requests
import json

from ui_main import Ui_MainWindow
from ui_splash_screen import Ui_SplashScreen

from ui_styles import Style


from ui_functions import *

counter = 0


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        
        UIFunctions.removeTitleBar(True)
        
        self.setWindowTitle('Questionnaire')
        UIFunctions.labelTitle(self, 'Questionnaire')
       
        
        startSize = QSize(900, 800)
        
        self.setMinimumSize(startSize)
        
        
       
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))
       
        self.ui.btn_home.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_home))

       
        self.ui.listWidget.clear()
        self.ui.btn_practice.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_practice))
        
        
        
        self.ui.pushButton.clicked.connect(self.add_images)
        self.ui.pushButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_4))
        

        
        self.ui.stackedWidget.setMinimumWidth(20)
        
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page))
        
       
        
      
        
        UIFunctions.selectStandardMenu(self, "btn_home")
        
      
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        
        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunctions.returStatus() == 1:
                UIFunctions.maximize_restore(self)

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow
       
        UIFunctions.uiDefinitions(self)
        


        
        self.show()
       
    def add_images(self):
        filename = QFileDialog.getOpenFileName(None, "Open")
        print(filename[0])
        image = cv2.imread(filename[0])
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        text = (image_to_string(threshold_img))
        API_ENDPOINT = "https://app.quillionz.com:8243/quillionzapifree/1.0.0/API/SubmitContent_GetQuestions"
        PARAMS = {

        "shortAnswer": True,

        "recall": True,

        "mcq": True,

        "whQuestions": True,

        "title": "Animal"}


    # your access token key here
        ACCESS_TOKEN = ""
        
        HEADERS = {

        "Authorization": "Bearer " + ACCESS_TOKEN

        }
        
        
        r = requests.post(url=API_ENDPOINT, headers=HEADERS, params=PARAMS, data=text.encode('utf-8'))
        
        question_sa = []

        data_sa = r.json()['Data']['shortAnswer']

        ak =len(data_sa)

        for i in range(ak):

            ques = data_sa[i]['Question']

            question_sa.append(str("Q.")+"  "+ques)
            
        question_fib = []

        answer_fib = [0]
        data_fib = r.json()['Data']['recall']

        l =len(data_fib)

        for i in range(l):

            ques = data_fib[i]['Question']

            ans = data_fib[i]['Answer']

            question_fib.append(ques)

            answer_fib.append(ans)
    
        
    def eventFilter(self, watched, event):
        if watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())
    

    def resizeEvent(self, event):
        self.resizeFunction()
        return super(MainWindow, self).resizeEvent(event)

    def resizeFunction(self):
        print('Height: ' + str(self.height()) + ' | Width: ' + str(self.width()))
   
class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
       
        self.timer.start(35)

        
        self.ui.label_description.setText("<strong>Test</strong> Your Knowledge Here")

        
        QtCore.QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))


        
        self.show()
       
    def progress(self):

        global counter

      
        self.ui.progressBar.setValue(counter)

        
        if counter > 100:

            self.timer.stop()

            
            self.main = MainWindow()
            self.main.show()

            
            self.close()

        
        counter += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeuib.ttf')
    window = SplashScreen()
    sys.exit(app.exec_())
