import sys
import socket

import win32api
import win32con
import os
import threading
import time


from PyQt5 import QtWidgets
from firstUI import Ui_MainWindow

encoding = 'gb2312'
BUFSIZE = 1024
fname="D:/VIDEO/12.mp4"

class MyWindow (QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setupUi(self)
    def sendOnClick(self):
        lst = Listener(9999)  # create a listen thread
        lst.start()

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

# a read thread, read data from remote
class Reader(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        while True:
            data = self.client.recv(BUFSIZE)
            if (data):
                string = bytes.decode(data, encoding)
                print ("from client::", string, "")

                if string == "open":
                    win32api.keybd_event(27, 0, 0, 0)  # ESC
                    time.sleep(0.01)
                    win32api.keybd_event(27, 0, win32con.KEYEVENTF_KEYUP, 0)
                    os.popen(r"D:/VIDEO/mplayer.exe  -loop 0 -fixed-vo " + fname)  # -fs
                if string == "pause":
                    win32api.keybd_event(32, 0, 0, 0)  # 空格
                    time.sleep(0.01)
                    win32api.keybd_event(32, 0, win32con.KEYEVENTF_KEYUP, 0)

                if string == "full":
                    win32api.keybd_event(70, 0, 0, 0)  # 输入f
                    time.sleep(0.01)
                    win32api.keybd_event(70, 0, win32con.KEYEVENTF_KEYUP, 0)
                if string == "send":
                    self.client.sendall(bytes("你好" + "\n", encoding))
                    self.client.sendall(bytes("天才" + "\n", encoding))
                #self.client.send("return frome server::" + string)
            else:

                break
        print ("close:", self.client.getpeername())




# a listen thread, listen remote connect
# when a remote machine request to connect, it will create a read thread to handle
class Listener(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", port))
        self.sock.listen(0)

    def run(self):
        print("listener started")
        while True:
            client, cltadd = self.sock.accept()
            print("accept a connect...")
            Reader(client).start()
            cltadd = cltadd
            print("accept a connect(new reader..)")



if __name__=="__main__":

    app=QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()

    ip = get_host_ip()
    port = "9999"
    myshow.lineEdit.setText(port)
    port = myshow.lineEdit.text()
    print(port)
    
    myshow.textBrowser.setText(ip)


    print("watch is show")
    sys.exit(app.exec())
    print("watch is close")

