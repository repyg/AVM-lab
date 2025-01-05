import numpy as np
import pandas as pd

# Данные исходных точек
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

# Точки для интерполяции
lagrange_points = [points[0], points[6], points[12]]
newton_points = [points[0], points[4], points[9], points[12]]

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

# Вычисляем значения полиномов для всех x точек
x_values = [x for x, y in points]
y_values = [y for x, y in points]

# Результаты интерполяции для каждого метода
lagrange_results = [lagrange_interpolation(x, lagrange_points) for x in x_values]
newton_results = [newton_interpolation(x, newton_points) for x in x_values]

# Вычисляем квадраты отклонений для каждого метода
lagrange_errors = [(y - y_lagrange) ** 2 for y, y_lagrange in zip(y_values, lagrange_results)]
newton_errors = [(y - y_newton) ** 2 for y, y_newton in zip(y_values, newton_results)]

# Среднеквадратичные ошибки
lagrange_mse_all = np.mean(lagrange_errors)
newton_mse_all = np.mean(newton_errors)

# Среднеквадратичные ошибки в точках, не использованных для интерполяции
excluded_points = set([0, 6, 12])  # Индексы точек для Лагранжа
lagrange_excl_errors = [err for idx, err in enumerate(lagrange_errors) if idx not in excluded_points]
lagrange_mse_excl = np.mean(lagrange_excl_errors)

excluded_points_newton = set([0, 4, 9, 12])  # Индексы точек для Ньютона
newton_excl_errors = [err for idx, err in enumerate(newton_errors) if idx not in excluded_points_newton]
newton_mse_excl = np.mean(newton_excl_errors)

# Создание таблиц для вывода
mse_data = {
    "": ["Во всех точках", "В точках, не использованных для получения интерполяционного полинома"],
    "Формула Лагранжа": [lagrange_mse_all, lagrange_mse_excl],
    "Формула Ньютона": [newton_mse_all, newton_mse_excl]
}

deviation_data = {
    "Формула Лагранжа": lagrange_errors,
    "Формула Ньютона": newton_errors
}

# Создаем DataFrame для среднеквадратичных ошибок
mse_df = pd.DataFrame(mse_data)

# Создаем DataFrame для квадратов отклонений
deviation_df = pd.DataFrame(deviation_data)

# Путь к файлу для сохранения
file_path = 'interpolation_errors.xlsx'

# Создаем ExcelWriter для сохранения в один файл на разных листах
with pd.ExcelWriter(file_path) as writer:
    # Сохраняем среднеквадратичные ошибки на первом листе
    mse_df.to_excel(writer, sheet_name='Среднеквадратичная ошибка', index=False)
    
    # Сохраняем квадраты отклонений на втором листе
    deviation_df.to_excel(writer, sheet_name='Квадраты отклонений', index=False)

print("Таблицы успешно сохранены в файл:", file_path)
