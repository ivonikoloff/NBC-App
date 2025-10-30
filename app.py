import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit, QLabel, QMessageBox
)

DB = "nbc.db"

class MemberApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NBC Member Manager")
        self.setMinimumWidth(700)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        form_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Име")
        self.egn_input = QLineEdit()
        self.egn_input.setPlaceholderText("ЕГН")
        self.status_input = QLineEdit()
        self.status_input.setPlaceholderText("Статус (напр. редовен)")
        add_btn = QPushButton("➕ Добави")
        add_btn.clicked.connect(self.add_member)

        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.egn_input)
        form_layout.addWidget(self.status_input)
        form_layout.addWidget(add_btn)
        self.layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton("🔄 Обнови")
        refresh_btn.clicked.connect(self.load_members)
        delete_btn = QPushButton("🗑️ Изтрий избрания")
        delete_btn.clicked.connect(self.delete_member)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addWidget(delete_btn)
        self.layout.addLayout(btn_layout)

        self.load_members()

    def connect_db(self):
        return sqlite3.connect(DB)

    def load_members(self):
        conn = self.connect_db()
        c = conn.cursor()
        c.execute("SELECT id, name, egn, status, joined_at, notes FROM members")
        rows = c.fetchall()
        conn.close()

        headers = ["ID", "Име", "ЕГН", "Статус", "Дата на приемане", "Бележки"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(rows))

        for row_i, row_data in enumerate(rows):
            for col_i, value in enumerate(row_data):
                self.table.setItem(row_i, col_i, QTableWidgetItem(str(value)))

    def add_member(self):
        name = self.name_input.text().strip()
        egn = self.egn_input.text().strip()
        status = self.status_input.text().strip()
        if not name or not egn:
            QMessageBox.warning(self, "Грешка", "Името и ЕГН са задължителни.")
            return

        conn = self.connect_db()
        c = conn.cursor()
        c.execute("INSERT INTO members (name, egn, status, joined_at) VALUES (?, ?, ?, DATE('now'))",
                  (name, egn, status))
        conn.commit()
        conn.close()

        self.name_input.clear()
        self.egn_input.clear()
        self.status_input.clear()
        self.load_members()

    def delete_member(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Грешка", "Не е избран член за изтриване.")
            return

        member_id = self.table.item(selected, 0).text()
        conn = self.connect_db()
        c = conn.cursor()
        c.execute("DELETE FROM members WHERE id = ?", (member_id,))
        conn.commit()
        conn.close()
        self.load_members()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MemberApp()
    window.show()
    sys.exit(app.exec())
