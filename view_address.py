import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLineEdit
import requests
import json


class FullAddressWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 300, 50)
        self.setWindowTitle('Полный Адрес')

        self.address = QLineEdit(self)
        self.address.resize(290, 40)
        self.address.move(5, 5)
        self.address.setReadOnly(True)

    def switch_address(self, address):
        if type(address) == str:
            self.address.setText(address)