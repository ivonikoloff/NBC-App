import sqlite3, datetime
from PyQt6 import QtWidgets
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

DB = 'nbc.db'

class MembersTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)

        self.list = QtWidgets.QListWidget()
        layout.addWidget(self.list)

        row = QtWidgets.QHBoxLayout()
        self.btn_add = QtWidgets.QPushButton("Добави член")
        self.btn_edit = QtWidgets.QPushButton("Редактирай")
        self.btn_remove = QtWidgets.QPushButton("Изключи")
        self.btn_export = QtWidgets.QPushButton("Експорт Excel")
        row.addWidget(self.btn_add)
        row.addWidget(self.btn_edit)
        row.addWidget(self.btn_remove)
        row.addWidget(self.btn_export)
        layout.addLayout(row)

        self.btn_add.clicked.connect(self.add_member)
        self.btn_remove.clicked.connect(self.exclude_member)

        self.reload()

    def reload(self):
        self.list.clear()
        conn = sqlite3.connect(DB)
        for mid, name, egn, status in conn.execute("SELECT id, name, egn, status FROM members"):
            self.list.addItem(f"{mid}: {name} ({status})")
        conn.close()

    def add_member(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Нов член", "Име:")
        if not ok or not name: return
        egn, ok = QtWidgets.QInputDialog.getText(self, "ЕГН", "ЕГН:")
        if not ok or not egn: return
        status, ok = QtWidgets.QInputDialog.getItem(self, "Статус", "Статус:",
            ["Редовен", "Асоцииран", "Почетен"], 0, False)
        if not ok: return

        conn = sqlite3.connect(DB)
        conn.execute("INSERT INTO members(name, egn, status, joined_at) VALUES(?,?,?,?)",
                     (name, egn, status, datetime.date.today().isoformat()))
        conn.commit()
        conn.close()
        self.reload()

    def exclude_member(self):
        cur = self.list.currentItem()
        if not cur: return
        member_id = cur.text().split(":")[0]
        conn = sqlite3.connect(DB)
        conn.execute("UPDATE members SET status='Изключен', left_at=? WHERE id=?",
                     (datetime.date.today().isoformat(), member_id))
        conn.commit()
        conn.close()

        pdf_name = f"Решение_изключване_{member_id}.pdf"
        c = canvas.Canvas(pdf_name, pagesize=A4)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 800, "РЕШЕНИЕ ЗА ПРЕКРАТЯВАНЕ НА ЧЛЕНСТВО")
        c.setFont("Helvetica", 11)
        c.drawString(50, 780, f"Член ID {member_id} е изключен на {datetime.date.today()}.")
        c.drawString(50, 760, "Председател: __________________")
        c.drawString(50, 740, "Секретар: _____________________")
        c.save()
        QtWidgets.QMessageBox.information(self, "Готово", f"Генериран е PDF: {pdf_name}")
        self.reload()
