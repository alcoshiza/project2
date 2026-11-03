from abc import ABC, abstractmethod

class Visitor(ABC):
    """Абстрактний базовий клас для відвідувачів кафе (Абстракція)."""
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def interact(self) -> str:
        pass

    @abstractmethod
    def get_tip(self) -> int:
        pass


class StandardVisitor(Visitor):
    """Звичайний гість (Наслідування)."""
    def interact(self) -> str:
        return f"Гість {self._name} спокійно п'є каву і роздивляється котиків."

    def get_tip(self) -> int:
        return 0


class VipVisitor(Visitor):
    """VIP-гість (Наслідування та Поліморфізм)."""
    def interact(self) -> str:
        return f"⭐ ВІП-ГІСТЬ {self._name} зробив гучний сторіс у соцмережах про котяче кафе!"

    def get_tip(self) -> int:
        return 100