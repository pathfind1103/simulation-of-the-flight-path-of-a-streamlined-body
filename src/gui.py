import tkinter as tk
from tkinter import messagebox
from src.physics import flight_params
from src.solvers import solve_trajectory
from src.plotter import plot_trajectory


def run_simulation():
    try:
        v0 = float(entry_v0.get())
        theta = float(entry_theta.get())
        t_max, H, L = flight_params(v0, theta)

        # Проверяем, что t_max положительное
        if t_max <= 0:
            messagebox.showerror("Ошибка", "Время полета должно быть положительным!")
            return

        result = solve_trajectory(v0, theta, t_max)
        if result is None:
            messagebox.showerror("Ошибка", "Не удалось вычислить траекторию.")
            return

        t, x, y = result
        print(f"t: {t[:5]}, x: {x[:5]}, y: {y[:5]}")  # Покажем первые 5 элементов

        plot_trajectory(x, y)
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числовые значения!")


root = tk.Tk()
root.title("Моделирование движения тела")

tk.Label(root, text="Начальная скорость (м/с):").grid(row=0, column=0)
entry_v0 = tk.Entry(root)
entry_v0.grid(row=0, column=1)

tk.Label(root, text="Угол (градусы):").grid(row=1, column=0)
entry_theta = tk.Entry(root)
entry_theta.grid(row=1, column=1)

tk.Button(root, text="Смоделировать", command=run_simulation).grid(row=2, column=0, columnspan=2)

root.mainloop()
