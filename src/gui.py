import tkinter as tk
from tkinter import messagebox
import numpy as np
from src.physics import flight_params, g
from src.solvers import ProjectileMotion, ProjectileMotionWithAirResistance
from src.plotter import plot_trajectory

def run_simulation():
    try:
        # Получаем значения начальной скорости и угла
        v0 = float(entry_v0.get())
        theta = float(entry_theta.get())

        # Получаем параметры полета
        t_max, H, L = flight_params(v0, theta)

        # Проверяем, что t_max положительное
        if t_max <= 0:
            messagebox.showerror("Ошибка", "Время полета должно быть положительным!")
            return

        # Выбираем модель движения в зависимости от выбора пользователя
        if model_choice.get() == "Без сопротивления":
            # Используем класс для траектории без сопротивления
            projectile = ProjectileMotion(v0, theta, t_max)
        elif model_choice.get() == "С сопротивлением":
            # Получаем параметры сопротивления из полей ввода
            Cd = float(entry_Cd.get())
            rho = float(entry_rho.get())
            A = float(entry_A.get())
            m = float(entry_m.get())
            projectile = ProjectileMotionWithAirResistance(v0, theta, t_max, g, Cd, rho, A, m)

        # Решаем траекторию
        t, x, y = projectile.solve_trajectory()

        # Строим график траектории
        plot_trajectory(x, y)

    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числовые значения!")

# Создаем основной интерфейс
root = tk.Tk()
root.title("Моделирование движения тела")

# Устанавливаем размеры окна
root.geometry("400x350")

# Центрируем окно
window_width = 400
window_height = 350
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Создаем элементы интерфейса
tk.Label(root, text="Начальная скорость (м/с):").grid(row=0, column=0)
entry_v0 = tk.Entry(root)
entry_v0.grid(row=0, column=1)

tk.Label(root, text="Угол (градусы):").grid(row=1, column=0)
entry_theta = tk.Entry(root)
entry_theta.grid(row=1, column=1)

# Выпадающий список для выбора модели
tk.Label(root, text="Модель движения:").grid(row=2, column=0)
model_choice = tk.StringVar()
model_choice.set("Без сопротивления")  # Модель по умолчанию
model_menu = tk.OptionMenu(root, model_choice, "Без сопротивления", "С сопротивлением")
model_menu.grid(row=2, column=1)

# Создаем дополнительные поля для модели с сопротивлением
tk.Label(root, text="Коэффициент сопротивления (Cd):").grid(row=3, column=0)
entry_Cd = tk.Entry(root)
entry_Cd.insert(0, "0.47")  # Значение по умолчанию
entry_Cd.grid(row=3, column=1)

tk.Label(root, text="Плотность воздуха (rho):").grid(row=4, column=0)
entry_rho = tk.Entry(root)
entry_rho.insert(0, "1.225")  # Значение по умолчанию
entry_rho.grid(row=4, column=1)

tk.Label(root, text="Площадь поперечного сечения (A):").grid(row=5, column=0)
entry_A = tk.Entry(root)
entry_A.insert(0, "0.1")  # Значение по умолчанию
entry_A.grid(row=5, column=1)

tk.Label(root, text="Масса тела (m):").grid(row=6, column=0)
entry_m = tk.Entry(root)
entry_m.insert(0, "1.0")  # Значение по умолчанию
entry_m.grid(row=6, column=1)

# Кнопка для запуска моделирования
tk.Button(root, text="Смоделировать", command=run_simulation).grid(row=7, column=0, columnspan=2)

# Функция для отображения/скрытия полей с параметрами сопротивления
def toggle_resistance_fields(*args):
    if model_choice.get() == "С сопротивлением":
        entry_Cd.grid(row=3, column=1)
        entry_rho.grid(row=4, column=1)
        entry_A.grid(row=5, column=1)
        entry_m.grid(row=6, column=1)
    else:
        entry_Cd.grid_forget()
        entry_rho.grid_forget()
        entry_A.grid_forget()
        entry_m.grid_forget()

# Привязываем функцию к изменению выбора модели
model_choice.trace("w", toggle_resistance_fields)

# Изначально скрываем поля с параметрами сопротивления
toggle_resistance_fields()

# Запуск интерфейса
root.mainloop()
