import os
import io
import json
import sys

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QComboBox, QFileDialog,
                             QLabel, QLineEdit, QMainWindow, QPushButton,
                             QTextEdit, QProgressBar, QVBoxLayout ,QCheckBox)
from PyQt5.QtCore import pyqtSlot

from modules import make_files

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
                # self.initSettings()
        # self.settings = self.importSettings()
        self.statusBar()
        defaultFontSize = 10
        # 左揃えのX座標
        defaultLineLeft =40
        # # メニューバーのアイコン設定
        # openFile = QAction('Open', self)
        # # ショートカット設定
        # openFile.setShortcut('Ctrl+O')
        # # ステータスバー設定
        # openFile.setStatusTip('Open new File')
        # openFile.triggered.connect(self.showDialog)

        # # メニューバー作成
        # menubar = self.menuBar()
        # fileMenu = menubar.addMenu('&File')
        # fileMenu.addAction(openFile)

        openNamesFileButton = QPushButton("namesファイルを開く", self)
        openNamesFileButton.setFont(QFont('Arial', defaultFontSize))
        openNamesFileButton.move(defaultLineLeft,48)
        openNamesFileButton.setFixedWidth(128)
        openNamesFileButton.clicked.connect(self.showNamesDialog)

        self.openNamesFileLabel = QLabel(self)
        self.openNamesFileLabel.setFont(QFont('Arial', defaultFontSize))
        self.openNamesFileLabel.move(180,53)
        self.openNamesFileLabel.setText("ファイルが開かれていません")
        self.openNamesFileLabel.adjustSize()

        openCfgFileButton = QPushButton("cfgファイルを開く", self)
        openCfgFileButton.setFont(QFont('Arial', defaultFontSize))
        openCfgFileButton.move(defaultLineLeft,96)
        openCfgFileButton.setFixedWidth(128)
        openCfgFileButton.clicked.connect(self.showCfgDialog)

        self.openCfgFileLabel = QLabel(self)
        self.openCfgFileLabel.setFont(QFont('Arial', defaultFontSize))
        self.openCfgFileLabel.move(180,104)
        self.openCfgFileLabel.setText("ファイルが開かれていません")
        self.openCfgFileLabel.adjustSize()

        base_dir_input_label = QLabel(self)
        base_dir_input_label.setFont(QFont('Arial', defaultFontSize))
        base_dir_input_label.move(defaultLineLeft,158)
        base_dir_input_label.setText("親ディレクトリ名（相対パス）")
        base_dir_input_label.adjustSize()

        self.base_dir_input = QLineEdit(self)
        self.base_dir_input.move(200,150)
        self.base_dir_input.setFixedWidth(200)

        height_input_label = QLabel(self)
        height_input_label.setFont(QFont('Arial', defaultFontSize))
        height_input_label.move(defaultLineLeft,204)
        height_input_label.setText("画像高さ")
        height_input_label.adjustSize()

        self.height_input = QLineEdit(self)
        self.height_input.move(200,200)
        self.height_input.setFixedWidth(200)

        width_input_label = QLabel(self)
        width_input_label.setFont(QFont('Arial', defaultFontSize))
        width_input_label.move(defaultLineLeft,250)
        width_input_label.setText("画像幅")
        width_input_label.adjustSize()

        self.width_input = QLineEdit(self)
        self.width_input.move(200,250)
        self.width_input.setFixedWidth(200)

        executeButton = QPushButton("ファイル作成", self)
        executeButton.setFont(QFont('Arial', defaultFontSize))
        executeButton.move(450, 320)

        executeButton.clicked.connect(self.execButtonClicked) 

        # クリックされたらbuttonClickedの呼び出し

        # self.pbar = QProgressBar(self)
        # # self.pbar.setTextVisible(False)
        # self.pbar.setMinimumWidth(255)
        # self.pbar.move(defaultLineLeft,98)

        # self.ETALabel = QLabel(self)
        # self.ETALabel.move(defaultLineLeft+120,138)
        # self.ETALabel.setMinimumWidth(120)
        # self.ETALabel.setFont(QFont('Arial', defaultFontSize-2))

        # self.stateLabel = QLabel(self)
        # self.stateLabel.move(defaultLineLeft,138)
        # self.stateLabel.setMinimumWidth(120)
        # self.stateLabel.setFont(QFont('Arial', defaultFontSize-2))

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('YoloMakeCfg')
        self.show()

    def showNamesDialog(self):

        open_path = "c://"
        user_name = os.getlogin()

        fileFilter = "names files(*.names);;All files(*)"


        # 第二引数はダイアログのタイトル、第三引数は表示するパス
        if os.path.exists("c://Users/"+user_name):
            open_path = "c://Users/"+user_name
        self.fNames = QFileDialog.getOpenFileName(self, 'Open file', open_path,fileFilter)
        if self.fNames[0]:
            self.openNamesFileLabel.setText(self.fNames[0])
            self.openNamesFileLabel.adjustSize()

    def showCfgDialog(self):

        open_path = "c://"
        user_name = os.getlogin()

        fileFilter = "cfg files(*.cfg);;All files(*)"

        # 第二引数はダイアログのタイトル、第三引数は表示するパス
        if os.path.exists("c://Users/"+user_name):
            open_path = "c://Users/"+user_name
        self.fCfg = QFileDialog.getOpenFileName(self, 'Open file', open_path,fileFilter)
        if self.fCfg[0]:
            self.openCfgFileLabel.setText(self.fCfg[0])
            self.openCfgFileLabel.adjustSize()

    # def showNamesDialog(self):
    #     self.showDialog("names")
    
    # def showCfgDialog(self):
    #     self.showDialog("cfg")

    def execButtonClicked(self):
        self.exec_process()

    # @pyqtSlot()
    def exec_process(self):
        if self.fNames[0]:
            names_input = self.fNames[0]
        if self.fCfg[0]:
            cfg_input = self.fCfg[0]
        base_dir = self.base_dir_input.text()
        width = self.width_input.text()
        height = self.height_input.text()
        if int(width)%32!=0:
            print("幅が32の倍数ではありません")
        if int(height)%32!=0:
            print("高さが32の倍数ではありません")
        make_files(names_input, cfg_input, base_dir, width, height)




if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())