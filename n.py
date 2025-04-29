import sys
import psycopg2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTableWidget, QTableWidgetItem, QMessageBox,
    QHeaderView, QPushButton, QHBoxLayout, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush
from test_bot import Event


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

        # Верхний розовый контейнер с таблицей
        self.content = QWidget()
        self.content.setStyleSheet("""
            background-color: #FCE6E6;
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
        """)
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Таблица
        self.table = QTableWidget()
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(False)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #FFD1D1;
                color: white;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-top-left-radius: 20px;
                border-top-right-radius: 20px;
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
                padding: 8px;
                margin: 6px;
            }
        """)

        content_layout.addWidget(self.table)
        layout.addWidget(self.content)

        # Нижний розовый контейнер с кнопками
        self.footer = QWidget()
        self.footer.setStyleSheet("""
            background-color: #FFD1D1;
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
        """)
        footer_layout = QHBoxLayout(self.footer)
        footer_layout.setContentsMargins(20, 15, 20, 15)
        footer_layout.setSpacing(15)

        # Кнопки
        self.add_button = QPushButton("Добавить мероприятие")
        self.sort_date_button = QPushButton("Сортировать по дате")
        self.sort_author_button = QPushButton("Сортировать по автору")

        for button in [self.add_button, self.sort_date_button, self.sort_author_button]:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #FCE181;
                    border: none;
                    border-radius: 10px;
                    padding: 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
            """)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            footer_layout.addWidget(button)

        layout.addWidget(self.footer)

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

            cursor.execute("SELECT e_id, name_event, time, username, datetimee FROM events")
            rows = cursor.fetchall()

            # Добавим "Статус" как доп. столбец
            column_names = ["id", "Название", "Время", "Организатор", "Дата и Время", "Статус"]
            self.table.setColumnCount(len(column_names))
            self.table.setHorizontalHeaderLabels(column_names)
            self.table.setRowCount(len(rows))

            for row_idx, row in enumerate(rows):
                event = Event(*row)
                data_list = [
                    event.event_id,
                    event.event_name,
                    event.event_time,
                    event.event_organizer,
                    event.event_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    "Доступно" if event.available else "Закрыто"
                ]

                for col_idx, value in enumerate(data_list):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(QColor("#FFD700")))
                    self.table.setItem(row_idx, col_idx, item)

                self.table.setRowHeight(row_idx, 70)

            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка подключения", f"Не удалось загрузить данные:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminPanel()
    window.show()
    sys.exit(app.exec_())