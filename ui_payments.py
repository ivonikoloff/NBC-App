import sqlite3, datetime
import pandas as pd
from PyQt6 import QtWidgets
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

DB = 'nbc.db'

class PaymentsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)

        self.list = QtWidgets.QListWidget()
        layout.addWidget(self.list)

        row = QtWidgets.QHBoxLayout()
        self.btn_add = QtWidgets.QPushButton("Ново плащане")
        self.btn_receipt = QtWidgets.QPushButton("Разписка PDF")
        self.btn_export = QtWidgets.QPushButton("Експорт Excel")
        row.addWidget(self.btn_add)
        row.addWidget(self.btn_receipt)
        row.addWidget(self.btn_export)
        layout.addLayout(row)

        self.btn_add.clicked.connect(self.add_payment)
        self.btn_receipt.clicked.connect(self.gen_receipt)
        self.btn_export.clicked.connect(self.export_excel)
        self.reload()

    def reload(self):
        self.list.clear()
        conn = sqlite3.connect(DB)
        for pid, mid, amt, date, method in conn.execute("SELECT id, member_id, amount, date, method FROM payments"):
            name = conn.execute("SELECT name FROM members WHERE id=?", (mid,)).fetchone()
            member = name[0] if name else "<?>"
            self.list.addItem(f"{pid}: {member} — {amt:.2f} лв. ({date}, {method})")
        conn.close()

    def add_payment(self):
        mid, ok = QtWidgets.QInputDialog.getInt(self, "Плащане", "ID на член:")
        if not ok: return
        amt, ok = QtWidgets.QInputDialog.getDouble(self, "Сума", "Сума (лв.):", 50.00, 0, 1e6, 2)
        if not ok: return
        method, ok = QtWidgets.QInputDialog.getItem(self, "Метод", "Начин:", ["В брой", "Банков превод"], 0, False)
        if not ok: return

        conn = sqlite3.connect(DB)
        conn.execute("INSERT INTO payments(member_id, amount, date, method, doc_no) VALUES(?,?,?,?,?)",
                     (mid, amt, datetime.date.today().isoformat(), method, f"RV-{int(datetime.datetime.now().timestamp())}"))
        conn.commit()
        conn.close()
        self.reload()

    def gen_receipt(self):
        cur = self.list.currentItem()
        if not cur: return
        pid = cur.text().split(":")[0]
        conn = sqlite3.connect(DB)
        row = conn.execute("""SELECT m.name, m.egn, p.amount, p.date, p.method
                              FROM payments p JOIN members m ON p.member_id=m.id WHERE p.id=?""", (pid,)).fetchone()
        conn.close()
        if not row: return
        name, egn, amt, date, method = row
        pdf = f"Разписка_{pid}.pdf"
        c = canvas.Canvas(pdf, pagesize=A4)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 800, "РАЗПИСКА ЗА ЧЛЕНСКИ ВНОС")
        c.setFont("Helvetica", 11)
        c.drawString(50, 780, f"Лице: {name} ({egn})")
        c.drawString(50, 760, f"Сума: {amt:.2f} лв.")
        c.drawString(50, 740, f"Дата: {date}, Метод: {method}")
        c.drawString(50, 720, "Подпис: ___________________")
        c.save()
        QtWidgets.QMessageBox.information(self, "Готово", f"Разписка PDF е създадена: {pdf}")

    def export_excel(self):
        conn = sqlite3.connect(DB)
        df = pd.read_sql_query("""SELECT p.id, m.name AS member, p.amount, p.date, p.method, p.doc_no
                                  FROM payments p JOIN members m ON p.member_id=m.id""", conn)
        conn.close()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Запази като", "payments.xlsx", "Excel (*.xlsx)")
        if not path: return
        df.to_excel(path, index=False)
        QtWidgets.QMessageBox.information(self, "Готово", "Файлът е записан.")
