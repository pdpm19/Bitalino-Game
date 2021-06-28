# Login
# Standard imports
import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Crypto.Hash import SHA256
from commands_db import Query

# Login Password Dialog
class LoginDialog(QDialog):
    def __init__(self, paths):
        uiPath = paths
        iconPath = os.path.join(uiPath, 'assets', 'icon.png')
        super(LoginDialog, self).__init__()
        self.setWindowTitle('Acesso')
        self.setWindowIcon(QIcon(iconPath))  # Insere o icon
        self.numberTries = 0    # number of tries
        
        self.username = QLabel('Utilizador:')
        self.usernameField = QLineEdit()

        self.password = QLabel('Palavra-passe:')
        self.passwordField = QLineEdit()
        self.passwordField.setEchoMode(QLineEdit.Password)  # shows ** instead of characters
        
        # Login Buttons (special type of buttons for Dialogs)
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.rejected.connect(self.Back) # closes the dlg
        #self.buttonBox.accepted.connect(self.Login)
        self.passwordField.editingFinished.connect(self.Login)
        self.grid = QGridLayout()
        self.grid.addWidget(self.username, 0,0)
        self.grid.addWidget(self.usernameField, 0,1)
        self.grid.addWidget(self.password, 1,0)
        self.grid.addWidget(self.passwordField, 1,1)
        
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.grid)
        self.layout.addWidget(self.buttonBox)
        
        self.setLayout(self.layout)

    # Checks if the password is correct, user has numberTries, 3, consecutive tries
    def Login(self):
        # Se está vazio...
        if self.usernameField.text() == '' or self.passwordField.text() == '':
            pass
        else:
            hash = Query('enfermeiro_password', 'Enfermeiro', ['', self.usernameField.text()], 'enfermeiro_id', '', 0)
            hash = hash[1]
            data = self.passwordField.text()
            data = data.encode()
            h = SHA256.new()
            h.update(data)
            if h.hexdigest() == hash:
                self.buttonBox.accepted.connect(self.accept)
                return self.usernameField.text()
            elif self.numberTries < 2 :
                self.numberTries = self.numberTries + 1
                self.passwordField.setText("")
                self.passwordField.setPlaceholderText("%d tentativas restantes..." %(3 - self.numberTries))   # warns the user of the number of left tries
            else:
                sys.exit()  # Closes the app

    def Back(self):
        sys.exit()