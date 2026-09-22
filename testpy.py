from math import floor

def classification(classified_dict):
    #=================Создаем массив словарей=================#
    red_nums = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36) # Кортеж из красных чисел

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

    classified_dict = {item["number"]: item for item in classified_dict}  # Преобразуем список в словарь
    return classified_dict

def stats(classified_dict):
    # Статистика по цветам
    total = 0

    red_count = 0
    black_count = 0

    even_count = 0
    odd_count = 0

    half_1 = 0
    half_2 = 0

    dozen_1 = 0
    dozen_2 = 0
    dozen_3 = 0

    column_1 = 0
    column_2 = 0
    column_3 = 0

    while True:  # Спрашиваем у пользователя число
        try:
            user_input = int(input("Введите число от 0 до 36: "))
            if user_input in classified_dict:
                info = classified_dict[user_input]
                total += 1

                if info['color'] == "red":
                    red_count += 1
                else:
                    black_count += 1

                if info['parity'] == "even":
                    even_count += 1
                else:
                    odd_count += 1

                if info['dozen'] == "1 st 12":
                    dozen_1 += 1
                elif info['dozen'] == "2 nd 12":
                    dozen_2 += 1
                elif info['dozen'] == "3 rd 12":
                    dozen_3 += 1

                if info['column'] == "1st":
                    column_1 += 1
                if info['column'] == "2nd":
                    column_2 += 1
                elif info['column'] == "3rd":
                    column_3 += 1

                if info['1 to 18/19 to 36'] == "1 to 18":
                    half_1 += 1
                else:
                    half_2 += 1

                red_percent = red_count / total * 100
                black_percent = black_count / total * 100

                even_percent = even_count / total * 100
                odd_percent = odd_count / total * 100

                half1_percent = half_1 / total * 100
                half2_percent = half_2 / total * 100

                dozen1_percent = dozen_1 / total * 100
                dozen2_percent = dozen_2 / total * 100
                dozen3_percent = dozen_3 / total * 100

                column1_percent = column_1 / total * 100
                column2_percent = column_2 / total * 100
                column3_percent = column_3 / total * 100

                print(f"\n=== Статистика ===\n"
                    f"Всего чисел: {total}\n"
                    f"Red: {red_count} ({round(red_percent, 2)}%)\n"
                    f"Black: {black_count} ({round(black_percent, 2)}%)\n"
                    f"Even: {even_count} ({round(even_percent, 2)}%)\n"
                    f"Odd: {odd_count} ({round(odd_percent, 2)}%)\n"
                    f"1 to 18: {half_1} ({round(half1_percent, 2)}%)\n"
                    f"19 to 36: {half_2} ({round(half2_percent, 2)}%)\n"
                    f"1 st 12: {dozen_1} ({round(dozen1_percent, 2)}%)\n"
                    f"2 nd 12: {dozen_2} ({round(dozen2_percent, 2)}%)\n"
                    f"3 rd 12: {dozen_3} ({round(dozen3_percent, 2)}%)\n"
                    f"1st column: {column_1} ({round(column1_percent, 2)}%)\n"
                    f"2nd column: {column_2} ({round(column2_percent, 2)}%)\n"
                    f"3rd column: {column_3} ({round(column3_percent, 2)}%)\n"
                    "===================\n")

                with open("results.txt", "a", encoding="utf-8") as file:
                    file.write(str(user_input) + ", ")
            else:
                print("Число вне диапазона (0–36)")
        except ValueError:
            print("Ошибка: введите целое число!")
            with open("results.txt", "a", encoding="utf-8") as file:
                file.write("\n")
            break

