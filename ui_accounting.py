from PyQt6 import QtWidgets

class AccountingTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.btn_balance = QtWidgets.QPushButton("Баланс / ОПР")
        self.btn_export = QtWidgets.QPushButton("Експорт ГФО (CSV/XML)")
        layout.addWidget(self.btn_balance)
        layout.addWidget(self.btn_export)
        self.btn_balance.clicked.connect(self.show_reports)
        self.btn_export.clicked.connect(self.export_reports)

    def show_reports(self):
        QtWidgets.QMessageBox.information(self, "Отчети", "Баланс и ОПР са генерирани (примерен режим).")

    def export_reports(self):
        QtWidgets.QMessageBox.information(self, "Експорт", "Експорт на ГФО е подготвен (примерен файл).")
