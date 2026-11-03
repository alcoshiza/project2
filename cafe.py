import random
from visitors import StandardVisitor, VipVisitor

class CatCafe:
    """Клас, що керує внутрішнім станом та економікою кафе (Інкапсуляція)."""
    def __init__(self, name: str, initial_budget: float, initial_coffee: int, initial_reputation: int):
        self.__name = name                    
        self.__budget = initial_budget        
        self.__coffee_beans = initial_coffee  
        self.__reputation = initial_reputation

    @property
    def name(self) -> str: return self.__name

    @property
    def budget(self) -> float: return self.__budget

    @property
    def coffee_beans(self) -> int: return self.__coffee_beans

    @property
    def reputation(self) -> int: return self.__reputation

    @reputation.setter
    def reputation(self, value: int):
        self.__reputation = max(0, min(100, value))

    def buy_supplies(self, amount: int, price_per_pack: int) -> str:
        if amount <= 0:
            return "⚠️ Кількість має бути більшою за нуль."
        total_cost = amount * price_per_pack
        if self.__budget >= total_cost:
            self.__budget -= total_cost
            self.__coffee_beans += amount
            return f"🛒 Успішно куплено {amount} порцій кави за {total_cost} грн."
        else:
            return "❌ Помилка: Недостатньо коштів на балансі для закупівлі!"

    def update_budget(self, amount: float):
        self.__budget += amount

    def update_reputation(self, amount: int):
        self.reputation = self.__reputation + amount

    def use_coffee(self) -> bool:
        if self.__coffee_beans > 0:
            self.__coffee_beans -= 1
            return True
        return False

    def simulate_day(self, cup_price: float) -> str:
        guest_names = ["Олена", "Максим", "Ірина", "Богдан", "Анастасія", "Дмитро", "Софія"]
        
        base_guests = max(2, int((self.__reputation / 15) - (cup_price / 25)))
        num_guests = base_guests + random.randint(0, 2)
        num_guests = max(1, num_guests)

        log_output = f"--- ☕ Робочий день розпочався (Гостей у черзі: {num_guests}) ---\n"

        visitors = []
        for _ in range(num_guests):
            name = random.choice(guest_names)
            if random.random() < 0.25:
                visitors.append(VipVisitor(name))
            else:
                visitors.append(StandardVisitor(name))

        served_count = 0
        for visitor in visitors:
            log_output += f"👉 {visitor.interact()}\n"
            
            if self.use_coffee():
                self.update_budget(cup_price)
                log_output += f"   ☕ Каву приготовано (+{cup_price:.0f} грн).\n"
                tip = visitor.get_tip()
                if tip > 0:
                    self.update_budget(tip)
                    log_output += f"   🎁 Отримано чайові ВІП-гостя: +{tip} грн!\n"
                served_count += 1
            else:
                log_output += f"   ❌ Бракує зерен кави! Гість пішов розчарованим.\n"
                self.update_reputation(-3)

        log_output += f"📊 Підсумок дня: обслуговано {served_count} гостей.\n"
        return log_output