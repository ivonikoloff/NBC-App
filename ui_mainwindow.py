from PyQt6 import QtWidgets
from .ui_members import MembersTab
from .ui_payments import PaymentsTab
from .ui_projects import ProjectsTab
from .ui_accounting import AccountingTab
from .ui_votes import VotesTab
from .ui_archive import ArchiveTab
from .ui_reminders import RemindersTab

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NBC Association")
        self.resize(1200, 800)

        tabs = QtWidgets.QTabWidget()
        tabs.addTab(MembersTab(), "Членство")
        tabs.addTab(PaymentsTab(), "Плащания")
        tabs.addTab(ProjectsTab(), "Проекти и бюджети")
        tabs.addTab(AccountingTab(), "Счетоводство")
        tabs.addTab(VotesTab(), "Гласувания / Протоколи")
        tabs.addTab(ArchiveTab(), "Архив / OCR")
        tabs.addTab(RemindersTab(), "Напомняния")

        self.setCentralWidget(tabs)
