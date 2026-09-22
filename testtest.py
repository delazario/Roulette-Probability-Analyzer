from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt

# Пример словаря с цветами рулетки
roulette_colors = {
    1: "red", 2: "black", 3: "red", 4: "black", 5: "red", 6: "black",
    7: "red", 8: "black", 9: "red", 10: "black",
    11: "black", 12: "red", 13: "black", 14: "red", 15: "black", 16: "red",
    17: "black", 18: "red", 19: "red", 20: "black", 21: "red", 22: "black",
    23: "red", 24: "black", 25: "red", 26: "black", 27: "red", 28: "black",
    29: "black", 30: "red", 31: "black", 32: "red", 33: "black", 34: "red",
    35: "black", 36: "red", 0: "green"
}

class NumberHistory(QWidget):
    def __init__(self):
        super().__init__()

        self.history_layout = QHBoxLayout()
        self.setLayout(self.history_layout)
        self.history_layout.setSpacing(5)

    def add_number(self, number):
        color = roulette_colors.get(number, "green")

        label = QLabel(str(number))
        label.setFixedSize(30, 30)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(f"""
            QLabel {{
                background-color: {'red' if color == 'red' else 'black' if color == 'black' else 'green'};
                color: white;
                border: 1px solid white;
                font-weight: bold;
            }}
        """)

        self.history_layout.addWidget(label)
