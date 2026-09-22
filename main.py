import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QLabel, QWidget, QTableWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from design import Ui_MainWindow
from math import floor

class NumberHistory(QWidget):
    def __init__(self, scroll_area):
        super().__init__()
        self.scroll_area = scroll_area
        self.setFixedHeight(40)
        self.setStyleSheet("background-color: #121212;")
        self.setMinimumWidth(0)
        self.x_offset = 5  # Положення наступного числа по осі X

    def add_number(self, number):
        label = QLabel(str(number['number']), self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFixedSize(15, 15)
        label.move(self.x_offset, 5)
        label.setStyleSheet(f"""QLabel {{
                                    background-color: {'green' if number['number'] == 0 else 'red' if number['color'] == "red" else 'black'};
                                    font-size: 8pt;
                                    color: white;
                                    text-align: center;}}""")
        label.show()

        self.x_offset += 20  # 30 ширина + 5 вiдступ
        self.setMinimumWidth(self.x_offset + 10)

        self.scroll_area.horizontalScrollBar().setValue(self.scroll_area.horizontalScrollBar().maximum())

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("icon.ico"))

        self.two_divider = 18 / 37
        self.three_divider = 12 / 37

        self.color_prob = self.two_divider
        self.current_color = ""
        self.color_streak = 1

        self.parity_prob = self.two_divider
        self.current_parity = ""
        self.parity_streak = 1

        self.half_prob = self.two_divider
        self.current_half = ""
        self.half_streak = 1

        self.dozen_prob = self.three_divider
        self.current_dozen = ""
        self.dozen_streak = 1
        self.dozen_dict = {"1 st 12": 0, "2 nd 12": 0, "3 rd 12": 0}

        self.column_prob = self.three_divider
        self.current_column = ""
        self.column_streak = 1
        self.column_dict = {"1st": 0, "2nd": 0, "3rd": 0}

        self.total = 0

        self.red_count = 0
        self.black_count = 0

        self.even_count = 0
        self.odd_count = 0

        self.half_1 = 0
        self.half_2 = 0

        self.dozen_1 = 0
        self.dozen_2 = 0
        self.dozen_3 = 0

        self.column_1 = 0
        self.column_2 = 0
        self.column_3 = 0

        self.zero_count = 0

        self.max_prob = -1
        self.last_prob = -1
        self.bet_steak = 1

        self.history_numbers = []
        self.nums = []
        self.nums = self._classification(self.nums)

        self.ui.btn_add.setShortcut("Return")
        self.ui.btn_add.setFocus()
        self.ui.btn_add.clicked.connect(self._on_add_clicked)

        self.ui.new_game.clicked.connect(self._msg_new_game)

        self.ui.btn_left.clicked.connect(lambda: self.ui.scroll_nums.horizontalScrollBar().setValue(
            self.ui.scroll_nums.horizontalScrollBar().value() - 50))

        self.ui.btn_right.clicked.connect(lambda: self.ui.scroll_nums.horizontalScrollBar().setValue(
            self.ui.scroll_nums.horizontalScrollBar().value() + 50))

        self.ui.save_game.clicked.connect(self.save_numbers)
        self.ui.load_game.clicked.connect(self.load_numbers)

        self.ui.table_prob.setRowCount(5)
        self.ui.table_prob.verticalHeader().setVisible(False)
        self.ui.table_prob.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.ui.table_prob.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.ui.table_prob.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.ui.table_prob.setItem(0, 0, QTableWidgetItem("Червоне/Чорне"))
        self.ui.table_prob.setItem(1, 0, QTableWidgetItem("Парне/Непарне"))
        self.ui.table_prob.setItem(2, 0, QTableWidgetItem("1 — 18/19 — 36"))
        self.ui.table_prob.setItem(3, 0, QTableWidgetItem("Дюжина"))
        self.ui.table_prob.setItem(4, 0, QTableWidgetItem("Колонка"))

        self.ui.table_stats.setRowCount(13)
        self.ui.table_stats.verticalHeader().setVisible(False)
        self.ui.table_stats.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.ui.table_stats.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.ui.table_stats.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.ui.table_stats.setItem(0, 0, QTableWidgetItem("Червоне"))
        self.ui.table_stats.setItem(1, 0, QTableWidgetItem("Чорне"))
        self.ui.table_stats.setItem(2, 0, QTableWidgetItem("Парне"))
        self.ui.table_stats.setItem(3, 0, QTableWidgetItem("Непарне"))
        self.ui.table_stats.setItem(4, 0, QTableWidgetItem("1 — 18"))
        self.ui.table_stats.setItem(5, 0, QTableWidgetItem("19 — 36"))
        self.ui.table_stats.setItem(6, 0, QTableWidgetItem("1 — 12"))
        self.ui.table_stats.setItem(7, 0, QTableWidgetItem("13 — 24"))
        self.ui.table_stats.setItem(8, 0, QTableWidgetItem("25 — 36"))
        self.ui.table_stats.setItem(9, 0, QTableWidgetItem("1-а колонка"))
        self.ui.table_stats.setItem(10, 0, QTableWidgetItem("2-а колонка"))
        self.ui.table_stats.setItem(11, 0, QTableWidgetItem("3-а колонка"))
        self.ui.table_stats.setItem(12, 0, QTableWidgetItem("Zero"))

        self.nums_history = NumberHistory(self.ui.scroll_nums)
        self.ui.scroll_nums.setWidget(self.nums_history)

    def _msg_new_game(self):
        msgbox_clear = QMessageBox()
        msgbox_clear.setIcon(QMessageBox.Icon.Information)
        msgbox_clear.setWindowTitle("Увага")
        msgbox_clear.setText("Ви дійсно хочете почати гру заново?")
        msgbox_clear.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)

        result = msgbox_clear.exec()
        if result == QMessageBox.StandardButton.Yes:
            self.close()
            self.__init__()
            self.show()

    def load_numbers(self):
        msgbox_load_game = QMessageBox()
        msgbox_load_game.setIcon(QMessageBox.Icon.Information)
        msgbox_load_game.setWindowTitle("Увага")
        msgbox_load_game.setText("Ви дійсно хочете завантажити збережений файл гри?")
        msgbox_load_game.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
        result = msgbox_load_game.exec()
        if result == QMessageBox.StandardButton.Yes:
            try:
                self.close()
                self.__init__()
                self.show()
                with open("saved_game.txt", "r", encoding="utf-8") as f:
                    contents = f.read()
                    numbers = [int(num.strip()) for num in contents.split(",") if num.strip().isdigit()]

                    for num in numbers:
                        self._probability(self.nums, num)
                        self._stats(self.nums, num)
            except Exception as e:
                print("Ошибка при загрузке:", e)

    def save_numbers(self):
        msgbox_save_game = QMessageBox()
        msgbox_save_game.setIcon(QMessageBox.Icon.Information)
        msgbox_save_game.setWindowTitle("Увага")
        msgbox_save_game.setText("Ви дійсно хочете зберегти гру?")
        msgbox_save_game.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        result = msgbox_save_game.exec()
        if result == QMessageBox.StandardButton.Yes:
            try:
                with open("saved_game.txt", "w", encoding="utf-8") as f:
                    f.write(",".join(str(n) for n in self.history_numbers))  # Список чисел
            except Exception as e:
                print("Ошибка при сохранении:", e)

    def _on_add_clicked(self):
        text = self.ui.line_add.text()
        try:
            self._probability(self.nums, text)
            self._stats(self.nums, text)
        except ValueError:
            msgbox_value_error = QMessageBox()
            msgbox_value_error.setIcon(QMessageBox.Icon.Warning)
            msgbox_value_error.setWindowTitle("Помилка")
            msgbox_value_error.setText("Невірний тип даних! Введіть ціле число від 0 до 36!")
            msgbox_value_error.setStandardButtons(QMessageBox.StandardButton.Ok)
            msgbox_value_error.exec()
            self.ui.line_add.clear()

    def _classification(self, classified_dict):
        # Створюємо масив словників
        red_nums = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36)  # Кортеж із червоних чисел

        for i in range(37):
            if i == 0:
                color = "none"
                parity = "none"
                half = "none"
                dozen = "none"
                column = "none"
            else:
                color = "red" if i in red_nums else "black"  # red/black

                parity = "even" if i % 2 == 0 else "odd"  # even/odd

                half = "1 to 18" if 1 <= i <= 18 else "19 to 36"  # 1 to 18/19 to 36

                if 1 <= i <= 12:  # 1st/2nd/3rd DOZEN
                    dozen = "1 st 12"
                elif 13 <= i <= 24:
                    dozen = "2 nd 12"
                elif 25 <= i <= 36:
                    dozen = "3 rd 12"
                else:
                    dozen = "none"

                if i % 3 == 1:  # 1st/2nd/3rd COLUMN
                    column = "1st"
                elif i % 3 == 2:
                    column = "2nd"
                elif i % 3 == 0:
                    column = "3rd"
                else:
                    column = "none"

            classified_dict.append({
                "number": i,
                "color": color,
                "parity": parity,
                "dozen": dozen,
                "column": column,
                "1 to 18/19 to 36": half
            })

        classified_dict = {item["number"]: item for item in classified_dict}  # Перетворимо список на словник
        return classified_dict

    def _probability(self, classified_dict, user_input):
        user_input = int(user_input)
        if user_input in classified_dict:
            info = classified_dict[user_input]
            self.nums_history.add_number(info)
            self.history_numbers.append(user_input)

            if not user_input == 0:
                # Імовірність кольору
                if info['color'] == self.current_color:
                    self.color_streak = 1
                    self.current_color = "red" if self.current_color == "black" else "black"
                    self.color_prob = self.two_divider
                else:
                    if self.current_color == "":
                        self.current_color = "red" if info['color'] == "black" else "black"
                    else:
                        self.color_streak += 1
                        self.color_prob = 1 - (19 / 37) ** self.color_streak

                # Імовірність парності
                if info['parity'] == self.current_parity:
                    self.parity_streak = 1
                    self.current_parity = "even" if self.current_parity == "odd" else "odd"
                    self.parity_prob = self.two_divider
                else:
                    if self.current_parity == "":
                        self.current_parity = "even" if info['parity'] == "odd" else "odd"
                    else:
                        self.parity_streak += 1
                        self.parity_prob = 1 - (19 / 37) ** self.parity_streak

                # Імовірність половини
                if info['1 to 18/19 to 36'] == self.current_half:
                    self.half_streak = 1
                    self.current_half = "1 to 18" if self.current_half == "19 to 36" else "19 to 36"
                    self.half_prob = self.two_divider
                else:
                    if self.current_half == "":
                        self.current_half = "1 to 18" if info['1 to 18/19 to 36'] == "19 to 36" else "19 to 36"
                    else:
                        self.half_streak += 1
                        self.half_prob = 1 - (19 / 37) ** self.half_streak

                # Імовірність дюжини
                for i in self.dozen_dict:
                    if i == info['dozen']:
                        self.dozen_dict[info['dozen']] += 1

                if info['dozen'] == self.current_dozen:
                    self.dozen_streak = 1
                    self.dozen_prob = self.three_divider
                    next_dozen = []
                    for i in self.dozen_dict:
                        if not i == info['dozen']:
                            next_dozen.append(self.dozen_dict[i])
                    min_dozen = min(next_dozen)
                    next_dozen.clear()
                    for i in self.dozen_dict:
                        if not i == info['dozen']:
                            if self.dozen_dict[i] == min_dozen:
                                self.current_dozen = i
                else:
                    if self.current_dozen == "":
                        for i in self.dozen_dict:
                            if i == info['dozen']:
                                self.current_dozen = "2 nd 12" if i == "1 st 12" else "1 st 12"
                    else:
                        self.dozen_streak += 1
                        self.dozen_prob = 1 - (25 / 37) ** self.dozen_streak

                # Імовірність колонки
                for i in self.column_dict:
                    if i == info['column']:
                        self.column_dict[info['column']] += 1

                if info['column'] == self.current_column:
                    self.column_streak = 1
                    self.column_prob = self.three_divider
                    next_column = []
                    for i in self.column_dict:
                        if not i == info['column']:
                            next_column.append(self.column_dict[i])
                    min_column = min(next_column)
                    next_column.clear()
                    for i in self.column_dict:
                        if not i == info['column']:
                            if self.column_dict[i] == min_column:
                                self.current_column = i
                else:
                    if self.current_column == "":
                        for i in self.column_dict:
                            if i == info['column']:
                                self.current_column = "2nd" if i == "1st" else "1st"
                    else:
                        self.column_streak += 1
                        self.column_prob = 1 - (25 / 37) ** self.column_streak

                rounded_color = floor(self.color_prob * 10000) / 100
                rounded_parity = floor(self.parity_prob * 10000) / 100
                rounded_half = floor(self.half_prob * 10000) / 100
                rounded_dozen = floor(self.dozen_prob * 10000) / 100
                rounded_column = floor(self.column_prob * 10000) / 100

                self.ui.table_prob.setItem(self.max_prob, 3, QTableWidgetItem(""))
                best_prob = []

                self.ui.table_prob.setItem(0, 1, QTableWidgetItem("Червоне")) if self.current_color == "red" else self.ui.table_prob.setItem(0, 1, QTableWidgetItem("Чорне"))
                self.ui.table_prob.setItem(0, 2, QTableWidgetItem(str(rounded_color) + "%"))
                best_prob.append(rounded_color)

                self.ui.table_prob.setItem(1, 1, QTableWidgetItem("Парне")) if self.current_parity == "even" else self.ui.table_prob.setItem(1, 1, QTableWidgetItem("Непарне"))
                self.ui.table_prob.setItem(1, 2, QTableWidgetItem(str(rounded_parity) + "%"))
                best_prob.append(rounded_parity)

                self.ui.table_prob.setItem(2, 1, QTableWidgetItem("1 — 18")) if self.current_half == "1 to 18" else self.ui.table_prob.setItem(2, 1, QTableWidgetItem("19 — 36"))
                self.ui.table_prob.setItem(2, 2, QTableWidgetItem(str(rounded_half) + "%"))
                best_prob.append(rounded_half)

                if self.current_dozen == "1 st 12":
                    self.ui.table_prob.setItem(3, 1, QTableWidgetItem("1 — 12"))
                elif self.current_dozen == "2 nd 12":
                    self.ui.table_prob.setItem(3, 1, QTableWidgetItem("13 — 24"))
                elif self.current_dozen == "3 nd 12":
                    self.ui.table_prob.setItem(3, 1, QTableWidgetItem("25 — 36"))
                self.ui.table_prob.setItem(3, 2, QTableWidgetItem(str(rounded_dozen) + "%"))
                best_prob.append(rounded_dozen)

                if self.current_column == "1st":
                    self.ui.table_prob.setItem(4, 1, QTableWidgetItem("1-а колонка"))
                elif self.current_column == "2nd":
                    self.ui.table_prob.setItem(4, 1, QTableWidgetItem("2-а колонка"))
                elif self.current_column == "3rd":
                    self.ui.table_prob.setItem(4, 1, QTableWidgetItem("3-а колонка"))
                self.ui.table_prob.setItem(4, 2, QTableWidgetItem(str(rounded_column) + "%"))
                best_prob.append(rounded_column)

                max_value = max(best_prob)
                if max_value > 70.0:
                    self.max_prob = best_prob.index(max_value)
                    if self.max_prob == self.last_prob:
                        self.bet_steak *= 2
                    else:
                        self.bet_steak = 1
                    self.last_prob = self.max_prob
                    self.ui.table_prob.setItem(self.max_prob, 3, QTableWidgetItem(f"x{self.bet_steak}"))
        else:
            msgbox_amount_error = QMessageBox()
            msgbox_amount_error.setIcon(QMessageBox.Icon.Warning)
            msgbox_amount_error.setWindowTitle("Помилка")
            msgbox_amount_error.setText("Введіть число від 0 до 36!")
            msgbox_amount_error.setStandardButtons(QMessageBox.StandardButton.Ok)
            msgbox_amount_error.exec()
        self.ui.line_add.clear()

    def _stats(self, classified_dict, user_input):
        user_input = int(user_input)
        if user_input in classified_dict:
            if user_input == 0:
                self.zero_count += 1
            else:
                info = classified_dict[user_input]

                if info['color'] == "red":
                    self.red_count += 1
                else:
                    self.black_count += 1

                if info['parity'] == "even":
                    self.even_count += 1
                else:
                    self.odd_count += 1

                if info['1 to 18/19 to 36'] == "1 to 18":
                    self.half_1 += 1
                else:
                    self.half_2 += 1

                if info['dozen'] == "1 st 12":
                    self.dozen_1 += 1
                elif info['dozen'] == "2 nd 12":
                    self.dozen_2 += 1
                elif info['dozen'] == "3 rd 12":
                    self.dozen_3 += 1

                if info['column'] == "1st":
                    self.column_1 += 1
                if info['column'] == "2nd":
                    self.column_2 += 1
                elif info['column'] == "3rd":
                    self.column_3 += 1

            self.total += 1

            self.red_percent = round(self.red_count / self.total * 100, 2)
            self.black_percent = round(self.black_count / self.total * 100, 2)

            self.even_percent = round(self.even_count / self.total * 100, 2)
            self.odd_percent = round(self.odd_count / self.total * 100, 2)

            self.half1_percent = round(self.half_1 / self.total * 100, 2)
            self.half2_percent = round(self.half_2 / self.total * 100, 2)

            self.dozen1_percent = round(self.dozen_1 / self.total * 100, 2)
            self.dozen2_percent = round(self.dozen_2 / self.total * 100, 2)
            self.dozen3_percent = round(self.dozen_3 / self.total * 100, 2)

            self.column1_percent = round(self.column_1 / self.total * 100, 2)
            self.column2_percent = round(self.column_2 / self.total * 100, 2)
            self.column3_percent = round(self.column_3 / self.total * 100, 2)

            self.zero_precent = round(self.zero_count / self.total * 100, 2)

            self.ui.table_stats.setItem(0, 1, QTableWidgetItem(str(self.red_percent) + "%"))
            self.ui.table_stats.setItem(0, 2, QTableWidgetItem(str(self.red_count)))
            self.ui.table_stats.setItem(1, 1, QTableWidgetItem(str(self.black_percent) + "%"))
            self.ui.table_stats.setItem(1, 2, QTableWidgetItem(str(self.black_count)))
            self.ui.table_stats.setItem(2, 1, QTableWidgetItem(str(self.even_percent) + "%"))
            self.ui.table_stats.setItem(2, 2, QTableWidgetItem(str(self.even_count)))
            self.ui.table_stats.setItem(3, 1, QTableWidgetItem(str(self.odd_percent) + "%"))
            self.ui.table_stats.setItem(3, 2, QTableWidgetItem(str(self.odd_count)))
            self.ui.table_stats.setItem(4, 1, QTableWidgetItem(str(self.half1_percent) + "%"))
            self.ui.table_stats.setItem(4, 2, QTableWidgetItem(str(self.half_1)))
            self.ui.table_stats.setItem(5, 1, QTableWidgetItem(str(self.half2_percent) + "%"))
            self.ui.table_stats.setItem(5, 2, QTableWidgetItem(str(self.half_2)))
            self.ui.table_stats.setItem(6, 1, QTableWidgetItem(str(self.dozen1_percent) + "%"))
            self.ui.table_stats.setItem(6, 2, QTableWidgetItem(str(self.dozen_1)))
            self.ui.table_stats.setItem(7, 1, QTableWidgetItem(str(self.dozen2_percent) + "%"))
            self.ui.table_stats.setItem(7, 2, QTableWidgetItem(str(self.dozen_2)))
            self.ui.table_stats.setItem(8, 1, QTableWidgetItem(str(self.dozen3_percent) + "%"))
            self.ui.table_stats.setItem(8, 2, QTableWidgetItem(str(self.dozen_3)))
            self.ui.table_stats.setItem(9, 1, QTableWidgetItem(str(self.column1_percent) + "%"))
            self.ui.table_stats.setItem(9, 2, QTableWidgetItem(str(self.column_1)))
            self.ui.table_stats.setItem(10, 1, QTableWidgetItem(str(self.column2_percent) + "%"))
            self.ui.table_stats.setItem(10, 2, QTableWidgetItem(str(self.column_2)))
            self.ui.table_stats.setItem(11, 1, QTableWidgetItem(str(self.column3_percent) + "%"))
            self.ui.table_stats.setItem(11, 2, QTableWidgetItem(str(self.column_3)))
            self.ui.table_stats.setItem(12, 1, QTableWidgetItem(str(self.zero_precent) + "%"))
            self.ui.table_stats.setItem(12, 2, QTableWidgetItem(str(self.zero_count)))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Window()
    window.show()
    sys.exit(app.exec())