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
import os

from fpdf import FPDF

from ui_main import Ui_MainWindow
from ui_splash_screen import Ui_SplashScreen

from ui_styles import Style


from ui_functions import *

counter = 0
text = ""
count = 0
a = 0
s = 0


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
        self.ui.label_20.clear()
        self.ui.label_21.clear()
        self.ui.btn_practice.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_practice))
        
        
        self.ui.btn_practice.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_practice))
        self.ui.pushButton.clicked.connect(self.add_images)
        self.ui.pushButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_4))
        

        
        self.ui.stackedWidget.setMinimumWidth(20)
        
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page))
        self.ui.sa_ok.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_4))
        self.ui.fib.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page))
        
       
        
      
        
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
        self.ui.listWidget.clear()
        self.ui.textBrowser.clear()
        self.ui.lineEdit.clear()
        self.ui.label_20.setText( "Please wait while image is being processed")
        self.ui.label_21.setText( "You will be directed to next page once the process is done ")
        self.ui.pushButton_3.setText("Next")
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
        ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ik5UWmhOMkZpT1dVME1UWXhOalE0TkdFMFptRmxNVFV3TmpneVlqVXpNekUwWlRFMll6UTROZz09In0.eyJzdWIiOiJBa2Fua3NoYUBjYXJib24uc3VwZXIiLCJiYWNrZW5kSnd0IjoiZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKU1V6STFOaUlzSW5nMWRDSTZJazVVV21oT01rWnBUMWRWTUUxVVdYaE9hbEUwVGtkRk1GcHRSbXhOVkZWM1RtcG5lVmxxVlhwTmVrVXdXbFJGTWxsNlVUUk9aejA5SW4wPS5leUpvZEhSd09sd3ZYQzkzYzI4eUxtOXlaMXd2WTJ4aGFXMXpYQzloY0hCc2FXTmhkR2x2Ym5ScFpYSWlPaUpWYm14cGJXbDBaV1FpTENKb2RIUndPbHd2WEM5M2MyOHlMbTl5WjF3dlkyeGhhVzF6WEM5emRXSnpZM0pwWW1WeUlqb2lRV3RoYm10emFHRWlMQ0pvZEhSd09sd3ZYQzkzYzI4eUxtOXlaMXd2WTJ4aGFXMXpYQzlyWlhsMGVYQmxJam9pVUZKUFJGVkRWRWxQVGlJc0ltbHpjeUk2SW5kemJ6SXViM0puWEM5d2NtOWtkV04wYzF3dllXMGlMQ0pvZEhSd09sd3ZYQzkzYzI4eUxtOXlaMXd2WTJ4aGFXMXpYQzloY0hCc2FXTmhkR2x2Ym01aGJXVWlPaUp6YzJwcmJtTmxhMnBrYm1NaUxDSm9kSFJ3T2x3dlhDOTNjMjh5TG05eVoxd3ZZMnhoYVcxelhDOWxibVIxYzJWeUlqb2lRV3RoYm10emFHRkFZMkZ5WW05dUxuTjFjR1Z5SWl3aWFIUjBjRHBjTDF3dmQzTnZNaTV2Y21kY0wyTnNZV2x0YzF3dlpXNWtkWE5sY2xSbGJtRnVkRWxrSWpvaUxURXlNelFpTENKbGVIQWlPakUxT1Rrek5UZzJOelVzSW1oMGRIQTZYQzljTDNkemJ6SXViM0puWEM5amJHRnBiWE5jTDJGd2NHeHBZMkYwYVc5dWFXUWlPaUkwTnpFaUxDSm9kSFJ3T2x3dlhDOTNjMjh5TG05eVoxd3ZZMnhoYVcxelhDOWhjSEJzYVdOaGRHbHZibFZWU1dRaU9pSTRaRGc0TWpBek5pMHpPR013TFRRMk4ySXRPV0k0WWkwNU9HUXhZekptTmpZNVpHRWlmUT09LlBEOHoyQ3R0QUtEU3dxcWJfTXIxSWdJVlFWQnByclpFT2JyZkN4bTY1YXVFX0N1NTBjbXI5a1ZScFM2akxXYm9peTV3b1FFbDNfbHVDTW5GeDBvVWMwWTljQkJTTm9BNW9PNWFVN2J1cmdNVnZmWV82TDJMeEgxLUtWRWdvM3BpUlhjeHQ1VUJrd1I0VHRjLTNtU2dsbERhR3Y3bmRuS1gwWkxES3V0T2hlcnFsQXhMU0pyeWRNVmZ3WnhTZHIycDMxa1dsVVYxQ19nV2FfeGhSZlhKSnBwMVg0U1hTVFo4SXRnalFSTW9nOHdmbDd0XzI1b1didFJhMUVPSkFjbGVsZGdnUGdJM2VBeGFLUHhWa2M0LVB1bFJoLTF1ZmdTMzNHYXVIeUpvM3BlSkZhUjZkZm5EaFVtOEdoa1RRMXhmbjNNc2lOcW5QbVpfVTJ4RmZ3dG43UT09IiwiaXNzIjoiaHR0cHM6XC9cL2FwcC5xdWlsbGlvbnouY29tOjk0NDNcL29hdXRoMlwvdG9rZW4iLCJ0aWVySW5mbyI6eyJGcmVlVGllciI6eyJzdG9wT25RdW90YVJlYWNoIjp0cnVlLCJzcGlrZUFycmVzdExpbWl0IjoyLCJzcGlrZUFycmVzdFVuaXQiOiJtaW4ifX0sImtleXR5cGUiOiJQUk9EVUNUSU9OIiwic3Vic2NyaWJlZEFQSXMiOlt7InN1YnNjcmliZXJUZW5hbnREb21haW4iOiJjYXJib24uc3VwZXIiLCJuYW1lIjoiUXVpbGxpb256QVBJLUZyZWUiLCJjb250ZXh0IjoiXC9xdWlsbGlvbnphcGlmcmVlXC8xLjAuMCIsInB1Ymxpc2hlciI6ImFkbWluIiwidmVyc2lvbiI6IjEuMC4wIiwic3Vic2NyaXB0aW9uVGllciI6IkZyZWVUaWVyIn1dLCJhdWQiOiJodHRwOlwvXC9vcmcud3NvMi5hcGltZ3RcL2dhdGV3YXkiLCJhcHBsaWNhdGlvbiI6eyJvd25lciI6IkFrYW5rc2hhIiwidGllciI6IlVubGltaXRlZCIsIm5hbWUiOiJzc2prbmNla2pkbmMiLCJpZCI6NDcxLCJ1dWlkIjpudWxsfSwic2NvcGUiOiJhbV9hcHBsaWNhdGlvbl9zY29wZSBkZWZhdWx0IiwiY29uc3VtZXJLZXkiOiJ0SWpZMG9Yd0lwQkg1OUpWZmYyWE5YQVRCYUVhIiwiZXhwIjozNzQ2ODQxNDIzLCJpYXQiOjE1OTkzNTc3NzYsImp0aSI6IjFmY2JhMjI3LWEwZGEtNDdmOC04MjM0LTRlNmZlYTQ2N2Y5OSJ9.HEWFq08OT8R3y-uuX56HmaYIlf2OZ3WhumWT2TMEPIWNE4a8VgzX5XJYaL-5iZDrnzfpKkm7nIyMpFkv2rDMx_MNq5nNXVf8nFJBAdpmB82jC2xbVZhGaLXUXM0j5kfeF5sEvicEYXrg3GsLG3-QjzBWRYLDQ4qABUEA16YH2CQKWAy-cEqzO1N4JK49udj17ir19WWamne_BzhqA0iYiKDdG5V2RWBRHTfSB-t6SzkMuzmueeMLxKjvzAeLjAzowKenocTDGMi4pLX9a1j18k0jiAIyx10arl2OxSIOVy4ZKJtuS1XwydjefSh221hohxIkCTE-ejui0SMEFVvCuQ"
        
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
            
        print(question_sa)
        self.ui.listWidget.addItems(question_sa)
        
        self.ui.short_ans.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.sa_ans))
            
        def pdf(list,length):
        
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            pdf = FPDF()

            pdf.set_margins(4,5, 2)

            pdf.add_page()

            pdf.set_font("Times",'B', size=30)

            pdf.cell(200, 10, txt="Test Paper", ln=15, align="C")

 

            pdf.ln(5)

            pdf.set_font('Times', 'B', 20)

            pdf.cell(200, 10, txt="Short Answers", ln=15, align="C")

            pdf.ln(8)

            pdf.set_font('Times', 'I', 10)

            pdf.multi_cell(200, 10, txt="This test has been generated using the Questionnaire software.No answers are provided to the questions and it is upto the discretion of the candidate to decide upon the right answers.A short answer is of 3-4 sentences,so the answers should be brief",align ='J')

            pdf.ln(10)

            pdf.set_font('Times', 'B', 15)
        
        

            for i in range(length):

                pdf.multi_cell(200, 10, txt=str(i+1) + "." + "     " + list[i])

                pdf.ln(10)

                x = pdf.get_x()

                y = pdf.get_y()

                pdf.dashed_line(x,y,x+175,y,6)

                pdf.ln(10)
                
                
            pdf.output(desktop + "/" + "Questions" + ".pdf") 
            
        self.ui.pushButton_5.clicked.connect(pdf(question_sa,ak))    
        self.ui.sa_ok.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_4))
        check = []    
        question_fib = []

        answer_fib = [0]
        gadha =[]
        data_fib = r.json()['Data']['recall']

        l =len(data_fib)

        for i in range(l):

            ques = data_fib[i]['Question']

            ans = data_fib[i]['Answer']

            question_fib.append(ques)

            answer_fib.append(ans)
            
      def click():
            global count
            global s
            self.ui.label_20.clear()
            self.ui.label_21.clear()
            if count == l:
                self.ui.pushButton_3.setText("Submit")
                user = (self.ui.lineEdit.text())
                gadha.append(user)
                
                
                if user == answer_fib[count]:
                    check.append('Correct')
                    s = s+1
                else:
                    check.append('wrong')
                print(check)
                
                
                self.ui.pushButton_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
                
                
                
                
            
                
            
            else:
                self.ui.textBrowser_7.setText(str(l))
                self.ui.textBrowser.setText(str("Q.")+" "+str(count+1)+"  "+question_fib[count])
                
                user = (self.ui.lineEdit.text())
                gadha.append(user)
                if user == answer_fib[count]:
                    check.append('Correct')
                    s = s+1
                else:
                    check.append('Wrong')
                self.ui.lineEdit.clear()
                count = count + 1
                self.ui.pushButton_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page))
                
            return
        
        def score():
            global a
            self.ui.textBrowser_2.setText(str(s))
            if a == l:
                
                self.ui.pushButton_4.setText("Go to Type of Question")
                self.ui.pushButton_4.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_4))
                
                
            else:
                self.ui.pushButton_4.setText("Next")
                self.ui.textBrowser_3.setText(str("Q.")+" "+str(a+1)+"  "+question_fib[a])
                self.ui.textBrowser_5.setText(gadha[a+1])
                self.ui.textBrowser_6.setText(answer_fib[a+1])

                if check[a+1] == "Correct":
                    self.ui.textBrowser_4.setText("Correct")
                    self.ui.textBrowser_4.setStyleSheet("color: rgb(166, 255, 139);")
                    
                else:
                   self.ui.textBrowser_4.setText("Wrong")
                   self.ui.textBrowser_4.setStyleSheet("color: Red;")
                a = a + 1
                self.ui.pushButton_4.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_5))
                
            
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_5))
        self.ui.pushButton_4.clicked.connect(score)
        self.ui.pushButton_2.clicked.connect(score)
        self.ui.pushButton_3.setText("Next")        
        self.ui.pushButton_3.clicked.connect(click)
        self.ui.pushButton_3.setText("Next")  
        self.ui.fib.clicked.connect(click)
        self.ui.fib.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page))
        
        
         
       
                
           
        print(question_fib)
        print(answer_fib)
       
        print(check)
        
        return()
        
    
        
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
