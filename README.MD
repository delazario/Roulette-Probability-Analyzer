# Roulette Probability Analyzer

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey.svg)

A desktop application designed to analyze the empirical probabilities of European Roulette spins and manage betting recommendations using the Martingale strategy. This software was developed as a Bachelor's thesis project at the National University "Zaporizhzhia Polytechnic".

## 📖 Overview
The **Roulette Probability Analyzer** takes real-time spin results as input and calculates the probabilities of various categories (Red/Black, Even/Odd, Halves, Dozens, Columns) appearing in the next spin. By analyzing historical data and tracking losing streaks, the program automatically suggests betting multipliers based on the Martingale system to help users make informed decisions.

## ✨ Features
* **Real-time Data Entry:** Quickly input winning numbers (0-36) with instant updates to all statistical tables.
* **Automatic Classification:** The app automatically categorizes numbers into colors, parities, halves, dozens, and columns.
* **Probability Calculation:** Dynamically calculates the probability of specific categories hitting next, based on consecutive streak data.
* **Martingale Strategy Integration:** Recommends a bet multiplier (e.g., x2, x4) if a category's probability exceeds a 70% threshold.
* **Detailed Statistics:** Tracks and displays exact hit counts and percentages for all possible bet categories.
* **Session Management:** Save your current game history to a local SQLite database and load it later to resume analysis.
* **Modern GUI:** A clean, dark-themed user interface built with PyQt6 and CSS styling for reduced eye strain.

## 🛠 Technologies
* **Python** - Core application logic.
* **PyQt6 & Qt Designer** - Graphical User Interface.
* **SQLite** - Local database for saving and loading game sessions.

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/delazario/Roulette-Probability-Analyzer.git](https://github.com/delazario/Roulette-Probability-Analyzer.git)
   cd Roulette-Probability-Analyzer
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install PyQt6
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

## 🎮 Usage Guide
1. Launch the application.
2. In the top input field, enter the winning number from the roulette wheel (from `0` to `36`) and press **Enter** (or click **Додати**).
3. The visual history bar will display the number with its corresponding color (Red, Black, or Green).
4. The **Probability Table (Імовірність)** will update to show the current predicted chance of each category hitting. If a streak is detected, a suggested Martingale multiplier (e.g., `x2`) will appear in the "Bet (Ставка)" column.
5. The **Statistics Table (Статистика)** will show the overall percentages and exact counts for the entire session.
6. Use the **Save (Зберегти)** and **Load (Завантажити)** buttons to manage your sessions.

## ⚠️ Disclaimer
This software is developed strictly for **educational and academic purposes**. The application relies on empirical probability tracking and the Martingale betting strategy, which do not guarantee financial profit. Roulette is a game of independent random events. Please gamble responsibly and be aware of the financial risks associated with real-money gambling.

## 📝 License
This project is open-source and available under the [MIT License](LICENSE).