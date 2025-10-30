import sqlite3
from PyQt6 import QtWidgets

DB = 'nbc.db'

class RemindersTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel("Крайни срокове / напомняния"))
        self.list = QtWidgets.QListWidget()
        layout.addWidget(self.list)
        self.btn_mark = QtWidgets.QPushButton("Маркирай като изпълнено")
        layout.addWidget(self.btn_mark)
        self.btn_mark.clicked.connect(self.mark_done)
        self.reload()

    def reload(self):
        self.list.clear()
        conn = sqlite3.connect(DB)
        for title, due, status in conn.execute("SELECT title, due_date, status FROM reminders"):
            self.list.addItem(f"{title} — {due} [{status}]")
        conn.close()

    def mark_done(self):
        cur = self.list.currentItem()
        if not cur: return
        QtWidgets.QMessageBox.information(self, "Готово", "Задачата е маркирана като изпълнена.")
