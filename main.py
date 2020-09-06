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
        ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ik5UWmhOMkZpT1dVME1UWXhOalE0TkdFMFptRmxNVFV3TmpneVlqVXpNekUwWlRFMll6UTROZz09In0.eyJzdWIiOiJBa2Fua3NoYUBjYXJib24uc3VwZXIiLCJiYWNrZW5kSnd0IjoiZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKU1V6STFOaUlzSW5nMWRDSTZJazVVV21oT01rWnBUMWRWTUUxVVdYaE9hbEUwVGtkRk1GcHRSbXhOVkZWM1RtcG5lVmxxVlhwTmVrVXdXbFJGTWxsNlVUUk9aejA5SW4wPS5leUpvZEhSd09sd3ZYQzkzYzI4eUxtOXlaMXd2WTJ4aGFXMXpYQzloY0hCc2FXTmhkR2x2Ym5ScFpYSWlPaUpWYm14cGJXbDBaV1FpTENKb2RIUndPbHd2WEM5M2MyOHlMbTl5WjF3dlkyeGhhVzF6WEM5emRXSnpZM0pwWW1WeUlqb2lRV3RoYm10emFHRWlMQ0pvZEhSd09sd3ZYQzkzYzI4eUxtOXlaMXd2WTJ4aGFXMXpYQzlyWlhsMGVYQmxJam9pVUZKUFJGVkRWRWxQVGlJc0ltbHpjeUk2SW5kemJ6SXViM0puWEM5d2NtOWtkV04wYzF3dllXMGlMQ0pvZEhSd09sd3ZYQzkzYzI4eUxtOXlaMXd2WTJ4aGFXMXpYQzloY0hCc2FXTmhkR2x2Ym01aGJXVWlPaUp6YW10a2FITnJhbVFpTENKb2RIUndPbHd2WEM5M2MyOHlMbTl5WjF3dlkyeGhhVzF6WEM5bGJtUjFjMlZ5SWpvaVFXdGhibXR6YUdGQVkyRnlZbTl1TG5OMWNHVnlJaXdpYUhSMGNEcGNMMXd2ZDNOdk1pNXZjbWRjTDJOc1lXbHRjMXd2Wlc1a2RYTmxjbFJsYm1GdWRFbGtJam9pTFRFeU16UWlMQ0psZUhBaU9qRTFPVGt6TmpZd05UWXNJbWgwZEhBNlhDOWNMM2R6YnpJdWIzSm5YQzlqYkdGcGJYTmNMMkZ3Y0d4cFkyRjBhVzl1YVdRaU9pSTBOeklpTENKb2RIUndPbHd2WEM5M2MyOHlMbTl5WjF3dlkyeGhhVzF6WEM5aGNIQnNhV05oZEdsdmJsVlZTV1FpT2lJd1l6QmhNRGRrTXkwMU5ESXlMVFEyT0RNdFlXVmpNUzFrWXpnd1lqY3pOak5oT1RraWZRPT0ualZrUmUycVhhbWJrNlhrTnR1M3dwX3Z3d3BVX0NPcmJ2djdjWll3NU1idEdNTHNVbW1yakdaQ2ZhbHdtQW1YdU9LUXZSeFE1WG0wLXc3czh4LUlhM0ktY0xZWVNDc0hEbjhXWmlaMEhMTHlIMDRsQVNheHJLcUdFb3FxdEVFV2RVbWh3dU54TG5TM2ctSkpBRFN5b3Q2SERERjN4c002THVOeEh6N3EteThDRGFHRWtsNlhVS1hZWjMzNlBGYW1LWGhCczBDdmxPcy01M0otTFZZYkV6VVdtUWNNTThOQ3FlYkk4QmVqWTNDMlM1UEt2QnRBZi1CLWZ3QUFYdkpmN1I1c3VrTU1tQUNEMWFsYXFOdWNlQ0ZlMmRydG5MQ1BzRXF5WFgtR3JKUTNibTkzLV9ORjVJNTZ6YVlrNU9VNGtxWTZYRktEZHhNc3RPVUN0RDQ0Ty1BPT0iLCJpc3MiOiJodHRwczpcL1wvYXBwLnF1aWxsaW9uei5jb206OTQ0M1wvb2F1dGgyXC90b2tlbiIsInRpZXJJbmZvIjp7IkZyZWVUaWVyIjp7InN0b3BPblF1b3RhUmVhY2giOnRydWUsInNwaWtlQXJyZXN0TGltaXQiOjIsInNwaWtlQXJyZXN0VW5pdCI6Im1pbiJ9fSwia2V5dHlwZSI6IlBST0RVQ1RJT04iLCJzdWJzY3JpYmVkQVBJcyI6W3sic3Vic2NyaWJlclRlbmFudERvbWFpbiI6ImNhcmJvbi5zdXBlciIsIm5hbWUiOiJRdWlsbGlvbnpBUEktRnJlZSIsImNvbnRleHQiOiJcL3F1aWxsaW9uemFwaWZyZWVcLzEuMC4wIiwicHVibGlzaGVyIjoiYWRtaW4iLCJ2ZXJzaW9uIjoiMS4wLjAiLCJzdWJzY3JpcHRpb25UaWVyIjoiRnJlZVRpZXIifV0sImF1ZCI6Imh0dHA6XC9cL29yZy53c28yLmFwaW1ndFwvZ2F0ZXdheSIsImFwcGxpY2F0aW9uIjp7Im93bmVyIjoiQWthbmtzaGEiLCJ0aWVyIjoiVW5saW1pdGVkIiwibmFtZSI6InNqa2Roc2tqZCIsImlkIjo0NzIsInV1aWQiOm51bGx9LCJzY29wZSI6ImFtX2FwcGxpY2F0aW9uX3Njb3BlIGRlZmF1bHQiLCJjb25zdW1lcktleSI6IndnbVB0TUl5V1RTY2I4X21MVTdkRkNDRUlCVWEiLCJleHAiOjM3NDY4NDg4MDMsImlhdCI6MTU5OTM2NTE1NiwianRpIjoiNzVhYjc5OTctMDc5MC00MzY5LWFlNmYtMDQ4ZDg2Mzk4MGMzIn0.o1F-wamaBk5sOWcgJSZJFPXOgY7xIovVsQEX_tVXhsnoAqo_Xk9tzecK0-cAKUhQ2QuIo1UX7v3f6ukUf7QAD0NyskOaKkIpJH9nRnJ8iVSDOYkkgqHJ0-2VHeAO3-QwCJmhtYVa9bEnRNIzjxDQNgU0XUhayP_zn3dm0b215Ts7m9t68bEjK9k20xPrDt4k5lmT994X6uoJEA6KUxAI5bhTGxsLM5Zn1RQqDo5wpUTrnPD8coQY5gFlQm_cz5-n2qdS08dLogMwOwYp4kEL6HTqO565sS2EM9FF7oASkbmn9HBXyBaG54mqHNJdo6sHBJD7MZ_ZPIyl5HpI1g-P6w"
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
