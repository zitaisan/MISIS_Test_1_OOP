from abc import ABC, abstractmethod
from typing import List, Optional
import copy

class Printable(ABC):
    """Base abstract class for printable objects."""
    
    def print_me(self, os, prefix="", is_last=False, no_slash=False, is_root=False):
        """Base printing method for the tree structure display.
        Implement properly to display hierarchical structure."""
        # To be implemented
        
    @abstractmethod
    def clone(self):
        """Create a deep copy of this object."""
        pass

class BasicCollection(Printable):
    """Base class for collections of items."""
    def __init__(self):
        self.items = []
    
    def add(self, elem):
        # To be implemented
        pass
    
    def find(self, elem):
        # To be implemented
        pass

class Component(Printable):
    """Base class for computer components."""
    def __init__(self, numeric_val=0):
        self.numeric_val = numeric_val
        
    # To be implemented

class Address(Printable):
    """Class representing a network address."""
    def __init__(self, addr):
        self.address = addr
    
    # To be implemented

class Computer(BasicCollection, Component):
    """Class representing a computer with addresses and components."""
    def __init__(self, name):
        self.name = name
        self.addresses = []
        self.components = []
    
    def add_address(self, addr):
        # To be implemented
        return self
    
    def add_component(self, comp):
        # To be implemented
        return self
    
    # Другие методы...

class Network(Printable):
    """Class representing a network of computers."""
    def __init__(self, name):
        self.name = name
        self.computers = []
    
    def add_computer(self, comp):
        # To be implemented
        return self
    
    def find_computer(self, name):
        # To be implemented
        return None
    
    # Другие методы...

class Disk(Component):
    """Disk component class with partitions."""
    # Определение типов дисков
    SSD = 0
    MAGNETIC = 1
    
    def __init__(self, storage_type, size):
        # Initialize properly
        self.partitions = []
    
    def add_partition(self, size, name):
        # To be implemented
        return self

class CPU(Component):
    """CPU component class."""
    def __init__(self, cores, mhz):
        # To be implemented
        pass

class Memory(Component):
    """Memory component class."""
    def __init__(self, size):
        # To be implemented
        pass

# Пример использования (может быть неполным или содержать ошибки)
def main():
    # Создание тестовой сети
    n = Network("MISIS network")
    
    # Добавляем первый сервер с одним CPU и памятью
    n.add_computer(
        Computer("server1.misis.ru")
        .add_address("192.168.1.1")
        .add_component(CPU(4, 2500))
        .add_component(Memory(16000))
    )
    
    # Добавляем второй сервер с CPU и HDD с разделами
    n.add_computer(
        Computer("server2.misis.ru")
        .add_address("10.0.0.1")
        .add_component(CPU(8, 3200))
        .add_component(
            Disk(Disk.MAGNETIC, 2000)
            .add_partition(500, "system")
            .add_partition(1500, "data")
        )
    )
    
    # Выводим сеть для проверки форматирования
    print("=== Созданная сеть ===")
    print(n)
    
    # Тест ожидаемого вывода
    expected_output = """Network: MISIS network
+-Host: server1.misis.ru
| +-192.168.1.1
| +-CPU, 4 cores @ 2500MHz
| \-Memory, 16000 MiB
\-Host: server2.misis.ru
  +-10.0.0.1
  +-CPU, 8 cores @ 3200MHz
  \-HDD, 2000 GiB
    +-[0]: 500 GiB, system
    \-[1]: 1500 GiB, data"""
    
    assert str(n) == expected_output, "Формат вывода не соответствует ожидаемому"
    print("✓ Тест формата вывода пройден")
    
    # Тестируем глубокое копирование
    print("\n=== Тестирование глубокого копирования ===")
    x = n.clone()
    
    # Тестируем поиск компьютера
    print("Поиск компьютера server2.misis.ru:")
    c = x.find_computer("server2.misis.ru")
    print(c)
    
    # Модифицируем найденный компьютер в копии
    print("\nДобавляем SSD к найденному компьютеру в копии:")
    c.add_component(
        Disk(Disk.SSD, 500)
        .add_partition(500, "fast_storage")
    )
    
    # Проверяем, что оригинал не изменился
    print("\n=== Модифицированная копия ===")
    print(x)
    print("\n=== Исходная сеть (должна остаться неизменной) ===")
    print(n)
    
    # Проверяем ассерты для тестирования системы
    print("\n=== Выполнение тестов ===")
    
    # Тест поиска
    assert x.find_computer("server1.misis.ru") is not None, "Компьютер не найден"
    print("✓ Тест поиска пройден")
    
    # Тест независимости копий
    original_server2 = n.find_computer("server2.misis.ru")
    modified_server2 = x.find_computer("server2.misis.ru")
    
    original_components = sum(1 for _ in original_server2.components)
    modified_components = sum(1 for _ in modified_server2.components)
    
    assert original_components == 2, f"Неверное количество компонентов в оригинале: {original_components}"
    assert modified_components == 3, f"Неверное количество компонентов в копии: {modified_components}"
    print("✓ Тест независимости копий пройден")
    
    # Проверка типов дисков
    disk_tests = [
        (Disk(Disk.SSD, 256), "SSD"),
        (Disk(Disk.MAGNETIC, 1000), "HDD")
    ]
    
    for disk, expected_type in disk_tests:
        assert expected_type in str(disk), f"Неверный тип диска в выводе: {str(disk)}"
    print("✓ Тест типов дисков пройден")
    
    print("\nВсе тесты пройдены!")

if __name__ == "__main__":
    main()