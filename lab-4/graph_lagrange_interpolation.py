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

# Выбранные точки для полинома Лагранжа
lagrange_points = [points[0], points[6], points[12]]

# Функция для полинома Лагранжа
def lagrange_interpolation(x, points):
    def L(k, x):
        xk, _ = points[k]
        result = 1
        for i, (xi, _) in enumerate(points):
            if i != k:
                result *= (x - xi) / (xk - xi)
        return result
    
    return sum(y * L(k, x) for k, (xk, y) in enumerate(points))

# Создаём массив x для построения плавного графика
x_vals = np.linspace(-3, 3.5, 14)
y_lagrange = [lagrange_interpolation(x, lagrange_points) for x in x_vals]

# Таблица значений методом Лагранжа
table_data = {
    "x": x_vals,
    "y (Лагранж)": y_lagrange
}
df = pd.DataFrame(table_data)

# Сохранение таблицы в Excel
excel_file = "lagrange_interpolation_table.xlsx"
df.to_excel(excel_file, index=False)

print(f"Таблица сохранена в файл: {excel_file}")

# Исходные точки для отображения
x_points, y_points = zip(*points)
x_lagrange, y_lagrange_points = zip(*lagrange_points)

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_lagrange, label="Полином Лагранжа", color="blue", linewidth=2)
plt.scatter(x_points, y_points, color="red", label="Исходные точки")
plt.scatter(x_lagrange, y_lagrange_points, color="green", label="Точки Лагранжа", marker="s")

# Настройка отображения
plt.title("График полученной зависимости")
plt.xlabel("ось x")
plt.ylabel("ось y")
plt.legend()
plt.grid()

# Сохранение графика
plt.savefig("graph_lagrange_interpolation.png")
plt.show()
