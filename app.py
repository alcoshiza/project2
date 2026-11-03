import tkinter as tk
from tkinter import messagebox
from cafe import CatCafe

class CatCafeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🐾 Скотч Кафе — Симулятор")
        self.root.geometry("650x700")
        self.root.config(bg="#FDFBF7")

        self.cafe = CatCafe("Скотч", 2500.0, 20, 70)
        self.day = 1
        self.max_days = 5

        self.create_widgets()
        self.update_status_labels()

    def create_widgets(self):
        self.BG_COLOR = "#FDFBF7"
        self.CARD_BG = "#F4ECE1"
        self.TEXT_COLOR = "#3E2723"
        self.BTN_BG = "#8D6E63"
        self.BTN_FG = "#FFFFFF"

        title_label = tk.Label(
            self.root, text="🐾 Котяче Кафе «Скотч»", 
            font=("Segoe UI", 18, "bold"), bg=self.BG_COLOR, fg=self.TEXT_COLOR
        )
        title_label.pack(pady=10)

        # Панель статусу
        self.status_frame = tk.Frame(self.root, bg=self.CARD_BG, bd=1, relief="solid")
        self.status_frame.pack(fill="x", padx=20, pady=10, ipady=10)

        self.lbl_day = tk.Label(self.status_frame, text="", font=("Segoe UI", 11, "bold"), bg=self.CARD_BG, fg=self.TEXT_COLOR)
        self.lbl_day.pack(side="left", expand=True)

        self.lbl_budget = tk.Label(self.status_frame, text="", font=("Segoe UI", 11, "bold"), bg=self.CARD_BG, fg="#2E7D32")
        self.lbl_budget.pack(side="left", expand=True)

        self.lbl_coffee = tk.Label(self.status_frame, text="", font=("Segoe UI", 11, "bold"), bg=self.CARD_BG, fg="#D84315")
        self.lbl_coffee.pack(side="left", expand=True)

        self.lbl_reputation = tk.Label(self.status_frame, text="", font=("Segoe UI", 11, "bold"), bg=self.CARD_BG, fg="#1565C0")
        self.lbl_reputation.pack(side="left", expand=True)

        # Панель керування
        control_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        control_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(control_frame, text="Докупити зерна (1 шт = 25 грн):", font=("Segoe UI", 10), bg=self.BG_COLOR, fg=self.TEXT_COLOR).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_coffee = tk.Entry(control_frame, font=("Segoe UI", 10), width=10, bd=1, relief="solid")
        self.entry_coffee.grid(row=0, column=1, padx=10, pady=5)
        self.entry_coffee.insert(0, "5")

        tk.Label(control_frame, text="Ціна за чашку кави (грн):", font=("Segoe UI", 10), bg=self.BG_COLOR, fg=self.TEXT_COLOR).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_price = tk.Entry(control_frame, font=("Segoe UI", 10), width=10, bd=1, relief="solid")
        self.entry_price.grid(row=1, column=1, padx=10, pady=5)
        self.entry_price.insert(0, "60")

        self.btn_action = tk.Button(
            self.root, text="РОЗПОЧАТИ РОБОЧИЙ ДЕНЬ ☕", 
            font=("Segoe UI", 11, "bold"), bg=self.BTN_BG, fg=self.BTN_FG, 
            activebackground="#6D4C41", activeforeground="#FFFFFF",
            relief="flat", cursor="hand2", command=self.run_day
        )
        self.btn_action.pack(pady=15, ipadx=15, ipady=8)

        # Консоль / лог
        log_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(log_frame, text="Журнал подій кафе:", font=("Segoe UI", 10, "bold"), bg=self.BG_COLOR, fg=self.TEXT_COLOR).pack(anchor="w")
        
        self.text_log = tk.Text(log_frame, height=15, font=("Consolas", 10), bg="#FFFFFF", fg="#2C2C2C", bd=1, relief="solid", padx=10, pady=10)
        self.text_log.pack(fill="both", expand=True, pady=5)
        self.text_log.config(state="disabled")

    def update_status_labels(self):
        self.lbl_day.config(text=f"📅 День: {self.day}/{self.max_days}")
        self.lbl_budget.config(text=f"💰 Бюджет: {self.cafe.budget:.0f} грн")
        self.lbl_coffee.config(text=f"☕ Зерна: {self.cafe.coffee_beans} шт")
        self.lbl_reputation.config(text=f"⭐ Репутація: {self.cafe.reputation}")

    def log_message(self, message: str):
        self.text_log.config(state="normal")
        self.text_log.insert("end", message + "\n")
        self.text_log.see("end")
        self.text_log.config(state="disabled")

    def run_day(self):
        if self.day > self.max_days:
            messagebox.showinfo("Гра завершена", "Зміни вже закінчилися!")
            return

        try:
            coffee_amount = int(self.entry_coffee.get())
            cup_price = float(self.entry_price.get())
            if cup_price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Помилка", "Будь ласка, введіть коректні числові значення!")
            return

        self.log_message(f"\n{'='*10} ДЕНЬ {self.day} {'='*10}")

        if coffee_amount > 0:
            msg = self.cafe.buy_supplies(coffee_amount, 25)
            self.log_message(msg)

        day_log = self.cafe.simulate_day(cup_price)
        self.log_message(day_log)

        if self.cafe.budget < 0:
            self.log_message("💀 БАНКРУТСТВО! Гроші закінчилися через борги.")
            messagebox.showerror("Кінець гри", "Кафе змушене зачинитися через борги!")
            self.btn_action.config(state="disabled")
            return

        self.update_status_labels()
        self.day += 1

        if self.day > self.max_days:
            self.log_message("\n🎉 ГРУ ЗАВЕРШЕНО УСПІШНО!")
            messagebox.showinfo("Перемога!", f"Вітаємо! Кафе успішно пропрацювало всі дні.\nФінальний бюджет: {self.cafe.budget:.0f} грн")
            self.btn_action.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = CatCafeApp(root)
    root.mainloop()