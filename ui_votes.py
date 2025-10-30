import sqlite3, datetime
from PyQt6 import QtWidgets
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

DB = 'nbc.db'

class VotesTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.list_agenda = QtWidgets.QListWidget()
        layout.addWidget(QtWidgets.QLabel("Дневен ред:"))
        layout.addWidget(self.list_agenda)

        row = QtWidgets.QHBoxLayout()
        self.btn_vote = QtWidgets.QPushButton("Гласуване")
        self.btn_protocol = QtWidgets.QPushButton("Протокол PDF")
        row.addWidget(self.btn_vote)
        row.addWidget(self.btn_protocol)
        layout.addLayout(row)

        self.btn_protocol.clicked.connect(self.gen_protocol)
        self.reload()

    def reload(self):
        self.list_agenda.clear()
        conn = sqlite3.connect(DB)
        for txt, in conn.execute("SELECT text FROM agenda"):
            self.list_agenda.addItem(txt)
        conn.close()

    def gen_protocol(self):
        pdf = f"Протокол_{int(datetime.datetime.now().timestamp())}.pdf"
        c = canvas.Canvas(pdf, pagesize=A4)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 800, "ПРОТОКОЛ ОТ ЗАСЕДАНИЕ")
        c.setFont("Helvetica", 11)
        y = 770
        for i in range(self.list_agenda.count()):
            c.drawString(60, y, f"- {self.list_agenda.item(i).text()} (Резултат: )")
            y -= 20
        c.drawString(50, y-30, "Председател: ______ (КЕП)")
        c.drawString(50, y-50, "Секретар: ______ (КЕП)")
        c.save()
        QtWidgets.QMessageBox.information(self, "Готово", f"Протоколът е създаден: {pdf}")
