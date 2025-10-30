import os, sqlite3, datetime
from PyQt6 import QtWidgets
from PIL import Image
import pytesseract

DB = 'nbc.db'

class ArchiveTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.btn_add = QtWidgets.QPushButton("Качи файл")
        self.btn_search = QtWidgets.QPushButton("Търси по OCR текст")
        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_search)
        self.results = QtWidgets.QListWidget()
        layout.addWidget(self.results)
        self.btn_add.clicked.connect(self.add_doc)
        self.btn_search.clicked.connect(self.search_doc)

    def add_doc(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Избери документ", "", "Images/PDF (*.png *.jpg *.jpeg *.pdf)")
        if not path: return
        text = ""
        try:
            if path.lower().endswith((".png", ".jpg", ".jpeg")):
                text = pytesseract.image_to_string(Image.open(path), lang="bul")
        except Exception:
            text = ""
        conn = sqlite3.connect(DB)
        conn.execute("INSERT INTO documents(name,path,ocr_text,created_at) VALUES(?,?,?,?)",
                     (os.path.basename(path), path, text, datetime.datetime.now().isoformat()))
        conn.commit()
        conn.close()
        QtWidgets.QMessageBox.information(self, "Готово", "Документът е добавен.")

    def search_doc(self):
        term, ok = QtWidgets.QInputDialog.getText(self, "Търсене", "Търси дума:")
        if not ok or not term: return
        self.results.clear()
        conn = sqlite3.connect(DB)
        for name, path in conn.execute("SELECT name, path FROM documents WHERE ocr_text LIKE ?", (f"%{term}%",)):
            self.results.addItem(f"{name} → {path}")
        conn.close()
