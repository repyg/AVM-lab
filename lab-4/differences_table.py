import pandas as pd
from main import points

# Извлекаем значения y и x для индекса
x_values = [x for x, _ in points]
y_values = [y for _, y in points]
n = len(y_values)

# Построение таблицы конечных разностей
differences = [y_values]
for i in range(1, n):
    delta_y = [differences[i-1][j+1] - differences[i-1][j] for j in range(n-i)]
    differences.append(delta_y)

# Создаем DataFrame и заполняем его значениями
table_data = {
    "x": [f"{x:.2f}" for x in x_values],  # Индексируем x как строки для визуальной наглядности
    "y(x)": y_values
}
for i, delta_y in enumerate(differences):
    if i == 0:
        continue
    col_name = f"Δ^{i}y"
    # Добавляем разности в виде столбцов
    table_data[col_name] = delta_y + [None] * (n - len(delta_y))  # Заполняем только значимые значения, остальное None

# Создаем DataFrame
table = pd.DataFrame(table_data)

# Рассчитываем максимальные значения модулей для каждой степени разностей (d_m)
dm_row = {
    "x": "d_m",
    "y(x)": None
}
min_dm = max(differences[0]) - min(differences[0])
for i in range(1, len(differences)-1):
    col_name = f"Δ^{i}y"
    dm_row[col_name] = max(differences[i]) - min(differences[i])  # Максимум модуля в каждом столбце разностей
    min_dm = max(differences[i]) - min(differences[i]) if min_dm > max(differences[i]) - min(differences[i]) else min_dm
# Добавляем строку d_m в таблицу с помощью pd.concat()
dm_df = pd.DataFrame([dm_row])
table = pd.concat([table, dm_df], ignore_index=True)

# Добавляем строку с минимальным значением d_m
min_dm_row = {
    "x": "Минимум d_m",
    "y(x)": None
}
for i in range(1, len(differences)):
    col_name = f"Δ^{i}y"
    min_dm_row[col_name] = min_dm if dm_row.get(col_name) == min_dm else None

# Добавляем строку минимального значения d_m в таблицу
min_dm_df = pd.DataFrame([min_dm_row])
table = pd.concat([table, min_dm_df], ignore_index=True)

# Сохранение таблицы в Excel
file_path = 'differences_table.xlsx'  # Путь к файлу на вашем компьютере
table.to_excel(file_path, index=False)

print(f"Таблица конечных разностей сохранена в файл: {file_path}")
