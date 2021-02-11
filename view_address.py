from PyQt5.QtWidgets import QWidget, QLineEdit, QCheckBox


class FullAddressWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 300, 100)
        self.setWindowTitle('Полный Адрес')

        self.inp_address = QLineEdit(self)
        self.inp_address.resize(290, 40)
        self.inp_address.move(5, 5)
        self.inp_address.setReadOnly(True)

        self.box_postcode = QCheckBox(self)
        self.box_postcode.setText('Почтовый индекс')
        self.box_postcode.move(5, 60)
        self.box_postcode.clicked.connect(self.add_postcode)

        self.postcode = ''
        self.address = ''

    def add_postcode(self):
        pos = f'Почтовый индекс - {self.postcode}'
        if self.postcode != '' and not self.inp_address.text().endswith(pos):
            self.inp_address.setText(f'{self.address}, {pos}')
        else:
            self.inp_address.setText(self.address)

    def switch_address(self, address, postcode):
        self.postcode = postcode
        self.address = address

        if self.postcode == '':
            self.box_postcode.setEnabled(False)

        if type(address) == str:
            self.inp_address.setText(address)