import sys
import psycopg2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush


class AdminPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel")
        self.setGeometry(100, 100, 700, 1000)
        self.setStyleSheet("background-color: white;")

        # Центральный виджет и макет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Розовый контейнер
        self.content = QWidget()
        self.content.setStyleSheet("""
            background-color: #FCE6E6;
            border-radius: 20px;
        """)
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Таблица
        self.table = QTableWidget()
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(False)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #FFD1D1;
                color: white;
                font-weight: bold;
                padding: 10px;
                border: none;
            }
        """)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: transparent;
                border: none;
            }
            QTableWidget::item {
                background-color: #FCE181;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        content_layout.addWidget(self.table)
        layout.addWidget(self.content)

        self.load_data()

    def load_data(self):
        try:
            conn = psycopg2.connect(
                dbname="tg_db",
                user="postgres",
                password="Root1!?_",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM events")
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            self.table.setColumnCount(len(column_names))
            self.table.setRowCount(len(rows))
            self.table.setHorizontalHeaderLabels(column_names)

            for row_idx, row in enumerate(rows):
                # Задаём белую строку: используем прозрачные QTableWidgetItem, если нужно
                for col_idx in range(len(row)):
                    empty_item = QTableWidgetItem()
                    empty_item.setBackground(QBrush(QColor("white")))
                    self.table.setItem(row_idx, col_idx, empty_item)

                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)

                    # Фон жёлтый с закруглением
                    item.setBackground(QBrush(QColor("#FFD700")))
                    self.table.setItem(row_idx, col_idx, item)

                self.table.setRowHeight(row_idx, 60)

            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка подключения", f"Не удалось загрузить данные:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminPanel()
    window.show()
    sys.exit(app.exec_())