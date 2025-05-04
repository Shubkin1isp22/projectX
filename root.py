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
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QDateTimeEdit, QFormLayout
import datetime


class AdminPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel")
        self.setGeometry(100, 100, 700, 1000)
        self.setStyleSheet("background-color: white;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        self.content = QWidget()
        self.content.setStyleSheet("""
            background-color: #FCE6E6;
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
        """)
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(0, 0, 0, 0)

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

        self.footer = QWidget()
        self.footer.setStyleSheet("""
            background-color: #FFD1D1;
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
        """)
        footer_layout = QHBoxLayout(self.footer)
        footer_layout.setContentsMargins(20, 15, 20, 15)
        footer_layout.setSpacing(15)

        self.add_button = QPushButton("Добавить мероприятие")
        self.sort_date_button = QPushButton("Сортировать по дате")
        self.sort_author_button = QPushButton("Сортировать по автору")

        self.add_button.clicked.connect(self.add_event)
        self.sort_date_button.clicked.connect(self.sort_by_date)
        self.sort_author_button.clicked.connect(self.sort_by_author)

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

        # Добавим поля ввода для нового мероприятия
        self.name_input = QLineEdit()
        self.time_input = QLineEdit()
        self.organizer_input = QLineEdit()
        self.datetime_input = QDateTimeEdit()
        self.datetime_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        # Добавление полей в интерфейс
        form_layout = QFormLayout()
        form_layout.addRow("Название мероприятия:", self.name_input)
        form_layout.addRow("Время мероприятия:", self.time_input)
        form_layout.addRow("Организатор мероприятия:", self.organizer_input)
        form_layout.addRow("Дата и время мероприятия:", self.datetime_input)

        add_event_form = QWidget()
        add_event_form.setLayout(form_layout)
        layout.addWidget(add_event_form)

        self.load_data()        

    def load_data(self, order_by=None):
        try:
            conn = psycopg2.connect(
                dbname="tg_db",
                user="postgres",
                password="Root1!?_",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()

            query = "SELECT e_id, name_event, time, username, datetimee FROM events"
            if order_by == "date":
                query += " ORDER BY datetimee"
            elif order_by == "author":
                query += " ORDER BY username"

            cursor.execute(query)
            rows = cursor.fetchall()

            column_names = ["", "id", "Название", "Время", "Организатор", "Дата и Время", "Статус"]
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

                button_widget = QWidget()
                button_layout = QHBoxLayout(button_widget)
                button_layout.setContentsMargins(0, 0, 0, 0)
                button_layout.setSpacing(5)

                edit_button = QPushButton("✏️")
                delete_button = QPushButton("❌")

                for btn in (edit_button, delete_button):
                    btn.setFixedSize(28, 28)
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #ffffff;
                            border: 1px solid #ccc;
                            border-radius: 5px;
                        }
                        QPushButton:hover {
                            background-color: #eee;
                        }
                    """)

                edit_button.clicked.connect(lambda _, r=row, row_index=row_idx: self.edit_event(r, row_index))
                delete_button.clicked.connect(lambda _, r=row, row_index=row_idx: self.delete_event(r[0], row_index))

                button_layout.addWidget(edit_button)
                button_layout.addWidget(delete_button)
                self.table.setCellWidget(row_idx, 0, button_widget)

                for col_idx, value in enumerate(data_list):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QBrush(QColor("#FFD700")))
                    self.table.setItem(row_idx, col_idx + 1, item)

                self.table.setRowHeight(row_idx, 70)

            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка подключения", f"Не удалось загрузить данные:\n{e}")

    def delete_event(self, event_id, row_index):
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить это мероприятие?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                conn = psycopg2.connect(
                    dbname="tg_db",
                    user="postgres",
                    password="Root1!?_",
                    host="localhost",
                    port="5432"
                )
                cursor = conn.cursor()

                cursor.execute("DELETE FROM events WHERE e_id = %s", (event_id,))
                conn.commit()

                cursor.close()
                conn.close()

                self.table.removeRow(row_index)
                QMessageBox.information(self, "Успех", "Мероприятие успешно удалено.")

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении:\n{e}")

    def edit_event(self, event_data, row_index):
        event_data = list(event_data)
        if isinstance(event_data[4], str):
            event_data[4] = datetime.datetime.strptime(event_data[4], "%Y-%m-%d %H:%M:%S")

        dialog = EditEventDialog(event_data, self)
        if dialog.exec_():
            updated_event = dialog.get_updated_data()
            try:
                conn = psycopg2.connect(
                    dbname="tg_db",
                    user="postgres",
                    password="Root1!?_",
                    host="localhost",
                    port="5432"
                )
                cursor = conn.cursor()

                cursor.execute("""
                    UPDATE events
                    SET name_event = %s, time = %s, username = %s, datetimee = %s
                    WHERE e_id = %s
                """, (updated_event[1], updated_event[2], updated_event[3], updated_event[4], updated_event[0]))

                conn.commit()
                cursor.close()
                conn.close()

                self.table.item(row_index, 2).setText(updated_event[1])
                self.table.item(row_index, 3).setText(updated_event[2])
                self.table.item(row_index, 4).setText(updated_event[3])
                self.table.item(row_index, 5).setText(updated_event[4].strftime("%Y-%m-%d %H:%M:%S"))

                QMessageBox.information(self, "Успех", "Мероприятие обновлено.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении:\n{e}")

    def sort_by_date(self):
        self.load_data(order_by="date")

    def sort_by_author(self):
        self.load_data(order_by="author")

    def add_event(self):
        # Получаем данные нового мероприятия
        new_event = (
            None,  # Или можно оставить пустым, т.к. e_id auto-increment
            self.name_input.text(),
            self.time_input.text(),
            self.organizer_input.text(),
            self.datetime_input.dateTime().toPyDateTime()
        )

        try:
            conn = psycopg2.connect(
                dbname="tg_db",
                user="postgres",
                password="Root1!?_",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()

            # Вставляем данные без e_id
            cursor.execute("""
                INSERT INTO events (name_event, time, username, datetimee)
                VALUES (%s, %s, %s, %s)
            """, (new_event[1], new_event[2], new_event[3], new_event[4]))

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Успех", "Мероприятие успешно добавлено.")
            self.load_data()  # Перезагружаем данные

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении мероприятия:\n{e}")


class EditEventDialog(QDialog):
    def __init__(self, event_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактировать мероприятие")
        self.event_id = event_data[0]

        self.name_input = QLineEdit(event_data[1])
        self.time_input = QLineEdit(event_data[2].strftime("%H:%M") if isinstance(event_data[2], datetime.time) else str(event_data[2]))
        self.organizer_input = QLineEdit(event_data[3])

        self.datetime_input = QDateTimeEdit()
        self.datetime_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        if isinstance(event_data[4], str):
            event_data[4] = datetime.datetime.strptime(event_data[4], "%Y-%m-%d %H:%M:%S")
        self.datetime_input.setDateTime(event_data[4])

        form_layout = QFormLayout()
        form_layout.addRow("Название:", self.name_input)
        form_layout.addRow("Время:", self.time_input)
        form_layout.addRow("Организатор:", self.organizer_input)
        form_layout.addRow("Дата и Время:", self.datetime_input)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.accept)
        form_layout.addRow(self.save_button)

        self.setLayout(form_layout)

    def get_updated_data(self):
        return (
            self.event_id,
            self.name_input.text(),
            self.time_input.text(),
            self.organizer_input.text(),
            self.datetime_input.dateTime().toPyDateTime()
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminPanel()
    window.show()
    sys.exit(app.exec_())