def probability(classified_dict):
    # Статистика по цветам
    two_divider = 18 / 37
    three_divider = 12 / 37

    color_prob = two_divider
    current_color = ""
    color_streak = 1

    parity_prob = two_divider
    current_parity = ""
    parity_streak = 1

    half_prob = two_divider
    current_half = ""
    half_streak = 1

    dozen_prob = three_divider
    current_dozen = ""
    dozen_streak = 1
    dozen_dict = {"1 st 12": 0, "2 nd 12": 0, "3 rd 12": 0}

    column_prob = three_divider
    current_column = ""
    column_streak = 1
    column_dict = {"1st": 0, "2nd": 0, "3rd": 0}

    while True:  # Спрашиваем у пользователя число
        try:
            user_input = int(input("Введите число от 0 до 36: "))
            if user_input in classified_dict:
                info = classified_dict[user_input]
                if not user_input == 0:

                    # Вероятность цвета
                    if info['color'] == current_color:
                        color_streak = 1
                        current_color = "red" if current_color == "black" else "black"
                        color_prob = two_divider
                    else:
                        if current_color == "":
                            current_color = "red" if info['color'] == "black" else "black"
                        else:
                            color_streak += 1
                            color_prob = 1 - (19 / 37) ** color_streak

                    # Вероятность четности
                    if info['parity'] == current_parity:
                        parity_streak = 1
                        current_parity = "even" if current_parity == "odd" else "odd"
                        parity_prob = two_divider
                    else:
                        if current_parity == "":
                            current_parity = "even" if info['parity'] == "odd" else "odd"
                        else:
                            parity_streak += 1
                            parity_prob = 1 - (19 / 37) ** parity_streak

                    # Вероятность половины
                    if info['1 to 18/19 to 36'] == current_half:
                        half_streak = 1
                        current_half = "1 to 18" if current_half == "19 to 36" else "19 to 36"
                        half_prob = two_divider
                    else:
                        if current_half == "":
                            current_half = "1 to 18" if info['1 to 18/19 to 36'] == "19 to 36" else "19 to 36"
                        else:
                            half_streak += 1
                            half_prob = 1 - (19 / 37) ** half_streak

                    # Вероятность дюжины
                    for i in dozen_dict:
                        if i == info['dozen']:
                            dozen_dict[info['dozen']] += 1

                    if info['dozen'] == current_dozen:
                        next_dozen = []
                        for i in dozen_dict:
                            if not i == info['dozen']:
                                next_dozen.append(dozen_dict[i])
                        min_dozen = min(next_dozen)
                        next_dozen.clear()
                        for i in dozen_dict:
                            if not i == info['dozen']:
                                if dozen_dict[i] == min_dozen:
                                    current_dozen = i
                        dozen_streak = 1
                        dozen_prob = three_divider
                    else:
                        if current_dozen == "":
                            for i in dozen_dict:
                                if i == info['dozen']:
                                    current_dozen = "2 nd 12" if i == "1 st 12" else "1 st 12"
                        else:
                            dozen_streak += 1
                            dozen_prob = 1 - (25 / 37) ** dozen_streak

                    # Вероятность колонки
                    for i in column_dict:
                        if i == info['column']:
                            column_dict[info['column']] += 1

                    if info['column'] == current_column:
                        next_column = []
                        for i in column_dict:
                            if not i == info['column']:
                                next_column.append(column_dict[i])
                        min_column = min(next_column)
                        next_column.clear()
                        for i in column_dict:
                            if not i == info['column']:
                                if column_dict[i] == min_column:
                                    current_column = i
                        column_streak = 1
                        column_prob = three_divider
                    else:
                        if current_column == "":
                            for i in column_dict:
                                if i == info['column']:
                                    current_column = "2nd" if i == "1st" else "1st"
                        else:
                            column_streak += 1
                            column_prob = 1 - (25 / 37) ** column_streak

                    rounded_color = floor(color_prob * 10000) / 100
                    rounded_parity = floor(parity_prob * 10000) / 100
                    rounded_half = floor(half_prob * 10000) / 100
                    rounded_dozen = floor(dozen_prob * 10000) / 100
                    rounded_column = floor(column_prob * 10000) / 100

                    print(f"\n=== Вероятность ===\n"
                    f"{current_color} ({rounded_color}%)\n"
                    f"{current_parity} ({rounded_parity}%)\n"
                    f"{current_half} ({rounded_half}%)\n"
                    f"{current_dozen} ({rounded_dozen}%)\n"
                    f"{current_column} ({rounded_column}%)\n"
                    "===================\n")

                with open("results.txt", "a", encoding="utf-8") as file:
                    file.write(str(user_input) + ", ")
            else:
                print("Число вне диапазона (0–36)")
        except ValueError:
            print("Ошибка: введите целое число!")
            with open("results.txt", "a", encoding="utf-8") as file:
                file.write("\n")
            break


if __name__ == "__main__":
    nums = []
    nums = classification(nums)

    print("Выберите число из меню:\n"
          "1. Статистика рулетки;\n"
          "2. Анализ рекомендованной ставки.\n")

    try:
        menu = int(input())
        if menu == 1:
            stats(nums)
        elif menu == 2:
            probability(nums)
        else:
            print("Неверное число!")
    except ValueError:
        print("Введите целое число, а не символ!")