from abc import ABC, abstractmethod
import copy
from io import StringIO


class Printable(ABC):
    """Base abstract class for printable objects."""

    def print_me(self, os, prefix="", is_last=False, no_slash=False, is_root=False):
        """Base printing method for the tree structure display.
        Implement properly to display hierarchical structure."""
        # To be implemented
        pass

    @abstractmethod
    def clone(self):
        """Create a deep copy of this object."""
        pass

    def __str__(self):
        buffer = StringIO()
        self.print_me(buffer, is_root=True)
        return buffer.getvalue()


class BasicCollection(Printable):
    """Base class for collections of items."""

    def __init__(self):
        self.items = []

    def add(self, elem):
        # To be implemented
        self.items.append(elem)
        return self

    def find(self, elem):
        # To be implemented
        return next((item for item in self.items if item == elem), None)

    def clone(self):
        new_collection = self.__class__()
        new_collection.items = [item.clone() for item in self.items]
        return new_collection


class Component(Printable):
    """Base class for computer components."""

    def __init__(self, numeric_val=0):
        self.numeric_val = numeric_val

    # To be implemented
    def clone(self):
        return copy.deepcopy(self)


class Address(Printable):
    """Class representing a network address."""

    def __init__(self, addr):
        self.address = addr

    # To be implemented
    def print_me(self, os, prefix="", is_last=False, no_slash=False, is_root=False):
        os.write(f"{prefix}{'\\-' if is_last else '+-'}{self.address}\n")

    def clone(self):
        return Address(self.address)


class Computer(BasicCollection, Component):
    """Class representing a computer with addresses and components."""

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.addresses = []
        self.components = []

    def add_address(self, addr):
        self.addresses.append(Address(addr))
        return self

    def add_component(self, comp):
        self.components.append(comp)
        return self

    def print_me(self, os, prefix="", is_last=False, no_slash=False, is_root=False):
        new_prefix = prefix + ("  " if is_last else "| ")

        os.write(f"{prefix}{'\\-' if is_last else '+-'}Host: {self.name}\n")

        for i, addr in enumerate(self.addresses):
            addr.print_me(os, new_prefix, i == len(self.addresses) - 1 and not self.components)

        for i, comp in enumerate(self.components):
            comp.print_me(os, new_prefix, i == len(self.components) - 1, no_slash=not self.addresses)

    def clone(self):
        new_computer = Computer(self.name)
        new_computer.addresses = [addr.clone() for addr in self.addresses]
        new_computer.components = [comp.clone() for comp in self.components]
        return new_computer


class Network(Printable):
    """Class representing a network of computers."""

    def __init__(self, name):
        self.name = name
        self.computers = []

    def add_computer(self, comp):
        self.computers.append(comp)
        return self

    def find_computer(self, name):
        return next((comp for comp in self.computers if comp.name == name), None)

    def print_me(self, os, prefix="", is_last=False, no_slash=False, is_root=False):
        os.write(f"Network: {self.name}\n")
        for i, comp in enumerate(self.computers):
            comp.print_me(os, prefix, i == len(self.computers) - 1)

    def clone(self):
        new_network = Network(self.name)
        new_network.computers = [comp.clone() for comp in self.computers]
        return new_network


class Disk(Component):
    """Disk component class with partitions."""
    # Определение типов дисков
    SSD = 0
    MAGNETIC = 1

    def __init__(self, storage_type, size):
        # Initialize properly
        super().__init__()
        self.storage_type = storage_type
        self.size = size
        self.partitions = []

    def add_partition(self, size, name):
        # To be implemented
        self.partitions.append((size, name))
        return self

    def print_me(self, os, prefix="", is_last=False, no_slash=False, is_root=False):
        disk_type = "SSD" if self.storage_type == Disk.SSD else "HDD"
        os.write(f"{prefix}{'\\-' if is_last else '+-'}{disk_type}, {self.size} GiB\n")

        new_prefix = prefix + ("  " if is_last else "| ")
        for i, (size, name) in enumerate(self.partitions):
            os.write(f"{new_prefix}{'\\-' if i == len(self.partitions) - 1 else '+-'}[{i}]: {size} GiB, {name}\n")

    def clone(self):
        new_disk = Disk(self.storage_type, self.size)
        new_disk.partitions = copy.deepcopy(self.partitions)
        return new_disk


class CPU(Component):
    """CPU component class."""

    def __init__(self, cores, mhz):
        super().__init__()
        self.cores = cores
        self.mhz = mhz

    def print_me(self, os, prefix="", is_last=False, no_slash=False, is_root=False):
        os.write(f"{prefix}{'\\-' if is_last else '+-'}CPU, {self.cores} cores @ {self.mhz}MHz\n")

    def clone(self):
        return CPU(self.cores, self.mhz)


class Memory(Component):
    """Memory component class."""

    def __init__(self, size):
        # To be implemented
        super().__init__()
        self.size = size

    def print_me(self, os, prefix="", is_last=False, no_slash=False, is_root=False):
        os.write(f"{prefix}{'\\-' if is_last else '+-'}Memory, {self.size} MiB\n")

    def clone(self):
        return Memory(self.size)


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

    assert str(n).strip() == expected_output.strip(), "Формат вывода не соответствует ожидаемому"
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

    original_components = len(original_server2.components)
    modified_components = len(modified_server2.components)

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
