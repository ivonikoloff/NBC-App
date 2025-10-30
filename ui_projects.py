import sqlite3
from PyQt6 import QtWidgets

DB = 'nbc.db'

class ProjectsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.list = QtWidgets.QListWidget()
        layout.addWidget(self.list)

        row = QtWidgets.QHBoxLayout()
        self.btn_add = QtWidgets.QPushButton("Нов проект")
        self.btn_budget = QtWidgets.QPushButton("Симулация")
        row.addWidget(self.btn_add)
        row.addWidget(self.btn_budget)
        layout.addLayout(row)

        self.btn_add.clicked.connect(self.add_project)
        self.reload()

    def reload(self):
        self.list.clear()
        conn = sqlite3.connect(DB)
        for pid, name, budget, owner, status in conn.execute("SELECT id,name,budget,owner,status FROM projects"):
            self.list.addItem(f"{pid}: {name} — {budget:.2f} лв. ({status})")
        conn.close()

    def add_project(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Проект", "Име:")
        if not ok or not name: return
        budget, ok = QtWidgets.QInputDialog.getDouble(self, "Бюджет", "Сума (лв.):", 1000.00, 0, 1e9, 2)
        if not ok: return
        conn = sqlite3.connect(DB)
        conn.execute("INSERT INTO projects(name,budget,owner,status) VALUES(?,?,?,?)", (name, budget, "УС", "Активен"))
        conn.commit()
        conn.close()
        self.reload()
