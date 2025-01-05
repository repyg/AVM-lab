import numpy as np
import matplotlib.pyplot as plt
import pandas as pd  # Для таблицы

# Исходные точки
points = [
    (-3.0, 12.10), 
    (-2.5, 7.73), 
    (-2.0, 4.08), 
    (-1.5, 1.11),
    (-1.0, -1.12), 
    (-0.5, -2.91), 
    (0.0, -4.18), 
    (0.5, -5.05),
    (1.0, -5.58), 
    (1.5, -5.92), 
    (2.0, -6.00), 
    (2.5, -5.95),
    (3.0, -5.95), 
    (3.5, -6.05)
]

# Выбранные точки для полинома Ньютона
newton_points = [points[0], points[4], points[9], points[12]]

# Функция для полинома Ньютона
def newton_interpolation(x, points):
    def divided_differences(points):
        n = len(points)
        coef = np.zeros([n, n])
        for i, (_, y) in enumerate(points):
            coef[i][0] = y

        for j in range(1, n):
            for i in range(n - j):
                xi, _ = points[i]
                xj, _ = points[i + j]
                coef[i][j] = (coef[i + 1][j - 1] - coef[i][j - 1]) / (xj - xi)
        return coef[0]

    coefs = divided_differences(points)
    result = coefs[0]
    for i in range(1, len(points)):
        term = coefs[i]
        for j in range(i):
            term *= (x - points[j][0])
        result += term
    return result

# Создаём массив x для построения плавного графика
x_vals = np.linspace(-3, 3.5, 14)
y_newton = [newton_interpolation(x, newton_points) for x in x_vals]

# Таблица значений методом Ньютона
table_data = {
    "x": x_vals,
    "y (Ньютон)": y_newton
}
df = pd.DataFrame(table_data)

# Сохранение таблицы в Excel
excel_file = "newton_interpolation_table.xlsx"
try:
    df.to_excel(excel_file, index=False)
    print(f"Таблица сохранена в файл: {excel_file}")
except ModuleNotFoundError:
    print("Ошибка: для записи в Excel требуется установить библиотеку 'openpyxl'.")
    print("Установите её командой: pip install openpyxl")

# Исходные точки для отображения
x_points, y_points = zip(*points)
x_newton, y_newton_points = zip(*newton_points)

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_newton, label="Полином Ньютона", color="blue", linewidth=2)
plt.scatter(x_points, y_points, color="red", label="Исходные точки")
plt.scatter(x_newton, y_newton_points, color="green", label="Точки Ньютона", marker="s")

# Настройка отображения
plt.title("График полученной зависимости")
plt.xlabel("ось x")
plt.ylabel("ось y")
plt.legend()
plt.grid()

# Сохранение графика
plt.savefig("graph_newton_interpolation.png")
plt.show()
