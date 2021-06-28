import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# My Imports
from loginDlg import LoginDialog
# from commands_db import Query, Search
from game import StartGame
from commands_db import Query
# Global Variables
uiPath = ''
accessPath = ''
dbPath = ''
seleniumPath = ''
paths = ''
username = ''

# Makes input into Table Mode View
class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
    
    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

# GUI 
class GUI(QMainWindow):
    def __init__(self, width, heigth, windowTitle):
        super(GUI, self).__init__()
        self.setGeometry(800, 600, width, heigth)
        iconPath = os.path.join(uiPath, 'assets', 'icon.png')
        self.setWindowIcon(QIcon(iconPath))  # Insere o icon
        self.setWindowTitle(windowTitle)
        self.threadpool = QThreadPool()

        # Headline font
        self.headline = QFont("Arial", 14, QFont.Bold)

        # Main stacked (Homepage-Vehicle-Health)
        self.stacked = QStackedWidget()
        
        # Scrollable
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.stacked)
        
        
        self.homepageWidgets = QWidget()
        self.homepageLayout = QVBoxLayout()
        self.HomepageUI()

        # AQUI
        self.playWidgets = QWidget()
        self.playLayout = QVBoxLayout()
        self.PlayUI()

        self.searchWidgets = QWidget()
        self.searchLayout = QVBoxLayout()
        self.SearchUI()

        self.stacked.addWidget(self.homepageWidgets)
        self.stacked.addWidget(self.playWidgets)
        self.stacked.addWidget(self.searchWidgets)
        self.setCentralWidget(self.scroll)
        
    # Homepage
    def HomepageUI(self):
        # Insere o logo
        logo = QLabel()
        logoPath = os.path.join(uiPath, 'assets', 'logo.jpeg')
        pixmap = QPixmap(logoPath)  
        logo.resize(200, 200)
        logo.setPixmap(pixmap)
        self.homepageLayout.addWidget(logo)

        # Buttons
        homepageBtn = QWidget()
        homepageBtnLayout = QVBoxLayout()

        homepagePlayBtn = QPushButton('Jogar')
        homepagePlayBtn.pressed.connect(self.PlayConnect)
        
        homepageSearchBtn = QPushButton('Consultar BD')
        homepageSearchBtn.pressed.connect(self.SearchConnect)

        homepageBtnLayout.addWidget(homepagePlayBtn)
        homepageBtnLayout.addWidget(homepageSearchBtn)
        homepageBtn.setLayout(homepageBtnLayout)
        self.homepageLayout.addWidget(homepageBtn)

        self.homepageWidgets.setLayout(self.homepageLayout)
        self.homepageLayout.setAlignment(logo, Qt.AlignCenter)   

    def PlayUI(self):
        global username
        # escolhe o paciente para jogar
        patientWidget = QWidget() 
        patientLayout = QFormLayout()

        # Precisa de carregar o nome dos pacientes da BD
        # 1º Enfermeiro
        pacientes = Query('paciente_id', 'EnfPac', ['', username], 'enfermeiro_id', '', 0)
        print(pacientes)
        # 2º Pacientes
        nome_pacientes = Query('paciente_nome', 'Paciente', pacientes, 'paciente_id', 'OR', 0)
        nome_pacientes = nome_pacientes[1:]
        self.patientName = QComboBox()
        self.patientName.addItems(nome_pacientes)
        patientLayout.addRow(QLabel('Paciente:'), self.patientName)
        
        patientWidget.setLayout(patientLayout)

        optionsBtn = QWidget()
        optionsBtnLayout = QHBoxLayout()
    
        backBtn = QPushButton('Voltar')
        backBtn.pressed.connect(self.BackHomepage)
        playBtn = QPushButton('Jogar')
        playBtn.pressed.connect(self.Play)

        optionsBtnLayout.addWidget(backBtn)
        optionsBtnLayout.addWidget(playBtn)
        optionsBtn.setLayout(optionsBtnLayout)
        self.playLayout.addWidget(patientWidget)
        self.playLayout.addWidget(optionsBtn)
        self.playWidgets.setLayout(self.playLayout)
    
    def SearchUI(self):
        optionsBtn = QWidget()
        optionsBtnLayout = QHBoxLayout()
        
        backBtn = QPushButton('Voltar')
        backBtn.pressed.connect(self.BackHomepage)
        optionsBtnLayout.addWidget(backBtn)
        optionsBtn.setLayout(optionsBtnLayout)
        
        header = ['Paciente', 'Score', 'Timestamp']
        tableView = QTableView()
        
        # Vai ler da BD
        data = [ header,
            ['Pedro', 1000, '28/6/2021'],
            ['Vini', 999, '28/6/2021'],
            ['Catarina', 1001, '29/6/2021']
        ]
        self.model = TableModel(data)
        tableView.setModel(self.model)
        self.searchLayout.addWidget(tableView)
        self.searchLayout.addWidget(optionsBtn)
        self.searchWidgets.setLayout(self.searchLayout)

    def PlayConnect(self):
        self.stacked.setCurrentIndex(1)

    def BackHomepage(self):
        self.stacked.setCurrentIndex(0)

    def Play(self):
        # Abre o jogo
        print('Play: ', self.patientName.currentText())
        global gamePath
        print('GAME: ', gamePath) 
        StartGame(gamePath)
    
    def SearchConnect(self):
        self.stacked.setCurrentIndex(2)
    
    
    def DateConvert(self, date):
        d = date.date().day()
        day = ""
        month = ""
        if d < 10:
            day = "0" + str(d)
        else:
            day = str(d)
        m = date.date().month()
        if m < 10:
            month = "0" + str(m)
        else:
            month = str(m)
        year = date.date().year()
        sDate = day + str('/') + month + str('/') + str(year)
        return sDate
    
    

    # DB functions
    def DBManagerUI(self):
        layout = QVBoxLayout()
        
        menuWidget = QWidget()
        menuLayout = QVBoxLayout()
        
        addEntry = QPushButton('Adicionar entrada')
        addEntry.pressed.connect(self.AddEntryDlg)
        
        editEntry = QPushButton('Editar entrada')
        editEntry.pressed.connect(self.EditEntryDlg)
        
        removeEntry = QPushButton('Remover entrada')
        removeEntry.pressed.connect(self.RemoveEntryDlg)
        
        backBtn = QPushButton('Voltar')
        backBtn.pressed.connect(lambda: self.settingsStacked.setCurrentIndex(0))
        
        menuLayout.addWidget(addEntry)
        menuLayout.addWidget(editEntry)
        menuLayout.addWidget(removeEntry)
        menuLayout.addWidget(backBtn)
        menuWidget.setLayout(menuLayout)

        layout.addWidget(menuWidget)
        self.dbWidget.setLayout(layout)
    
   
    
    def DateConvert(self, date):
        d = date.date().day()
        day = ""
        month = ""
        if d < 10:
            day = "0" + str(d)
        else:
            day = str(d)
        m = date.date().month()
        if m < 10:
            month = "0" + str(m)
        else:
            month = str(m)
        year = date.date().year()
        sDate = day + str('/') + month + str('/') + str(year)
        return sDate
    
    

    # DB functions
    def DBManagerUI(self):
        layout = QVBoxLayout()
        
        menuWidget = QWidget()
        menuLayout = QVBoxLayout()
        
        addEntry = QPushButton('Adicionar entrada')
        addEntry.pressed.connect(self.AddEntryDlg)
        
        editEntry = QPushButton('Editar entrada')
        editEntry.pressed.connect(self.EditEntryDlg)
        
        removeEntry = QPushButton('Remover entrada')
        removeEntry.pressed.connect(self.RemoveEntryDlg)
        
        backBtn = QPushButton('Voltar')
        backBtn.pressed.connect(lambda: self.settingsStacked.setCurrentIndex(0))
        
        menuLayout.addWidget(addEntry)
        menuLayout.addWidget(editEntry)
        menuLayout.addWidget(removeEntry)
        menuLayout.addWidget(backBtn)
        menuWidget.setLayout(menuLayout)

        layout.addWidget(menuWidget)
        self.dbWidget.setLayout(layout)
    
# Calls the GUI
def GUILoad(args):
    print('hola! :D')
    
    global uiPath, gamePath, username
    uiPath = args[0]
    gamePath = args[1]
    app = QApplication([])

    # Login Password Dialog
    login = LoginDialog(paths)
    if login.exec_():
        username = login.Login()
        # Accepts the login
        window = GUI(600, 400, 'Racing Game!')
        window.show()
    sys.exit(app.exec_())